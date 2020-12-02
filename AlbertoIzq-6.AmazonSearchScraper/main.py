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

counter = 1

for item in all:
    description = item.find_all("div", {"class": "a-section a-spacing-none a-spacing-top-small"})[0].find("span", {"class": "a-size-base-plus a-color-base a-text-normal"}).text
    print("___", counter, ": ", description)

    try:
        stars = item.find("span", {"class": "a-icon-alt"}).text.replace(" de 5 estrellas", "")
    except:
        stars = None
    print(stars, " stars")

    try:
        reviews = item.find_all("div", {"class": "a-section a-spacing-none a-spacing-top-micro"})[0].find("span", {"class": "a-size-base"}).text
    except:
        reviews = None
    print(reviews, " reviews")

    try:
        price = item.find_all("div", {"class": "a-section a-spacing-none a-spacing-top-small"})[1].find("span", {"class": "a-price-whole"}).text
    except:
        price = None
    print("price is ", price, " €")

    try:
        amazon_prime = item.find_all("div", {"class": "a-section a-spacing-none a-spacing-top-micro"})[1].find("i", {"class": "a-icon a-icon-prime a-icon-medium"})
        amazon_prime = "Yes"
        print("AMAZON PRIME YES")
    except:
        amazon_prime = "No"
        print("NO")

    try:
        best_seller = item.find("div", {"class": "a-section a-spacing-micro s-grid-status-badge-container"}).find_all("span", {"class": "a-badge-text"})[0]
        best_seller = "Yes"
        print("Más vendido")
    except:
        best_seller = "No"
        print("NO")

    counter = counter + 1
    