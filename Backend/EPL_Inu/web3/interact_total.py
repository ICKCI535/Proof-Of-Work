from re import A
from web3 import Web3, HTTPProvider, WebsocketProvider
from web3.contract import Contract
import json
from datetime import datetime
import requests
GAS = 300000


def get_web3(rpc, is_ws=False) -> Web3:
    return Web3(WebsocketProvider(rpc)) if is_ws else Web3(HTTPProvider(rpc))


def get_contract(web3: Web3, address, abi) -> Contract:
    return web3.eth.contract(address=web3.toChecksumAddress(address), abi=abi)


async def choose_winner(web3: Web3, contract: Contract, match_id: int, winner: int, caller_pk: str, caller_address: str):
    txn = contract.functions.chooseWinner(match_id, winner).buildTransaction(
        {
            "from": caller_address,
            "gas": GAS,
            "gasPrice": web3.eth.gas_price,
            "nonce": web3.eth.get_transaction_count(caller_address) + 1,
        }
    )

    signed_txn = web3.eth.account.sign_transaction(txn, private_key=caller_pk)

    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

    print(Web3.toHex(tx_hash))
    web3.eth.waitForTransactionReceipt(Web3.toHex(tx_hash), timeout=120)


def exec_transaction(web3: Web3, contract: Contract, txn,  caller_pk: str, caller_address: str):

    signed_txn = web3.eth.account.sign_transaction(txn, private_key=caller_pk)

    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

    print(Web3.toHex(tx_hash))
    web3.eth.waitForTransactionReceipt(Web3.toHex(tx_hash), timeout=120)


def choose_winner(web3: Web3, contract: Contract, caller_pk: str, caller_address: str):
    with open('./scripts/python/selenium_get_data/results.txt') as r:
        data = r.readlines()
    nonce = web3.eth.get_transaction_count(caller_address)
    for line in data:
        home = int(line.split('|')[2].split(' - ')[0])
        away = int(line.split('|')[2].split(' - ')[1])
        match_id = int(line.split('|')[4])

        txn = contract.functions.chooseWinner(match_id, home, away).buildTransaction(
            {
                "from": caller_address,
                "gas": 300000,
                "gasPrice": web3.eth.gas_price,
                "nonce": nonce,
            }
        )
        exec_transaction(web3, contract, txn, caller_pk, caller_address)
        nonce += 1


def get_latest_id(web3: Web3, contract: Contract, caller_pk: str, caller_address: str):
    a = contract.functions.getLatestEventId().call()
    b = contract.functions.decodeByte(a).call()
    return b


def request_game_created(date):
    event_ids = []
    event_dates = []
    point_spread_homes = []
    event_statuses = []
    reward_pools = []
    total_overs = []
    with open('./scripts/Python/therundown/result.json', 'r') as r:
        matches = r.read()
        matches = json.loads(matches)
    for data in matches['data']:
        print(data)
        event_ids.append(data['event_id'])
        event_statuses.append(data['event_status'])
        event_dates.append(data['event_date'])
        reward_pools.append(100000000000000000)
        if float(data['point_spread_home']) < 0:
            data['point_spread_home'] = str(data['point_spread_home'])[1:]
            data['point_spread_home'] = web3.toWei(
                float(data['point_spread_home']), 'ether')
            point_spread_homes.append(int(-data['point_spread_home']))
        else:
            data['point_spread_home'] = web3.toWei(
                float(data['point_spread_home']), 'ether')
            point_spread_homes.append(int(data['point_spread_home']))
        total_overs.append(int(float(data['total_over'])*10**18))
    return {'event_ids': event_ids, 'event_dates': event_dates, 'event_statuses': event_statuses, 'point_spread_homes': point_spread_homes, 'total_overs': total_overs, "reward_pools": reward_pools}


def start_match_bet(expired, ou, event_id, reward_pool, web3: Web3, contract: Contract, caller_pk: str, caller_address: str):
    nonce = web3.eth.get_transaction_count(caller_address)
    txn = contract.functions.startMatchBet(expired, ou, event_id, reward_pool).buildTransaction(
        {
            "from": caller_address,
            "gas": 1000000,
            "gasPrice": web3.eth.gas_price,
            "nonce": nonce,
        }
    )
    exec_transaction(web3, contract, txn, caller_pk, caller_address)
    nonce += 1


def to_timestamp(date: datetime):
    return int(date.timestamp())


if __name__ == "__main__":
    address = Web3.toChecksumAddress(
        "0x6559d096Bd0b1d4d26D71B008f6421843E4CB048")
    rpc = "https://goerli.infura.io/v3/79687f15952340e9b3d5601a12e3bbaf"

    caller_pk = ""
    caller_address = Web3.toChecksumAddress(
        "0xE515BA407b97B053F89c4eecb8886F4C6101d4A3")
    web3 = get_web3(rpc, is_ws=False)
    print(web3.isConnected())

    abi = []
    with open("./scripts/abi.json", "r") as f:
        abi = json.loads(f.read())

    contract = get_contract(web3, address, abi)
    schedule = request_game_created("2022-10-23")
    print(schedule)
    start_match_bet(expired=schedule['event_dates'], ou=schedule['total_overs'], event_id=schedule['event_ids'], reward_pool=schedule['reward_pools'], web3=web3, contract=contract,
                    caller_pk=caller_pk, caller_address=caller_address)
# choose_winner(web3=web3, contract=contract,
#               caller_pk=caller_pk, caller_address=caller_address)
# print(to_timestamp(datetime(2022, 12, 22, 12, 30, 40)))
