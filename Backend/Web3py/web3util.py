import json
import os

class Web3Utility:
    def __init__(self, ps=None, token_to_buy=None, private_key=None):
        self.get_token_to_buy = token_to_buy
        self.private_key = private_key
        self.ps = ps
        current_path = os.path.dirname(os.path.realpath(__file__))
        with open(f"{current_path}/abi.txt", "r") as f:
            abi = json.loads(f.read())
        if token_to_buy:
            self.contract = self.ps.web3.eth.contract(address=self.ps.web3.toChecksumAddress(token_to_buy), abi=abi)

    def get_eth_balance(self, address):
        address = self.ps.web3.toChecksumAddress(address)
        bnb_balance = self.ps.web3.eth.getBalance(address)
        bnb_balance = self.ps.web3.fromWei(bnb_balance, 'ether')
        return bnb_balance

    def get_token_balance(self, address):
        token_balance = self.contract.functions.balanceOf(
            self.ps.web3.toChecksumAddress(address)).call()
        return self.ps.web3.fromWei(token_balance, 'ether')

    def estimateGas(self, txn):
        gas = self.ps.web3.eth.estimateGas({
            "from": txn['from'],
            "to": txn['to'],
            "value": txn['value'],
            "data": txn['data']
        })
        gas = gas + (gas / 10)  # Adding 1/10 from gas to gas!
        return gas

    def is_approve(self, address):
        Approve = self.contract.functions.allowance(
            address, self.ps.web3.toChecksumAddress(self.ps.router_address)).call()
        Aproved_quantity = self.contract.functions.balanceOf(address).call()
        if int(Approve) <= int(Aproved_quantity):
            return False
        else:
            return True

    def approve(self, address):
        address = self.ps.web3.toChecksumAddress(address)
        if not self.is_approve(address):
            txn = self.contract.functions.approve(self.ps.web3.toChecksumAddress(self.ps.router_address), self.ps.web3.toWei(100000, 'ether')).buildTransaction({
                'from': address,
                'gas': self.ps.gas_limit,
                'gasPrice': self.ps.web3.toWei(f'{self.ps.gas_price}', 'gwei'),
                'nonce': self.ps.web3.eth.getTransactionCount(address),
                'value': 0
            })
            txn.update({'gas': int(self.estimateGas(txn))})
            signed_txn = self.ps.web3.eth.account.sign_transaction(
                txn, private_key=self.private_key)
            tx_token = self.ps.web3.eth.send_raw_transaction(
                signed_txn.rawTransaction)
            txn_receipt = self.ps.web3.eth.waitForTransactionReceipt(tx_token)
            # print(txn_receipt)
            if txn_receipt["status"] == 1:
                print("Approved")
                return True
            else:
                return False
        else:
            print("Already approved.")
            return True

    def send_token(self, sender_address, to_address, value):
        sender_address = self.ps.web3.toChecksumAddress(sender_address)
        to_address = self.ps.web3.toChecksumAddress(to_address)
        value = self.ps.web3.toWei(value, 'ether')
        nonce = self.ps.web3.eth.get_transaction_count(sender_address)
        build_transaction_data = {
            'from': sender_address,
            'gas': self.ps.gas_limit,
            'gasPrice': self.ps.web3.toWei(f'{self.ps.gas_price}','gwei'),
            'nonce': nonce
        }
        txn = self.contract.functions.transfer(to_address, value).buildTransaction(build_transaction_data)
        signed_txn = self.ps.web3.eth.account.sign_transaction(txn, private_key=self.private_key)
        tx_hash = self.ps.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return self.ps.web3.toHex(tx_hash)

    def send_bnb(self, sender_address, to_address, value):
        sender_address = self.ps.web3.toChecksumAddress(sender_address)
        to_address = self.ps.web3.toChecksumAddress(to_address)
        value = self.ps.web3.toWei(value, 'ether')
        nonce = self.ps.web3.eth.get_transaction_count(sender_address)
        build_transaction_data = {
            'chainId': 56,
            'to': to_address,
            'value': value,
            'gas': self.ps.gas_limit,
            'gasPrice': self.ps.web3.toWei(f'{self.ps.gas_price}','gwei'),
            'nonce': nonce
        }
        print(build_transaction_data)
        txn = build_transaction_data
        signed_txn = self.ps.web3.eth.account.sign_transaction(txn, private_key=self.private_key)
        tx_hash = self.ps.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return self.ps.web3.toHex(tx_hash)