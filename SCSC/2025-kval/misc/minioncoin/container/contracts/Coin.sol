// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.25;

contract MinionCoin {
    string public constant name = "MinionCoin";
    string public constant symbol = "MINION";
    uint8 public constant decimals = 18;

    mapping(address => uint256) public coinsOf;
    uint256 public totalSupply;

    constructor(uint256 initialSupply) {
        totalSupply = initialSupply * (10 ** decimals);
        coinsOf[msg.sender] = totalSupply;
    }

    function transfer(address to, uint256 amount) public returns (bool) {
        require(to != address(0), "Invalid address");
        require(coinsOf[msg.sender] >= amount, "Insufficient balance");

        coinsOf[msg.sender] -= amount;
        coinsOf[to] += amount;

        return true;
    }
}
