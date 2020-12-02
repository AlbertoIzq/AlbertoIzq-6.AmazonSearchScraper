import requests
import time # To sleep script between page number retrieval attempts
from bs4 import BeautifulSoup
import pandas # To save it to csv file

def url_creation(item_search, page_nr):
    url_creator = []
    url_creator.append("https://www.amazon.es/s?k=")
    item_search = item_search.replace(" ", "+")
    url_creator.append(item_search)
    url_creator.append("&page=")
    url_creator.append(str(page_nr))
    url_creator.append("&__mk_es_ES=%C3%85M%C3%85%C5%BD%C3%95%C3%91&ref=sr_pg_")
    url_creator.append(str(page_nr))
    url = ""
    for s in url_creator:
        url = url + s
    return url

def retrieve_page_nr(item_search):
    attempts = 0
    attempts_max = 50
    page_nr = ""

    while True:
        try:
            url = url_creation(item_search, 1)
            r = requests.get(url, headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
            c = r.content
            soup = BeautifulSoup(c, "html.parser")
            all = soup.find_all("li", {"class": "a-disabled"})
            page_nr = all[-1].text
            page_nr = int(page_nr)
        except:
            print("Attempt", attempts, ". Couldn't get number of pages")
            attempts += 1
            time.sleep(2)
    
        if isinstance(page_nr, int):
            break
        elif attempts >= attempts_max:
            print("The script exceeded max number of attempts to retrieve number of pages from the webpage.",
                  "You are going to retrieve only results from page 1. Please execute script again...")
            page_nr = 1
            break

    return page_nr

# GET URL AND NUMBER OF PAGES
item_search = "guitarra eléctrica 7 cuerdas"
page_nr = retrieve_page_nr(item_search)
url = url_creation(item_search, 1)
#print(page_nr)
#print(url)

counter = 1
l = []

for page in range(1, page_nr + 1, 1):
    url = url_creation(item_search, page)
    print("CURRENT URL:", url)

    # RETRIEVE ITEM INFO FROM WEBPAGE
    r = requests.get(url, headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
    c = r.content
    #c
    soup = BeautifulSoup(c, "html.parser")
    #print(soup.prettify())
    all = soup.find_all("div", {"data-component-type": "s-search-result", "class": "s-result-item"})
    #print(len(all))

    for item in all:
        d = {}

        description = item.find_all("div", {"class": "a-section a-spacing-none a-spacing-top-small"})[0].find("span", {"class": "a-size-base-plus a-color-base a-text-normal"}).text
        d["Description"] = description
        print("___", counter, ": ", description)
   
        try:
            stars = item.find("span", {"class": "a-icon-alt"}).text.replace(" de 5 estrellas", "")
        except:
            stars = None
        d["Stars"] = stars
        print(stars, " stars")

        try:
            reviews = item.find_all("div", {"class": "a-section a-spacing-none a-spacing-top-micro"})[0].find("span", {"class": "a-size-base"}).text
        except:
            reviews = None
        d["Reviews"] = reviews
        print(reviews, " reviews")

        try:
            price = item.find_all("div", {"class": "a-section a-spacing-none a-spacing-top-small"})[1].find("span", {"class": "a-price-whole"}).text
        except:
            price = None
        d["Price"] = price
        print("price is ", price, " €")

        try:
            amazon_prime = item.find_all("div", {"class": "a-section a-spacing-none a-spacing-top-micro"})[1].find("i", {"class": "a-icon a-icon-prime a-icon-medium"})
            amazon_prime = "Yes"
            print("Amazon prime YES")
        except:
            amazon_prime = "No"
            print("NO Amazon prime")
        d["Amazon prime"] = amazon_prime

        try:
            best_seller = item.find("div", {"class": "a-section a-spacing-micro s-grid-status-badge-container"}).find_all("span", {"class": "a-badge-text"})[0]
            best_seller = "Yes"
            print("Best-seller YES")
        except:
            best_seller = "No"
            print("NO Best-seller")
        d["Best seller"] = best_seller

        counter = counter + 1

        l.append(d)

    print("PAGE", page, "PROCESSED!")

# SAVE INFO INTO CSV FILE
df = pandas.DataFrame(l)
df.to_csv("Output.csv")