import requests
from PIL import Image
from io import BytesIO

def view_nft(metadata_url):
    data = requests.get(metadata_url).json()
    print("=== NFT Metadata ===")
    print(f"Name: {data.get('name')}")
    print(f"Description: {data.get('description')}")
    print(f"Image URL: {data.get('image')}")
    
    if data.get('image'):
        response = requests.get(data.get('image'))
        img = Image.open(BytesIO(response.content))
        img.show()

if __name__ == "__main__":
    url = input("NFT Metadata URL: ")
    view_nft(url)
