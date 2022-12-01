from web3 import Web3
import os
import json


class Web3Polygon(object):

    def __init__(self):
        # 钱包地址
        self.wallet = "xxxxx"
        # 钱包的私钥
        self.wallet_key = "xxxxx"
        self.rpc = "https://matic-mumbai.chainstacklabs.com"
        # 智能合约地址
        self.address = "xxxxx"
        self.web3 = Web3(Web3.HTTPProvider(self.rpc))
        self.world_cup_abi = self.get_file_api()
        # 创建与合约交互的对象，连接完通讯地址后，我们对这地址签订合同，合同里面有合约地址和接口规范（ABI）
        # web3.eth.contract(接口文档的合约地址, ABI接口规范)
        self.contract = self.web3.eth.contract(address=self.address, abi=self.world_cup_abi)  # 生成合约


    def get_file_api(self):
        # 获取ABI存放地址
        filePath = os.path.dirname(__file__) + '\ABI.json'
        # 读取abi合约接口
        with open(filePath, 'r') as f:
            world_cup_abi = json.load(f)

        return world_cup_abi

    def deal_web3_contract(self, amount=100, gas_price='20', gas_limit=7000000):
        params = {
            # 发送代币地址
            'from': self.wallet,
            # 接收代币的地址
            # 'to': self.address,

            # 代币数量，以wei为单位，可以是字符串和int类型 web3.toWei（数值，代币单位）
            # 为了方便调通代码，我们这里用wei来做单位，正常都是用ether。
            # 1 ether = 1 x 10^18wei = 1 x 10^9 Gwei

            # 'value': self.web3.toWei(amount, 'wei'),
            'value': 0,

            # 每个在链上可以执行的命令都设置了一个消耗的gas值，例：PUSH操作需要消耗3个gas，一次转账一般要消耗21000 gas，gas使用ether来支付
            # 1 ether = 1 x 10^18wei = 1 x 10^9 Gwei， 无论您执行的命令是成功还是失败，都需要支付计算费用
            # 简易理解：gas_limit 是一次交易中gas的可用上限
            'gas': gas_limit,

            # 通过gasPrice可以节省矿工费用，但也会减慢矿工打包的速度。因为，矿工会优先打包gas price设置高的交易，如果您想加快转账，您可以把gas price设置得更高，这样您就可以插队靠前
            # 一次转账一般要消耗21000 gas，如果你设置的gas Price = 1000000000wei = 1Gwei，则此次转账的交易手续费为：TxFee = 21000 Gwei = 0.000021 ether
            # A账户欲向B账户转账4 ether，则要求A账户至少要有 4 + 0.000021 = 4. 000021 ethrer
            # 简易理解：gasPrice就是你想用多少气费进行交易，为什么设置20，是因为当前市场价20就够了。如果你有钱，想更快也可以设置成25甚至更高
            'gasPrice': self.web3.toWei(gas_price, 'gwei'),

            # 'nonce': web3.eth.getTransactionCount(主钱包地址)，主要标记当前最新的交易号是多少，算是记录在交易队列中的位置
            'nonce': self.web3.eth.getTransactionCount(self.wallet),
        }

        contestId, gameplay, betTarget, bet_amount = 6, 1, 0, 9000000000000000000
        transaction_params = self.contract.functions.bet(contestId, gameplay, betTarget, bet_amount).buildTransaction(params)

        # web3.eth.account.signTransaction用账户对交易签名（转账需要的参数，from钱包地址的秘钥）
        signed_tx = self.web3.eth.account.signTransaction(transaction_params, private_key=self.wallet_key)
        # 交易发送并获取交易hash
        tx_hash = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        # bytes 转Txn Hash
        txn_hash = self.web3.toHex(tx_hash)
        print(txn_hash)

    def get_claim_info(self):
        params = {
            # 发送代币地址
            'from': self.wallet,
            # 接收代币的地址
            # 'to': self.address,
            'value': 0,
            'gas': 7000000,
            'gasPrice': self.web3.toWei(20, 'gwei'),
            'nonce': self.web3.eth.getTransactionCount(self.wallet),
        }
        contestId, gameplay = 5, 1
        transaction_params = self.contract.functions.claim(contestId, gameplay).buildTransaction(params)
        signed_tx = self.web3.eth.account.signTransaction(transaction_params, private_key=self.wallet_key)
        tx_hash = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        txn_hash = self.web3.toHex(tx_hash)
        print(txn_hash)


    def get_balance_info(self, address):
        # 获取当前gas的价格
        print("--gas--:", self.web3.eth.gasPrice)
        # 获取eth余额
        balance = self.web3.fromWei(self.web3.eth.getBalance(address), "ether")
        print("--balance--:", balance)
        return balance


if __name__ == '__main__':
    address = "xxxxx" # 0.17230937999962976
    web = Web3Polygon()
    # web.get_claim_info()
    web.get_balance_info(address)



