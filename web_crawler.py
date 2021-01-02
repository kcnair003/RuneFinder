import requests
from bs4 import BeautifulSoup

URL = 'https://champion.gg/champion/Ahri/Middle'
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')
results = soup.find(id='blitz-app')
champion_runes = results.find_all('div', class_="View-sc-1c57lgy-1 cLLSJv View__StyledDiv-sc-1c57lgy-0 eidRwp")
for runes in champion_runes:
    images = runes.findAll('img')
    print(images)
#print(results.prettify())

#for runes in champion_runes:
#    print(runes, end='\n'*2)