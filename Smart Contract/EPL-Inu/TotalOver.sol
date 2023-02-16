//SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.7;

import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

interface IERC20 {
    function transfer(address to, uint256 value) external returns (bool);

    function approve(
        address owner,
        address spender,
        uint256 amount
    ) external returns (bool);

    function transferFrom(
        address from,
        address to,
        uint256 value
    ) external returns (bool);

    function balanceOf(address owner) external view returns (uint256 balance);
}

interface ERC721A {
    function safeMintTo(address toAddress, uint256 _quanity) external;
}

interface ERC1155 {
    function balanceOf(
        address account,
        uint256 id
    ) external view returns (uint256);

    function getTimeExpired(
        uint8 _id,
        address _sender
    ) external view returns (uint256);

    function checkVipRate(uint8 _tokenId) external pure returns (uint256);
}

interface Consumer {
    function requestMatchResolve(
        address oracle,
        string memory jobId,
        string memory date,
        string memory eventId
    ) external;

    function requestMatchCreated(
        address oracle,
        string memory jobId,
        string memory date
    ) external;

    function getLatestMatchId() external view returns (bytes memory);

    function decodeMatchDetails(
        bytes calldata data
    )
        external
        pure
        returns (
            bytes32 eventId,
            bytes memory homeName,
            bytes memory awayName,
            bytes memory eventStatus,
            int8 scoreHome,
            int8 scoreAway,
            bytes memory pointSpreadHome,
            bytes memory totalOver
        );

    function convertByteToString(
        bytes calldata data
    ) external pure returns (string memory);
}

//Bet
//consume match
abstract contract MatchConsumer is Ownable {
    bytes public latestEventId;
    address public principle = 0xE515BA407b97B053F89c4eecb8886F4C6101d4A3;
    address public consumerAddress = 0xa43BD502034BAEC38d2ad1B66e3A57ebF99c3b29;
    address public oracleAddress = 0xfF97c3F8c3993Ab8108eBaF3E45535fe4B1B5CBE;

    Consumer public consumer;

    constructor() {
        consumer = Consumer(consumerAddress);
    }

    modifier onlyApproveAddress(address sender) {
        require(
            msg.sender == consumerAddress ||
                msg.sender == owner() ||
                msg.sender == oracleAddress,
            "Cannot call this function"
        );
        _;
    }

    /**
     *@notice request result of a match
     * @param _oracle address of oracle
     * @param _jobId job id
     * @param _date date of match
     * @param _eventId id of match
     */
    function requestGameResolved(
        address _oracle,
        string memory _jobId,
        string memory _date,
        string memory _eventId
    ) external onlyOwner {
        consumer.requestMatchResolve(_oracle, _jobId, _date, _eventId);
    }

    /**
     * @notice View data latest event request from oracle
     * @return id data of last event request in bytes
     */
    function getLatestEvent() external view returns (bytes memory) {
        return consumer.getLatestMatchId();
    }

    /**
     *@notice decode data and pick winner of match
     * @dev require approve addresses
     * @param _data bytes data of match
     */
    function fullFillResult(
        bytes calldata _data
    ) internal onlyApproveAddress(msg.sender) {
        (
            bytes32 eventId,
            ,
            ,
            bytes memory eventStatus,
            int8 scoreHome,
            int8 scoreAway,
            ,

        ) = consumer.decodeMatchDetails(_data);

        innerFulfillResult(eventId, scoreHome, scoreAway, eventStatus);
    }

    function innerFulfillResult(
        bytes32 _eventId,
        int8 _scoreHome,
        int8 _scoreAway,
        bytes memory _eventStatus
    ) internal virtual;

    /**
     *@dev convert bytes to string
     * @param _bytes32 data in bytes32
     * @return  data data in string
     */
    function bytes32ToString(
        bytes32 _bytes32
    ) internal pure returns (string memory) {
        uint8 i = 0;
        while (i < 32 && _bytes32[i] != 0) {
            i++;
        }
        bytes memory bytesArray = new bytes(i);
        for (i = 0; i < 32 && _bytes32[i] != 0; i++) {
            bytesArray[i] = _bytes32[i];
        }
        return string(bytesArray);
    }
}

