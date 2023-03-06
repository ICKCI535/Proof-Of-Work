# https://github.com/CodeWithJoe2020/pancakeswapBot/blob/main/cakebot.py
# https://github.com/CodeWithJoe2020/pythonSniperbot/blob/main/sniper.py

import logging
import time
import json
from web3 import Web3


class PancakeSwap:
    def __init__(self,test_mode=False):        
        if not test_mode:
            bsc = "https://bsc-dataseed1.binance.org/"
            bsc_ws = "wss://old-morning-leaf.bsc.quiknode.pro/32542510b0df3c57d6439ad8c87c5ccdaf7b4cf4/"
            self.factory_address = "0xcA143Ce32Fe78f1f7019d7d551a6402fC5350c73"
            self.router_address = "0x10ed43c718714eb63d5aa57b78b54704e256024e"
            self.wrapped_bnb_address = "0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c"
            self.busd_contract = "0xe9e7cea3dedca5984780bafc599bd69add087d56"
            self.gas_price = 5
            self.gas_limit = 500000
            self.web3WS = Web3(Web3.WebsocketProvider(bsc_ws))
        else:
            logging.info("Testnet enabled")
            bsc = "https://data-seed-prebsc-1-s1.binance.org:8545"
            self.factory_address = "0x5fe5cc0122403f06abe2a75dbba1860edb762985"
            self.router_address = "0xCc7aDc94F3D80127849D2b41b6439b7CF1eB4Ae0"
            self.wrapped_bnb_address = "0x0de8fcae8421fc79b29ade9fff97854a424cad09"
            self.busd_contract = "0xe0dfffc2e01a7f051069649ad4eb3f518430b6a4"
            self.gas_price = 10
            self.gas_limit = 500000
            self.web3WS = ""
        self.web3 = Web3(Web3.HTTPProvider(bsc))
        if self.web3.isConnected():
            logging.info("Initiated Web3 object.")

        self.factory_abi = json.loads('[{"inputs":[{"internalType":"address","name":"_feeToSetter","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"token0","type":"address"},{"indexed":true,"internalType":"address","name":"token1","type":"address"},{"indexed":false,"internalType":"address","name":"pair","type":"address"},{"indexed":false,"internalType":"uint256","name":"","type":"uint256"}],"name":"PairCreated","type":"event"},{"constant":true,"inputs":[],"name":"INIT_CODE_PAIR_HASH","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"allPairs","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"allPairsLength","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"}],"name":"createPair","outputs":[{"internalType":"address","name":"pair","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"feeTo","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"feeToSetter","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"getPair","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_feeTo","type":"address"}],"name":"setFeeTo","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_feeToSetter","type":"address"}],"name":"setFeeToSetter","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]')
        self.router_abi = [{"inputs":[{"internalType":"address","name":"_factory","type":"address"},{"internalType":"address","name":"_WETH","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"WETH","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"amountADesired","type":"uint256"},{"internalType":"uint256","name":"amountBDesired","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"addLiquidity","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amountTokenDesired","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"addLiquidityETH","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"reserveIn","type":"uint256"},{"internalType":"uint256","name":"reserveOut","type":"uint256"}],"name":"getAmountIn","outputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"reserveIn","type":"uint256"},{"internalType":"uint256","name":"reserveOut","type":"uint256"}],"name":"getAmountOut","outputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsIn","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsOut","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"reserveA","type":"uint256"},{"internalType":"uint256","name":"reserveB","type":"uint256"}],"name":"quote","outputs":[{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidity","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidityETH","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidityETHSupportingFeeOnTransferTokens","outputs":[{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityETHWithPermit","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityETHWithPermitSupportingFeeOnTransferTokens","outputs":[{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityWithPermit","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapETHForExactTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactETHForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactETHForTokensSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForETH","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForETHSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokensSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMax","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapTokensForExactETH","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMax","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapTokensForExactTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"stateMutability":"payable","type":"receive"}]

        self.contract_factory = self.web3.eth.contract(address=self.web3.toChecksumAddress(self.factory_address), abi=self.factory_abi)
        self.contract_router = self.web3.eth.contract(address=self.web3.toChecksumAddress(self.router_address), abi=self.router_abi)    
        logging.info("Initiated Contract object.")
        
    def get_balance_eth(self,address):
        return self.web3.fromWei(self.web3.eth.get_balance(address), 'ether')

    def swap_exact_tokens_for_tokens(self, amount_in, from_contract_address, to_contract_address, sender_address, private_key, slip, method=None, count=0):
        amount_in = self.web3.toWei(amount_in, 'ether')
        sender_address = self.web3.toChecksumAddress(sender_address)
        from_contract_address = self.web3.toChecksumAddress(from_contract_address)
        to_contract_address = self.web3.toChecksumAddress(to_contract_address)
        wrapped_bnb_address = self.web3.toChecksumAddress(self.wrapped_bnb_address)

        bnb_price = self.get_amounts_out(amount=1, path=[self.web3.toChecksumAddress(self.wrapped_bnb_address), self.web3.toChecksumAddress(self.busd_contract)], index_result=1)
        bnb_price = float(bnb_price)

        if method == "sell":
            token_price = self.get_amounts_out(amount=1, path=[from_contract_address,wrapped_bnb_address,to_contract_address], index_result=2)
            token_price = float(token_price)
            slippage = float(amount_in) * token_price * slip
        else:
            token_price = self.get_amounts_out(amount=1, path=[to_contract_address,wrapped_bnb_address,from_contract_address], index_result=2)
            token_price = float(token_price)
            slippage = float(amount_in) / token_price * slip
        slippage = int(slippage)

        nonce = self.web3.eth.get_transaction_count(sender_address)
        build_transaction_data = {
            'from': sender_address,
            'gas': self.gas_limit,
            'gasPrice': self.web3.toWei(f'{self.gas_price}','gwei'),
            'nonce': nonce + count
        }
        pancakeswap2_txn = self.contract_router.functions.swapExactTokensForTokens(int(amount_in), slippage, [from_contract_address,wrapped_bnb_address,to_contract_address], sender_address, int(time.time()) + 10000).buildTransaction(build_transaction_data)
        signed_txn = self.web3.eth.account.sign_transaction(pancakeswap2_txn, private_key=private_key)
        tx_token = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return self.web3.toHex(tx_token)

    def swap_exact_tokens_for_eth(self, amount_in, from_contract_address, sender_address, private_key, slip, count=0):
        amount_in = self.web3.toWei(amount_in, 'ether')
        sender_address = self.web3.toChecksumAddress(sender_address)
        wrapped_bnb_address = self.web3.toChecksumAddress(self.wrapped_bnb_address)
        from_contract_address = self.web3.toChecksumAddress(from_contract_address)

        slippage = float(amount_in * self.get_current_price(from_contract_address)) * slip
        slippage = int(slippage)
 
        nonce = self.web3.eth.get_transaction_count(sender_address)
        build_transaction_data = {
            'from': sender_address,
            'gas': self.gas_limit,
            'gasPrice': self.web3.toWei(f'{self.gas_price}','gwei'),
            'nonce': nonce + count
        }
        pancakeswap2_txn = self.contract_router.functions.swapExactTokensForETH(amount_in, slippage, [from_contract_address,wrapped_bnb_address], sender_address, int(time.time()) + 10000).buildTransaction(build_transaction_data)
        signed_txn = self.web3.eth.account.sign_transaction(pancakeswap2_txn, private_key=private_key)
        tx_token = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return self.web3.toHex(tx_token)

    def swap_exact_eth_for_tokens(self, amount_in, to_contract_address, sender_address, private_key, slip, count=0):
        amount_in = self.web3.toWei(amount_in, 'ether')
        sender_address = self.web3.toChecksumAddress(sender_address)
        wrapped_bnb_address = self.web3.toChecksumAddress(self.wrapped_bnb_address)
        to_contract_address = self.web3.toChecksumAddress(to_contract_address)
        
        slippage = float(amount_in / self.get_current_price(to_contract_address)) * slip
        slippage = int(slippage)

        nonce = self.web3.eth.get_transaction_count(sender_address)
        build_transaction_data = {
            'from': sender_address,
            'value': amount_in,
            'gas': self.gas_limit,
            'gasPrice': self.web3.toWei(f'{self.gas_price}','gwei'),
            'nonce': nonce + count
        }
        pancakeswap2_txn = self.contract_router.functions.swapExactETHForTokens(slippage, [wrapped_bnb_address,to_contract_address], sender_address, int(time.time()) + 10000).buildTransaction(build_transaction_data)
        signed_txn = self.web3.eth.account.sign_transaction(pancakeswap2_txn, private_key=private_key)
        tx_token = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return self.web3.toHex(tx_token)

    def get_current_price(self, to_contract_address):
        amount_out = self.web3.toWei(1, 'ether')
        to_contract_address = self.web3.toChecksumAddress(to_contract_address)
        wrapped_bnb_address = self.web3.toChecksumAddress(self.wrapped_bnb_address)

        result = self.contract_router.functions.getAmountsIn(amount_out, [wrapped_bnb_address, to_contract_address]).call()
        return self.web3.fromWei(result[0], 'ether')

    def get_amounts_out(self, amount=1, to_contract_address=None, path=None, index_result = 0):
        amount_out = self.web3.toWei(amount, 'ether')
        if to_contract_address:
            to_contract_address = self.web3.toChecksumAddress(to_contract_address)
            wrapped_bnb_address = self.web3.toChecksumAddress(self.wrapped_bnb_address)
        if not path:
            path = [wrapped_bnb_address, to_contract_address]
        result = self.contract_router.functions.getAmountsOut(
            amount_out, path).call()
        return self.web3.fromWei(result[index_result], 'ether')