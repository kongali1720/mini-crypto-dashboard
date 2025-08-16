from web3 import Web3
from eth_account import Account

INFURA_URL = "https://infura.io/v3/YOUR_INFURA_PROJECT_ID"

w3 = Web3(Web3.HTTPProvider(INFURA_URL))

def simulate_eth_tx(sender_pk, receiver_address, amount_ether=0.01):
    sender_account = Account.from_key(sender_pk)
    nonce = w3.eth.get_transaction_count(sender_account.address)
    
    tx = {
        'nonce': nonce,
        'to': receiver_address,
        'value': w3.toWei(amount_ether, 'ether'),
        'gas': 21000,
        'gasPrice': w3.toWei('50', 'gwei')
    }
    
    signed_tx = w3.eth.account.sign_transaction(tx, sender_pk)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    print(f"Transaction sent! TX Hash: {w3.toHex(tx_hash)}")

if __name__ == "__main__":
    sender_pk = input("Sender Private Key: ")
    receiver = input("Receiver Address: ")
    amount = float(input("Amount in ETH: "))
    simulate_eth_tx(sender_pk, receiver, amount)
