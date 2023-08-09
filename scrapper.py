import requests
from bs4 import BeautifulSoup

querys = ["pollo"]

url_lists = [
    f"https://www.jumbo.cl/busqueda?ft={querys[0]}"
]

url = url_lists[0]

page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")

results = soup.find_all("div", class_="shelf-content")

for r in results:
    print(r, end="\n"*2)
