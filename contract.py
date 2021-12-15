import time
import json
import web3
from eth_account import Account
from web3.auto import w3
from web3.providers.websocket import WebsocketProvider
from web3 import Web3
from solc import compile_standard

with open("Token.sol") as c:
 contractText=c.read()
with open(".pk") as pkfile:
 privateKey=pkfile.read()
with open(".infura") as infurafile:
 infuraKey=infurafile.read()

compiled_sol = compile_standard({
 "language": "Solidity",
 "sources": {
  "THAtoken.sol": {
   "content": contractText
  }
 },
 "settings":
 {
  "outputSelection": {
   "*": {
    "*": [
     "metadata", "evm.bytecode"
     , "evm.bytecode.sourceMap"
    ]
   }
  }
 }
})
bytecode = compiled_sol['contracts']['THAtoken.sol']['THAtoken']['evm']['bytecode']['object']
abi = json.loads(compiled_sol['contracts']['THAtoken.sol']['THAtoken']['metadata'])['output']['abi']
W3 = Web3(WebsocketProvider('wss://ropsten.infura.io/ws/v3/%s'%infuraKey))
account1=Account.from_key(privateKey);
address1=account1.address

greeter = W3.eth.contract(
  address= "0xc3ed846BE808280db0DfffEb6f13E23a74cdea92",
  abi=abi
)


print("Output from balanceOf()")
print(greeter.functions.balanceOf("0x77bf401b369Ce1383900dFa004A558D7CeF8B615").call())
      
nonce = W3.eth.getTransactionCount("0xF2FAE8e32a632b1377Aaf0f7B76f9bA41a6faE3C")
tx_dict = greeter.functions.transfer("0x77bf401b369Ce1383900dFa004A558D7CeF8B615", 250).buildTransaction({
  'chainId': 3,
  'gas': 1400000,
  'gasPrice': w3.toWei('40', 'gwei'),
  'nonce': nonce,
  'from':address1
})

signed_txn = W3.eth.account.sign_transaction(tx_dict, private_key=privateKey)
result = W3.eth.sendRawTransaction(signed_txn.rawTransaction)
tx_receipt = None#W3.eth.getTransactionReceipt(result)

count = 0
while tx_receipt is None and (count < 300):
  time.sleep(1)
  try:
    tx_receipt = W3.eth.getTransactionReceipt(result)
  except:
    print('.')

if tx_receipt is None:
  print (" {'status': 'failed', 'error': 'timeout'} ")

#tx_hash = greeter.functions.setGreeting('Nihao').transact({"from":account1.address})
#tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
print("Output from balanceOf()")
print(greeter.functions.balanceOf("0x77bf401b369Ce1383900dFa004A558D7CeF8B615").call())
