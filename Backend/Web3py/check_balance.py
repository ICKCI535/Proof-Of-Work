import logging
import asyncio
import time
from pancakeswap import PancakeSwap
from web3util import Web3Utility
from multiprocessing.dummy import Pool as ThreadPool
from multiprocessing import Lock

logging.basicConfig(format="%(asctime)s %(message)s",
                    level=logging.INFO, datefmt='[%Y-%m-%d %H:%M:%S]')

ps = PancakeSwap(test_mode=False)

token_to_buy = "0x24802247bd157d771b7effa205237d8e9269ba8a"

with open("links.txt", "r") as f:
    wallets = f.readlines()

sum_balance = 0.0


def main(account):
    address = account.split('|')[0]
    private_key = account.split('|')[1].replace('\n', '')
    balance = ps.web3.eth.getBalance(address)
    balance = ps.web3.fromWei(balance, 'ether')
    # w3util = Web3Utility(ps,  token_to_buy, private_key)
    # balance = w3util.get_token_balance(address)
    print(f"{address}|{balance}")
    with open("report.txt", "a") as z:
        z.write(f"{balance}\n")


print("Sum:", sum_balance)
if __name__ == "__main__":
    so_thread = int(input('Nhap so Thread muon chay: '))

    with open('accounts.txt', 'r') as f:
        accounts = f.readlines()
    lock = Lock()
    pool = ThreadPool(so_thread)
    pool.map(main, accounts)
