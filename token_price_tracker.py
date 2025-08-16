import requests

def get_price(tokens=["bitcoin", "ethereum"]):
    token_str = ",".join(tokens)
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={token_str}&vs_currencies=usd"
    data = requests.get(url).json()
    for token in tokens:
        print(f"{token.title()} Price: ${data[token]['usd']}")

if __name__ == "__main__":
    tokens = input("Enter token names (comma separated): ").lower().split(",")
    get_price([t.strip() for t in tokens])
