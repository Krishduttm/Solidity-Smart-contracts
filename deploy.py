from solcx import compile_standard
import json
from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()

with open("simple_storage.sol", "r") as file:
    simple_storage_file = file.read()

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"simple_storage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)


bytecode = compiled_sol["contracts"]["simple_storage.sol"]["simple_storage"]["evm"][
    "bytecode"
]["object"]

abi = compiled_sol["contracts"]["simple_storage.sol"]["simple_storage"]["abi"]

w3 = Web3(
    Web3.HTTPProvider(
        "https://eth-rinkeby.alchemyapi.io/v2/FkdcuVGhpLILTIzT-yw1eYvtbhjd5wIx"
    )
)

chain_id = 4

my_address = "0xaAF3578900e33db639A57E4910a6F8F56a333e19"

private_key = os.getenv("PRIVATE_KEY")
# creating the contract in python

simple_storage = w3.eth.contract(abi=abi, bytecode=bytecode)

# get the latest transaction

nonce = w3.eth.getTransactionCount(my_address)

# print(nonce)

# Three steps to do -
# 1)Build a transaction
# 2)Sign a transaction
# 3)Send a transaction

# 1)
print("deploying....")
transaction = simple_storage.constructor().buildTransaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce,
    }
)

# print(transaction)

# 2)
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

# print(signed_txn)

# 3)

txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)


txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)
print("deployed!!")
# Interacting with the contract

SimpleStorage = w3.eth.contract(address=txn_receipt.contractAddress, abi=abi)

transaction_1 = SimpleStorage.functions.AddPeople(123, "KC").buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce + 1,
    }
)
print("updating....")
sign_txn1 = w3.eth.account.sign_transaction(transaction_1, private_key=private_key)

txn1_hash = w3.eth.send_raw_transaction(sign_txn1.rawTransaction)

txn1_receipt = w3.eth.wait_for_transaction_receipt(txn1_hash)
print("updated!....")
print(SimpleStorage.functions.SeePeople("KC").call())
