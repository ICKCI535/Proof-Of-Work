// SPDX-License-Identifier: GPL-2.0-or-later
pragma solidity ^0.8.4;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "@openzeppelin/contracts/utils/math/SafeMath.sol";
import "./VRFv2Consumer.sol";

contract Lottery is Ownable {
    using SafeMath for uint256;
    using SafeERC20 for IERC20;

    address[] public players;
    address public currentWinner;
    mapping(address => uint256) public userTicketList;
    uint256 public ethFee = 0.001 ether;
    uint256 public usdcFee = 1 ether;
    uint256 public currentLotteryId = 0;
    uint256[] public currentRNG;

    enum LotteryStatus {
        OPEN,
        CLOSED,
        PENDING,
        CANCELED
    }

    LotteryStatus public lotteryStatus = LotteryStatus.CLOSED;
    VRFv2Consumer public vrf;

    constructor() {
        uint64 subscriptionId = 2607;
        vrf = new VRFv2Consumer(subscriptionId);
    }

    // Admin functions
    function startLottery() external onlyOwner {
        require(
            lotteryStatus == LotteryStatus.CLOSED ||
                lotteryStatus == LotteryStatus.CANCELED,
            "lotteryStatus is not CLOSED"
        );
        lotteryStatus = LotteryStatus.OPEN;
        // reset
        currentWinner = address(0);
        require(resetUserTicketList(), "Reset userTicketList failed");
        players = new address[](0);

        currentLotteryId++;
    }

    function endlottery() external onlyOwner {
        require(
            lotteryStatus == LotteryStatus.OPEN,
            "lotteryStatus is not OPEN"
        );
        lotteryStatus = LotteryStatus.CLOSED;
        require(pickWinner() != address(0), "Winner is not picked");
        currentWinner = pickWinner();
    }

    function cancelLottery() external onlyOwner {
        require(
            lotteryStatus == LotteryStatus.OPEN,
            "lotteryStatus is not OPEN"
        );
        lotteryStatus = LotteryStatus.CANCELED;
    }

    function getRandomNumber() external returns (uint256[] memory randomWords) {
        uint256 requestId = vrf.requestRandomWords();
        while (true) {
            (, randomWords) = vrf.getRequestStatus(requestId);
            if (randomWords.length > 0) {
                break;
            }
        }
        currentRNG = randomWords;
        return randomWords;
    }

    function pickWinner() private returns (address) {
        // currentWinner = winner here;
    }

    function refund() external {
        require(
            lotteryStatus == LotteryStatus.CLOSED,
            "lotteryStatus is not CANCELED"
        );
        require(userTicketList[msg.sender] != 0, "You are not in the list");
        uint256 amountToRefund = userTicketList[msg.sender] * ethFee;
        (bool success, ) = msg.sender.call{value: amountToRefund}("");
        require(success, "Refund failed");
        userTicketList[msg.sender] = 0;
    }

    function setEthFee(uint256 _ethFee) external onlyOwner {
        ethFee = _ethFee;
    }

    function setUsdcFee(uint256 _usdcFee) external onlyOwner {
        usdcFee = _usdcFee;
    }

    function resetUserTicketList() public onlyOwner returns (bool) {
        for (uint i = 0; i < players.length; i++) {
            userTicketList[players[i]] = 0;
        }
        return true;
    }

    // User functions
    function enterLotteryEth() external payable {
        require(
            lotteryStatus == LotteryStatus.OPEN,
            "lotteryStatus is not OPEN"
        );
        require(
            msg.sender.balance >= ethFee,
            "You don't have enough ETH to enter"
        );
        require(msg.value >= ethFee, "Enter lottery failed");
        players.push(msg.sender);
        userTicketList[msg.sender]++;
    }

    function claimLotteryEth(uint256 winningAmount) external {
        require(
            lotteryStatus == LotteryStatus.CLOSED,
            "lotteryStatus is not CLOSED"
        );
        (bool success, ) = msg.sender.call{value: winningAmount}("");
        require(success, "Claim prize failed");
    }
}
