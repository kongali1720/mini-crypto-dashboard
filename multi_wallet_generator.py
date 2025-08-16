import secrets
import hashlib

def generate_wallet():
    private_key = secrets.token_hex(32)
    public_key = hashlib.sha256(private_key.encode()).hexdigest()
    address = hashlib.sha256(public_key.encode()).hexdigest()[:34]
    return private_key, public_key, address

def generate_multiple_wallets(count=5):
    wallets = []
    for _ in range(count):
        wallets.append(generate_wallet())
    return wallets

if __name__ == "__main__":
    n = int(input("How many wallets to generate? "))
    all_wallets = generate_multiple_wallets(n)
    for idx, (pk, pub, addr) in enumerate(all_wallets, 1):
        print(f"\n=== Wallet #{idx} ===")
        print(f"Private Key: {pk}")
        print(f"Public Key : {pub}")
        print(f"Address    : {addr}")
