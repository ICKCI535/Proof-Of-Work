// SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;

import "@openzeppelin/contracts/token/ERC1155/ERC1155.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

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

contract VipTicket is ERC1155, Ownable, ReentrancyGuard {
    uint256 public constant VIP1 = 0;
    uint256 public constant VIP2 = 1;
    uint256 public constant VIP3 = 2;
    uint256 public constant VIP4 = 3;
    uint256 public constant VIP5 = 4;
    uint256 public constant VIP6 = 5;
    uint256 public unitPrice = 1 * 10 ** 18;
    address public token = 0x78867BbEeF44f2326bF8DDd1941a4439382EF2A7;
    string tokenUri = "";
    address public host = 0xE515BA407b97B053F89c4eecb8886F4C6101d4A3;

    mapping(uint8 => mapping(address => uint256)) public times;

    constructor() public ERC1155("") {}

    function provideVip(address _receiver, uint8 _tokenId) public nonReentrant {
        uint fee = checkVipPrice(_tokenId);
        // require(
        //     IERC20(token).balanceOf(msg.sender) >= fee,
        //     "Not enough balance"
        // );
        // IERC20(token).transferFrom(msg.sender, host, fee);
        _mint(_receiver, _tokenId, 1, "");
        times[_tokenId][msg.sender] = block.timestamp + 2592000;
    }

    function checkVipPrice(
        uint8 _tokenId
    ) internal view returns (uint256 _price) {
        if (_tokenId == 0) {
            uint price = unitPrice;
            return price;
        } else if (_tokenId == 1) {
            uint price = unitPrice * 2;
            return price;
        } else if (_tokenId == 2) {
            uint price = unitPrice * 3;
            return price;
        } else if (_tokenId == 3) {
            uint price = unitPrice * 4;
            return price;
        } else if (_tokenId == 4) {
            uint price = unitPrice * 5;
            return price;
        } else if (_tokenId == 5) {
            uint price = unitPrice * 6;
            return price;
        }
    }

    function checkVipRate(uint8 _tokenId) external view returns (uint256) {
        if (_tokenId == 0) {
            uint fee = 1100000000000000000;
            return fee;
        } else if (_tokenId == 1) {
            uint fee = 1200000000000000000;
            return fee;
        } else if (_tokenId == 2) {
            uint fee = 1300000000000000000;
            return fee;
        } else if (_tokenId == 3) {
            uint fee = 1400000000000000000;
            return fee;
        } else if (_tokenId == 4) {
            uint fee = 1500000000000000000;
            return fee;
        } else if (_tokenId == 5) {
            uint fee = 1600000000000000000;
            return fee;
        } else if (_tokenId == 6) {
            uint fee = 1000000000000000000;
            return fee;
        }
    }

    function changeVipPrice(uint256 _price) public onlyOwner {
        unitPrice = _price;
    }

    function setTokenUri(string calldata newUri) public onlyOwner {
        tokenUri = newUri;
    }

    function uri(uint256) public view virtual override returns (string memory) {
        return tokenUri;
    }

    function getTimeExpired(
        uint8 _id,
        address _sender
    ) external view returns (uint256) {
        uint time = times[_id][_sender];
        return time;
    }
}
