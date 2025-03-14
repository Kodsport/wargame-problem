// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.25;

import "./Coin.sol";

contract Challenge {
    address public player = address(0);
    MinionCoin public coin;

    mapping(address => uint256) public balance;

    constructor() payable {
        coin = new MinionCoin(100000);
    }

    function hello() public {
        require(player == address(0), "Player already set");
        player = msg.sender;
    }

    function buyCoin(uint256 amount) public {
        uint256 cost = amount * 1 ether;
        require(balance[msg.sender] >= cost, "Insufficient funds");

        balance[msg.sender] -= cost;
        bool result = coin.transfer(msg.sender, amount);
        require(result, "Transfer failed");
    }

    function deposit() external payable {
        balance[msg.sender] += msg.value;
    }

    function withdraw() external {
        uint256 amount = balance[msg.sender];
        require(amount > 0, "No funds to withdraw");

        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Transfer failed");

        balance[msg.sender] = 0;
    }

    // Must return true to get flag
    function isSolved() public view returns (bool) {
        require(player != address(0), "Player not set");
        return coin.coinsOf(player) >= 1000;
    }
}
