# its python file not django 
from bs4 import BeautifulSoup
import requests

url = "https://webscraper.io/test-sites/tables"
response = requests.get(url)
# print(response.content)
soup = BeautifulSoup(response.content, 'html.parser')
# print(soup)
heading1 = soup.find_all('h1')
# print(heading1)
heading2 = soup.find_all('h2')
# print(heading2)
images = soup.find_all('img')
# print(images)
# print(images[0]['src'])
# print(images[0]['alt'])

table = soup.find_all('table')[1] # secound table of page
# print(table)
rows =  table.find_all('tr')[1:] # use python slice to exquope 1st hadding row start to 2nd
# print(row)
last_name = []
for row in rows:
    # print(row.find_all('td')[2])
    # print(row.find_all('td')[2].get_text())

    last_name.append(row.find_all('td')[2].get_text())

print(last_name)

