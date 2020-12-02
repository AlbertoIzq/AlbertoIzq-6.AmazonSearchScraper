import requests
from bs4 import BeautifulSoup

url = "https://www.amazon.es/s?k=guitarra+electrica&__mk_es_ES=%C3%85M%C3%85%C5%BD%C3%95%C3%91&ref=nb_sb_noss_2"
r = requests.get(url, headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
c = r.content
#c
soup = BeautifulSoup(c, "html.parser")
#print(soup.prettify())
all = soup.find_all("div", {"data-component-type": "s-search-result", "class": "s-result-item"})
#print(len(all))

#counter = 1

for item in all:
    description = item.find_all("div", {"class": "a-section a-spacing-none a-spacing-top-small"})[0].find("span", {"class": "a-size-base-plus a-color-base a-text-normal"}).text
    #print(counter, ": ",description)

    try:
        stars = item.find("span", {"class": "a-icon-alt"}).text.replace(" de 5 estrellas", "")
    except:
        stars = None
    
    print(stars)

    #counter = counter + 1
    