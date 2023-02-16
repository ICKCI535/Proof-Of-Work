//SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.4;

import "./access/Ownable.sol";

interface IERC20 {
    function transfer(address to, uint256 value) external returns (bool);

    function transferFrom(
        address from,
        address to,
        uint256 value
    ) external returns (bool);

    function balanceOf(address owner) external view returns (uint256 balance);
}

contract WrapTransactions is Ownable {
    event TransferFailed(address to, uint256 value);

    function scatterTokens(
        IERC20 token,
        address[] memory recipients,
        uint256[] memory values,
        bool revertOnfail
    ) external {
        uint256 totalSuccess = 0;
        uint256 totalTokens = 0;
        for (uint256 i = 0; i < values.length; i++) {
            totalTokens = totalTokens + values[i];
        }
        require(totalTokens <= token.balanceOf(msg.sender));
        for (uint256 i = 0; i < recipients.length; i++) {
            bool success = token.transferFrom(
                msg.sender,
                recipients[i],
                values[i]
            );

            if (!success) {
                // bool decoded = abi.decode(returnData, (bool));
                require(revertOnfail, "One of the transfers failed");
                emit TransferFailed(recipients[i], values[i]);
            } else {
                totalSuccess++;
            }
        }

        require(totalSuccess >= 1, "all transfers failed");
    }

    function scatterEthers(
        address[] memory recipients,
        uint256[] memory values,
        bool revertOnfail
    ) external payable {
        uint256 totalSuccess = 0;
        uint256 totalTokens = 0;
        for (uint256 i = 0; i < values.length; i++) {
            totalTokens = totalTokens + values[i];
        }
        require(totalTokens <= msg.value, "not enough balance");
        for (uint256 i = 0; i < recipients.length; i++) {
            (bool success, ) = recipients[i].call{
                value: values[i],
                gas: 300000
            }("");

            if (!success) {
                require(revertOnfail, "One of the transfers failed");
                emit TransferFailed(recipients[i], values[i]);
            } else {
                totalSuccess++;
            }
        }

        require(totalSuccess >= 1, "all transfers failed");
    }
}
