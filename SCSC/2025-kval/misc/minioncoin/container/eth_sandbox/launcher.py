import json
import os
import random
import string
import time
import hashlib
from dataclasses import dataclass
from typing import Callable, Dict, List, Optional
from uuid import uuid4, UUID

import requests
from eth_account import Account
from web3 import Web3
from web3.exceptions import TransactionNotFound
from web3.types import TxReceipt
from .ticket import Challenge

from eth_sandbox import get_shared_secret

HTTP_PORT = os.getenv("HTTP_PORT", "8545")

CHALLENGE_ID = os.getenv("CHALLENGE_ID", "challenge")
FLAG = "SSM{placeholder}"
with open("/usr/lib/python/eth_sandbox/flag.txt", "r") as f:
    FLAG = f.read().strip()
POW_DIFFICULTY = int(os.getenv("POW_DIFFICULTY", "5000"))
CHALL_NAME = os.getenv("CHALL_NAME", "Challenge launcher")

Account.enable_unaudited_hdwallet_features()


@dataclass
class Action:
    name: str
    handler: Callable[[], int]


def sendTransaction(web3: Web3, tx: Dict) -> Optional[TxReceipt]:
    if "gas" not in tx:
        tx["gas"] = 15_000_000

    if "gasPrice" not in tx:
        tx["gasPrice"] = 0

    txhash = web3.eth.send_transaction(tx)

    while True:
        try:
            rcpt = web3.eth.get_transaction_receipt(txhash)
            break
        except TransactionNotFound:
            time.sleep(0.1)

    if rcpt.status != 1:
        raise Exception("failed to send transaction")

    return rcpt


def new_launch_instance_action(
    do_deploy: Callable[[Web3, str], str],
):
    def action() -> int:
        if POW_DIFFICULTY != 0:
            challenge = Challenge.generate_challenge(5000)
            print(f"curl -sSfL https://pwn.red/pow | sh -s {str(challenge)}")
            solution = input("Solution please: ")
            is_valid = challenge.check(solution)
            if not is_valid:
                print("Invalid solution!")
                return 1

        uuid = str(uuid4())

        data = requests.post(
            f"http://127.0.0.1:{HTTP_PORT}/new",
            headers={
                "Authorization": f"Bearer {get_shared_secret()}",
                "Content-Type": "application/json",
            },
            data=json.dumps(
                {
                    "uuid": uuid,
                }
            ),
        ).json()

        if data["ok"] == False:
            print(data["message"])
            return 1

        mnemonic = data["mnemonic"]

        deployer_acct = Account.from_mnemonic(
            mnemonic, account_path=f"m/44'/60'/0'/0/0"
        )
        player_acct = Account.from_mnemonic(mnemonic, account_path=f"m/44'/60'/0'/0/1")

        web3 = Web3(
            Web3.HTTPProvider(
                f"http://127.0.0.1:{HTTP_PORT}/{uuid}",
                request_kwargs={
                    "headers": {
                        "Authorization": f"Bearer {get_shared_secret()}",
                        "Content-Type": "application/json",
                    },
                },
            )
        )

        challenge_addr = do_deploy(web3, deployer_acct.address, player_acct.address)

        with open(f"/tmp/{uuid}", "w") as f:
            f.write(
                json.dumps(
                    {
                        "uuid": uuid,
                        "mnemonic": mnemonic,
                        "address": challenge_addr,
                    }
                )
            )

        print()
        print(f"Your private blockchain has been deployed")
        print(f"It will automatically terminate in 30 minutes")
        print(f"Make sure to replace [addr] with the challenge ip/hostname")
        print(f"Blockchain info:")
        print(f"UUID:               {uuid}")
        print(f"RPC endpoint:       http://[addr]:{HTTP_PORT}/{uuid}")
        print(f"Private key:        {player_acct.key.hex()}")
        print(f"Your address:       {player_acct.address}")
        print(f"Challenge contract: {challenge_addr}")
        return 0

    return Action(name="Launch new instance", handler=action)


def new_kill_instance_action():
    def action() -> int:
        uuid = check_uuid(input("UUID please: "))
        if not uuid:
            print("Invalid uuid!")
            return 1

        data = requests.post(
            f"http://127.0.0.1:{HTTP_PORT}/kill",
            headers={
                "Authorization": f"Bearer {get_shared_secret()}",
                "Content-Type": "application/json",
            },
            data=json.dumps(
                {
                    "uuid": uuid,
                }
            ),
        ).json()

        print()
        print(data["message"])
        return 1

    return Action(name="Kill instance", handler=action)


def is_solved_checker(web3: Web3, addr: str) -> bool:
    result = web3.eth.call(
        {
            "to": addr,
            "data": web3.keccak(text="isSolved()")[:4],
        }
    )
    return int(result.hex(), 16) == 1


def check_uuid(uuid) -> bool:
    try:
        UUID(uuid)
        return uuid
    except Exception:
        return None


def new_get_flag_action(
    checker: Callable[[Web3, str], bool] = is_solved_checker,
):
    def action() -> int:
        uuid = check_uuid(input("UUID please: "))
        if not uuid:
            print("Invalid UUID!")
            return 1

        try:
            with open(f"/tmp/{uuid}", "r") as f:
                data = json.loads(f.read())
        except:
            print("Bad UUID")
            return 1

        web3 = Web3(Web3.HTTPProvider(f"http://127.0.0.1:{HTTP_PORT}/{data['uuid']}"))

        print()

        try:
            solved = checker(web3, data["address"])
        except:
            print("Are you sure you solved it? Try again!")
            return 1

        if not solved:
            print("Are you sure you solved it? Try again!")
            return 1

        print("Here's the flag:", FLAG)
        print("Also please kill the instance if you are done :)")

        return 0

    return Action(name="Get flag", handler=action)


def run_launcher(actions: List[Action]):
    print(CHALL_NAME)
    for i, action in enumerate(actions):
        print(f"{i+1} - {action.name}")

    try:
        action = int(input("What do you want to do?\n> ")) - 1
    except:
        print("Nope!")
        exit(1)

    if action < 0 or action >= len(actions):
        print("Nope!")
        exit(1)

    exit(actions[action].handler())
