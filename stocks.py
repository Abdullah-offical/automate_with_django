from bs4 import BeautifulSoup
import requests


url = f"https://finance.yahoo.com/quote/AAPL"
response = requests.get(url)
    # print(response.content)
soup = BeautifulSoup(response.content, 'html.parser')
current_price = soup.find(f"fin-streamer", {"data-symbol": "AAPL"})['data-value']
print(current_price)
