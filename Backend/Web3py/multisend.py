from web3 import Web3
from multiprocessing.dummy import Pool as ThreadPool
from multiprocessing import Lock


def main(account):
    address = account.split('|')[0]
    private_key = account.split('|')[1].replace('\n', '')
    web3 = Web3(Web3.HTTPProvider(
        'https://bsc-dataseed2.binance.org'))
    account_1 = web3.toChecksumAddress(address)
    private_key1 = private_key
    receiver = web3.toChecksumAddress(
        '0xcC2d7E93C2B2eE0d5273Ec91ff9AB814Ce85d577')

    # get the nonce.  Prevents one from sending the transaction twice
    nonce = web3.eth.getTransactionCount(account_1)
    val = web3.eth.getBalance(account_1)
    if val > 0.004:
        total_gas = int(web3.toWei("50", "gwei") * 21000)
        # build a transaction in a dictionary
        tx = {
            'nonce': nonce,
            'to': receiver,
            "value": val - total_gas,
            'gas': 21000,
            'gasPrice': web3.toWei('50', 'gwei')
        }

        # sign the transaction
        signed_tx = web3.eth.account.sign_transaction(tx, private_key1)

        # send transaction
        tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        while True:
            try:
                status = web3.eth.get_transaction_receipt(tx_hash)
                break
            except:
                continue
        print(status)

    # get transaction hash
        print(web3.toHex(tx_hash))


# with open('abi.txt', 'r') as r:
#     wallets = r.readlines()
# for wallet in wallets:
#     address = wallet.split('|')[0]
#     private_key = wallet.split('|')[1].replace('\n', '')
#     main(address, private_key)
if __name__ == "__main__":
    so_thread = int(input('Nhap so Thread muon chay: '))

    with open('acc_result.txt', 'r') as f:
        accounts = f.readlines()
    lock = Lock()
    pool = ThreadPool(so_thread)
    pool.map(main, accounts)
