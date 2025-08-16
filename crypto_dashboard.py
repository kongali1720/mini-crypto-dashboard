import tkinter as tk
from tkinter import ttk, messagebox
import secrets
import hashlib
import requests
from web3 import Web3
from eth_account import Account

# ===========================
# Blockchain / Crypto Setup
# ===========================
INFURA_URL = "https://goerli.infura.io/v3/YOUR_INFURA_PROJECT_ID"
w3 = Web3(Web3.HTTPProvider(INFURA_URL))

# ===========================
# Functions
# ===========================
def generate_wallet():
    private_key = secrets.token_hex(32)
    public_key = hashlib.sha256(private_key.encode()).hexdigest()
    address = hashlib.sha256(public_key.encode()).hexdigest()[:34]
    return private_key, public_key, address

def multi_wallets(count=5):
    wallets = [generate_wallet() for _ in range(count)]
    return wallets

def simulate_eth_tx(sender_pk, receiver_addr, amount):
    try:
        sender_account = Account.from_key(sender_pk)
        nonce = w3.eth.get_transaction_count(sender_account.address)
        tx = {
            'nonce': nonce,
            'to': receiver_addr,
            'value': w3.toWei(amount, 'ether'),
            'gas': 21000,
            'gasPrice': w3.toWei('50', 'gwei')
        }
        signed_tx = w3.eth.account.sign_transaction(tx, sender_pk)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        return w3.toHex(tx_hash)
    except Exception as e:
        return f"Error: {str(e)}"

def get_token_price(tokens):
    token_str = ",".join(tokens)
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={token_str}&vs_currencies=usd"
    data = requests.get(url).json()
    return {token: data[token]['usd'] for token in tokens if token in data}

# ===========================
# GUI Setup
# ===========================
root = tk.Tk()
root.title("🪙 Mini Crypto Dashboard")
root.geometry("700x600")
root.configure(bg="#0a0a0a")

style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", foreground="white", background="#1f1f1f", font=("Arial", 10))
style.configure("TLabel", foreground="white", background="#0a0a0a", font=("Arial", 10))
style.configure("TEntry", foreground="black", background="white", font=("Arial", 10))

# ---------------------------
# Wallet Generator
# ---------------------------
def wallet_action():
    try:
        n = int(wallet_count_entry.get())
    except:
        n = 1
    wallets = multi_wallets(n)
    wallet_text.delete("1.0", tk.END)
    for idx, (pk, pub, addr) in enumerate(wallets, 1):
        wallet_text.insert(tk.END, f"=== Wallet #{idx} ===\nPrivate Key: {pk}\nPublic Key: {pub}\nAddress: {addr}\n\n")

tk.Label(root, text="Generate Wallets", font=("Arial", 12, "bold")).pack(pady=5)
wallet_count_entry = ttk.Entry(root)
wallet_count_entry.pack()
wallet_count_entry.insert(0, "1")
ttk.Button(root, text="Generate", command=wallet_action).pack(pady=5)
wallet_text = tk.Text(root, height=10, bg="#1c1c1c", fg="#39ff14")
wallet_text.pack(fill=tk.BOTH, padx=10, pady=5)

# ---------------------------
# ETH Transaction Simulator
# ---------------------------
def send_tx_action():
    sender = sender_entry.get()
    receiver = receiver_entry.get()
    try:
        amount = float(amount_entry.get())
    except:
        messagebox.showerror("Error", "Amount must be a number!")
        return
    tx_hash = simulate_eth_tx(sender, receiver, amount)
    tx_text.delete("1.0", tk.END)
    tx_text.insert(tk.END, f"Transaction Result:\n{tx_hash}")

tk.Label(root, text="ETH Testnet Transaction Simulator", font=("Arial", 12, "bold")).pack(pady=5)
sender_entry = ttk.Entry(root)
sender_entry.pack(pady=2)
sender_entry.insert(0, "Sender Private Key")
receiver_entry = ttk.Entry(root)
receiver_entry.pack(pady=2)
receiver_entry.insert(0, "Receiver Address")
amount_entry = ttk.Entry(root)
amount_entry.pack(pady=2)
amount_entry.insert(0, "0.01")
ttk.Button(root, text="Send Transaction", command=send_tx_action).pack(pady=5)
tx_text = tk.Text(root, height=5, bg="#1c1c1c", fg="#39ff14")
tx_text.pack(fill=tk.BOTH, padx=10, pady=5)

# ---------------------------
# Token Price Tracker
# ---------------------------
def track_price_action():
    tokens = token_entry.get().lower().split(",")
    prices = get_token_price([t.strip() for t in tokens])
    price_text.delete("1.0", tk.END)
    for token, price in prices.items():
        price_text.insert(tk.END, f"{token.title()}: ${price}\n")

tk.Label(root, text="Token Price Tracker (Coingecko)", font=("Arial", 12, "bold")).pack(pady=5)
token_entry = ttk.Entry(root)
token_entry.pack(pady=2)
token_entry.insert(0, "bitcoin, ethereum")
ttk.Button(root, text="Get Prices", command=track_price_action).pack(pady=5)
price_text = tk.Text(root, height=5, bg="#1c1c1c", fg="#39ff14")
price_text.pack(fill=tk.BOTH, padx=10, pady=5)

# ===========================
# Run App
# ===========================
root.mainloop()