contract Spread is MatchConsumer, ReentrancyGuard {
    enum Team {
        NO,
        HOME,
        AWAY
    }
    enum Status {
        NOTSTART,
        BETTING,
        END,
        REFUND
    }
    struct Betting {
        // khi nhập 2 param address và match id thì trả về bao gồm tiền bet và đội dự đoán
        uint256 amount;
        Team chosenTeam; //1 = HOME, 2 = AWAY
        uint256 premiumPool;
    }
    struct Match {
        Status status; //0 = NOTSTART,1 = BETTING, 2 = END, 3 = REFUND
        Team winningTeam; //1 = HOME, 2 = AWAY
        int256 spread;
        uint256 expired;
        uint256 rewardPool;
    }

    mapping(address => mapping(string => Betting)) bets; //thêm 1 entry(1 betting) (địa chỉ ví => matchId => tiền tham gia và đội chọn)
    mapping(string => mapping(uint8 => uint256)) pools; //xác định tiền của pool thua và pool thắng của 1 match (matchId=> chọn pool thắng hoặc thua => tiền trong pool đó
    mapping(string => Match) matches; //lưu đội thắng của 1 match (matchId=> đội thắng và tình hình trận đấu kết thúc)
    mapping(string => mapping(uint8 => uint256)) totalRate;
    uint256 public ratioFee = 5;
    address public constant token = 0x78867BbEeF44f2326bF8DDd1941a4439382EF2A7;
    address public ticketAddress = 0x9826781a716cb3C3118fc7d1dAab5C57410cD2C2;
    address public vipNFT = 0x1f5315252e9223e7d76d09c0dCb1DAB8ca17baf9;

    //Events
    /**
     * @dev pop up when match is opened for betting
     * @param _eventId id of a match
     */
    event MatchStarted(string _eventId);

    /**
     *@dev pop up when match is closed for betting
     * @param _eventId id of a match
     */
    event MatchEnded(string _eventId);

    /**
     *@dev pop up when match is canceled
     * @param _eventId id of a match
     */
    event MatchCanceled(string _eventId);

    /**
     *@dev pop up when bettor takes part in bet
     * @param sender address of bettor
     * @param _eventId id of a match
     * @param betAmount bet amount
     * @param _team chosen team by bettor
     */
    event TicketBought(
        address sender,
        string _eventId,
        uint256 betAmount,
        uint256 _team
    );

    /**
     *@dev pop up when bettor cancels bet
     * @param sender address of uses
     * @param _eventId id of a match
     * @param betAmount bet amount
     * @param _team chosen team by bettor
     */
    event TicketCanceled(
        address sender,
        string _eventId,
        uint256 betAmount,
        uint256 _team
    );

    /**
     *@dev pop up when admin picks winner of a match
     * @param _eventId id of a match
     * @param _winningTeam winner of a match (home or away)
     */
    event WinnerPicked(string _eventId, Team _winningTeam);

    error InvalidMatch(string _eventId);
    error NotEndYet(string _eventId);
    error NotCreateBetYet(string _eventId);

    modifier isBetting(string calldata _eventId) {
        Match memory game = matches[_eventId];
        uint256 thisGame = uint256(matches[_eventId].status);
        if (thisGame != 1) {
            revert InvalidMatch(_eventId);
        }
        _;
    }

    function innerFulfillResult(
        bytes32 _eventId,
        int8 _scoreHome,
        int8 _scoreAway,
        bytes memory _eventStatus
    ) internal override {
        string memory eventId = bytes32ToString(_eventId);
        require(uint256(matches[eventId].status) == 1, "Bet is not created");
        string memory eventStatus = consumer.convertByteToString(_eventStatus);
        chooseWinner(eventId, eventStatus, _scoreHome, _scoreAway);
    }

    /**
     *@notice Open bet for a match
     * @dev require only owner
     * @param _timeExpired time close bet
     * @param _spread home team spread
     * @param _eventId id of match
     */
    function openBetting(
        uint256[] calldata _timeExpired,
        int256[] calldata _spread,
        string[] calldata _eventId,
        uint256[] calldata _rewardPool
    ) external onlyOwner {
        require(_timeExpired.length == _spread.length, "Error");
        require(_timeExpired.length == _eventId.length, "Error");
        uint256 totalReward = 0;
        for (uint256 i = 0; i < _timeExpired.length; i++) {
            matches[_eventId[i]] = Match(
                Status.BETTING,
                Team.NO,
                _spread[i],
                _timeExpired[i],
                _rewardPool[i]
            );
            totalReward += _rewardPool[i];
            emit MatchStarted(_eventId[i]);
        }
        IERC20(token).transferFrom(msg.sender, address(this), totalReward);
    }

    /**
     *@notice Cancel bet for a match
     * @dev require match is opened for betting, only owner
     * @param _eventId id of match
     */
    function cancelBetting(string calldata _eventId) external onlyOwner {
        require(
            matches[_eventId].status == Status.BETTING,
            "Bet is not created"
        );

        uint256 time = matches[_eventId].expired;
        int256 _spread = matches[_eventId].spread;
        IERC20(token).transfer(msg.sender, matches[_eventId].rewardPool);
        matches[_eventId] = Match(Status.REFUND, Team.NO, _spread, time, 0);

        emit MatchCanceled(_eventId);
    }

    /**
     *@notice choosing winner for a match
     * @dev require status full time, no winner yet
     * @param _eventId id of match\
     * @param _eventStatus status of match
     * @param _home scores of home team
     * @param _away scores of away team
     */
    function chooseWinner(
        string memory _eventId,
        string memory _eventStatus,
        int256 _home,
        int256 _away
    ) public onlyApproveAddress(msg.sender) {
        require(
            keccak256(abi.encodePacked(_eventStatus)) ==
                keccak256(abi.encodePacked("STATUS_FULL_TIME")),
            "ERROR"
        );
        require(
            uint256(matches[_eventId].status) != 2 &&
                uint256(matches[_eventId].status) != 3,
            "Already end"
        );
        uint256 time = matches[_eventId].expired;
        int256 _spread = matches[_eventId].spread;
        uint256 rewardPool = matches[_eventId].rewardPool;
        if (_home * 10 ** 18 + _spread - _away * 10 ** 18 > 0) {
            matches[_eventId] = Match(
                Status.END,
                Team.HOME,
                _spread,
                time,
                rewardPool
            );
            emit WinnerPicked(_eventId, Team.HOME);
        } else {
            matches[_eventId] = Match(
                Status.END,
                Team.AWAY,
                _spread,
                time,
                rewardPool
            );
            emit WinnerPicked(_eventId, Team.AWAY);
        }
    }

    function calculateBetFee(
        uint256 _betAmount
    ) private view returns (uint256, uint256) {
        uint256 fee = (_betAmount * ratioFee) / 100;
        return (_betAmount - fee, fee);
    }

    /**
     *@notice entry bet for a match
     * @dev require the bet is opened, enough balance to bet
     * @param _eventId id of match
     * @param _amount money amount
     * @param _team chosen team
     */
    function placeBet(
        string calldata _eventId,
        uint256 _amount,
        Team _team,
        uint8 _vipId
    ) external isBetting(_eventId) nonReentrant {
        require(_team != Team.NO, "Invalid team.");
        require(
            bets[msg.sender][_eventId].amount == 0,
            "You have already joined"
        );
        // require(block.timestamp < matches[_eventId].expired, "Overtime");
        // require(
        //     IERC20(token).balanceOf(msg.sender) >= _amount,
        //     "Not enough balance"
        // );

        (uint256 betAmount, uint256 fee) = calculateBetFee(_amount);
        uint256 premiumPool = ERC1155(vipNFT).checkVipRate(_vipId);
        uint256 vipBalance = ERC1155(vipNFT).balanceOf(msg.sender, _vipId);
        uint256 timeExpired = ERC1155(vipNFT).getTimeExpired(
            _vipId,
            msg.sender
        );

        if (_vipId != 6) {
            require(vipBalance > 0, "Not VIP");
            require(timeExpired >= block.timestamp, "VIP expired");
        }

        totalRate[_eventId][uint8(_team)] += premiumPool;
        bets[msg.sender][_eventId] = Betting(
            betAmount,
            Team(_team),
            premiumPool
        );
        pools[_eventId][uint8(_team)] += betAmount;

        IERC20(token).transferFrom(msg.sender, address(this), betAmount);
        IERC20(token).transferFrom(msg.sender, principle, fee);

        if (_amount > 50 ether) {
            uint256 rewardTicketAmount = _amount / 50 ether;
            ERC721A(ticketAddress).safeMintTo(msg.sender, rewardTicketAmount);
        }

        emit TicketBought(msg.sender, _eventId, _amount, uint8(_team)); //da tham gia bet
    }

    /**
     *@notice entry bet for a match
     * @dev require the bet is opened
     * @param _eventId id of match
     */
    function cancelBet(string calldata _eventId) external nonReentrant {
        require(
            bets[msg.sender][_eventId].amount > 0,
            "You haven't joined yet"
        );
        require(
            block.timestamp < matches[_eventId].expired,
            "Match is happening"
        );
        uint8 team = uint8(bets[msg.sender][_eventId].chosenTeam);
        uint256 amount = bets[msg.sender][_eventId].amount;
        pools[_eventId][uint8(team)] -= amount;
        uint256 premiumPool = bets[msg.sender][_eventId].premiumPool;
        totalRate[_eventId][team] -= premiumPool;

        delete bets[msg.sender][_eventId];

        IERC20(token).transfer(msg.sender, amount);

        emit TicketCanceled(msg.sender, _eventId, amount, team);
    }

    /**
     *@notice bettor claim refund money
     * @dev require match is canceled
     * @param _eventId id of match
     */
    function claimRefundBet(string calldata _eventId) external nonReentrant {
        require(uint256(matches[_eventId].status) == 3, "Invalid match");
        require(bets[msg.sender][_eventId].amount > 0, "No balance to claim");
        uint256 amount = bets[msg.sender][_eventId].amount;
        delete bets[msg.sender][_eventId];
        IERC20(token).transfer(msg.sender, amount);
    }

    /**
     *@notice bettor claim reward
     */
    function claimPrize(string calldata _eventId) external nonReentrant {
        require(
            matches[_eventId].winningTeam ==
                bets[msg.sender][_eventId].chosenTeam,
            "Cannot claim"
        );
        require(bets[msg.sender][_eventId].amount > 0, "Cannot claim");
        uint256 betAmount = bets[msg.sender][_eventId].amount;
        uint8 winner = uint8(matches[_eventId].winningTeam);
        Team loser = winner == uint256(Team.HOME) ? Team.AWAY : Team.HOME;
        uint256 prizeAmount = pools[_eventId][uint8(loser)] *
            (betAmount / pools[_eventId][winner]);
        uint256 premiumPool = matches[_eventId].rewardPool;
        uint256 bonusPrize = (premiumPool / totalRate[_eventId][winner]) *
            bets[msg.sender][_eventId].premiumPool;

        delete bets[msg.sender][_eventId];

        IERC20(token).transfer(
            msg.sender,
            prizeAmount + betAmount + bonusPrize
        );
    }

    /**
     * @notice View bettor's bet of match
     * @param _eventId id of match
     * @return data data of bettor's bet
     */
    function getUserBet(
        string calldata _eventId
    ) public view returns (Betting memory) {
        Betting memory betting = bets[msg.sender][_eventId];
        return betting;
    }

    /**
     * @notice View result of match
     * @param _eventId id of match
     * @return data result of a match
     */
    function getMatch(
        string calldata _eventId
    ) public view returns (Match memory) {
        Match memory resultMatch = matches[_eventId];
        return resultMatch;
    }

    /**
     * @notice View result of match
     * @param _eventId id of match
     * @return data each pool of match (pool home and pool away)
     */
    function getMatchPool(
        string calldata _eventId
    ) public view returns (uint256, uint256) {
        uint256 poolHome = pools[_eventId][uint8(Team.HOME)];
        uint256 poolAway = pools[_eventId][uint8(Team.AWAY)];
        return (poolHome, poolAway);
    }

    function getAmountWin(
        string calldata _eventId
    ) public view returns (uint256) {
        if (
            matches[_eventId].winningTeam ==
            bets[msg.sender][_eventId].chosenTeam
        ) {
            uint256 betAmount = bets[msg.sender][_eventId].amount;
            uint8 winner = uint8(matches[_eventId].winningTeam);
            Team loser = winner == uint8(Team.HOME) ? Team.AWAY : Team.HOME;
            uint256 prizeAmount = pools[_eventId][uint8(loser)] *
                (betAmount / pools[_eventId][winner]);
            uint256 premiumPool = matches[_eventId].rewardPool;
            uint256 bonusPrize = (premiumPool / totalRate[_eventId][winner]) *
                bets[msg.sender][_eventId].premiumPool;

            return betAmount + prizeAmount + bonusPrize;
        } else {
            return 0;
        }
    }

    function predictAmount(
        string calldata _eventId
    ) public view returns (uint256) {
        uint256 betAmount = bets[msg.sender][_eventId].amount;
        uint8 winner = uint8(bets[msg.sender][_eventId].chosenTeam);
        Team loser = winner == uint8(Team.HOME) ? Team.AWAY : Team.HOME;
        uint256 prizeAmount = pools[_eventId][uint8(loser)] *
            (betAmount / pools[_eventId][winner]);
        uint256 premiumPool = matches[_eventId].rewardPool;
        uint256 bonusPrize = (premiumPool / totalRate[_eventId][winner]) *
            bets[msg.sender][_eventId].premiumPool;

        return betAmount + prizeAmount + bonusPrize;
    }

    function getTotalRate(
        string calldata _eventId,
        uint8 _team
    ) external view returns (uint256) {
        return totalRate[_eventId][_team];
    }
}
