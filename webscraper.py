# required for HTML parsing
from bs4 import BeautifulSoup
# required for HTTP requests
import requests
import json
import ssl
import re

# Adding header
headers = {
    'authority': 'www.amazon.in',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'dnt': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-dest': 'document',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
}

# ignore SSL certificate errors
ssl._create_default_https_context = ssl._create_unverified_context

url_str = input("Enter the product category you want to search for: ")

words = url_str.split()
var = len(words)

if var == 1:
	url = "https://www.amazon.in/s/ref=nb_sb_noss_1?url=search-alias%3Daps&field-keywords=" + words[0]

if var == 2:
	url = "https://www.amazon.in/s/ref=nb_sb_noss_1?url=search-alias%3Daps&field-keywords=" + words[0] + "+" + words[1]

elif var == 3:
	url = "https://www.amazon.in/s/ref=nb_sb_noss_1?url=search-alias%3Daps&field-keywords=" + words[0] + "+" + words[1] + "+" + words[2]

response = requests.get(url, headers=headers)
content = BeautifulSoup(response.content, "html.parser")

productArr = []

# Check for sponsored containers
for product in content.findAll('div', attrs={"class":"sg-col-4-of-24 sg-col-4-of-12 sg-col-4-of-36 s-result-item s-asin sg-col-4-of-28 sg-col-4-of-16 AdHolder sg-col sg-col-4-of-20 sg-col-4-of-32"}):
    image = product.find('img', attrs={'src':re.compile('.jpg')})
    # Product name
    title = product.find('h2', attrs={"class": "a-size-mini a-spacing-none a-color-base s-line-clamp-4"})
    if title == None:
        title = product.find('span', attrs={"class": "a-size-medium a-color-base a-text-normal"})
        if title == None:
            title = product.find('h2', attrs={"class": "a-size-mini a-spacing-none a-color-base s-line-clamp-2"})
            name = title.text.strip()
        else:
            name = title.text.strip()
    else:
        name = title.text.strip()
    # Prices
    price_container = product.find('span', attrs={"class": "a-price-whole"})
    try:
        price = price_container.text
    except:
        price = "N/A"
    # Number of reviews
    num_review_container = product.find('span', attrs={"class": "a-size-base"})
    if (num_review_container != None):
        num_reviews = num_review_container.text
    else:
        num_reviews = "0"
    # Number of ratings
    ratings = product.find('span', attrs={'class':'a-icon-alt'})
    if ratings is not None:
            rating = ratings.text
    else:
        rating = '0'
    productObject = {
        "image-url": image['src'],
        "title": name,
        "price": price,
        "reviews": num_reviews,
        "ratings": rating,
    }

    # Saving the scraped data in json format
    productArr.append(productObject)

# Check for the most common style
for product in content.findAll('div', attrs={"class":"sg-col-4-of-24 sg-col-4-of-12 sg-col-4-of-36 s-result-item s-asin sg-col-4-of-28 sg-col-4-of-16 sg-col sg-col-4-of-20 sg-col-4-of-32"}):
    image = product.find('img', attrs={'src':re.compile('.jpg')})
    # Product names
    title = product.find('h2', attrs={"class": "a-size-mini a-spacing-none a-color-base s-line-clamp-4"})
    if title == None:
        title = product.find('span', attrs={"class": "a-size-medium a-color-base a-text-normal"})
        if title == None:
            title = product.find('h2', attrs={"class": "a-size-mini a-spacing-none a-color-base s-line-clamp-2"})
            name = title.text.strip()
        else:
            name = title.text.strip()
    else:
        name = title.text.strip()
    # Prices
    price_container = product.find('span', attrs={"class": "a-price-whole"})
    try:
        price = price_container.text
    except:
        price = "N/A"
    # Number of reviews
    num_review_container = product.find('span', attrs={"class": "a-size-base"})
    if (num_review_container != None):
        num_reviews = num_review_container.text
    else:
        num_reviews = "0"
    # Number of ratings    
    ratings = product.find('span', attrs={'class':'a-icon-alt'})
    if ratings is not None:
            rating = ratings.text
    else:
        rating = '0'
    productObject = {
        "image-url": image['src'],
        "title": name,
        "price": price,
        "reviews": num_reviews,
        "ratings": rating,
    }
    # Saving the scraped data in json format
    productArr.append(productObject)

# Check for special styles
for product in content.findAll('div', attrs={"class":"sg-col-20-of-24 s-result-item s-asin sg-col-0-of-12 sg-col-28-of-32 sg-col-16-of-20 AdHolder sg-col sg-col-32-of-36 sg-col-12-of-16 sg-col-24-of-28"}):
    image = product.find('img', attrs={'src':re.compile('.jpg')})
    # Product names
    title = product.find('h2', attrs={"class": "a-size-mini a-spacing-none a-color-base s-line-clamp-4"})
    if title == None:
        title = product.find('span', attrs={"class": "a-size-medium a-color-base a-text-normal"})
        if title == None:
            title = product.find('h2', attrs={"class": "a-size-mini a-spacing-none a-color-base s-line-clamp-2"})
            name = title.text.strip()
        else:
            name = title.text.strip()
    else:
        name = title.text.strip()
    # Prices
    price_container = product.find('span', attrs={"class": "a-price-whole"})
    try:
        price = price_container.text
    except:
        price = "N/A"
    # Number of reviews
    num_review_container = product.find('span', attrs={"class": "a-size-base"})
    if (num_review_container != None):
        num_reviews = num_review_container.text
    else:
        num_reviews = "0"
    # Number of ratings
    ratings = product.find('span', attrs={'class':'a-icon-alt'})
    if ratings is not None:
            rating = ratings.text
    else:
        rating = '0'
    productObject = {
        "image-url": image['src'],
        "title": name,
        "price": price,
        "reviews": num_reviews,
        "ratings": rating,
    }

    # Saving the scraped data in json format
    productArr.append(productObject)

# Check for special style
for product in content.findAll('div', attrs={"class":"sg-col-4-of-24 sg-col-4-of-12 sg-col-4-of-36 s-result-item s-asin sg-col-4-of-28 sg-col-4-of-16 AdHolder sg-col sg-col-4-of-20 sg-col-4-of-32"}):
    image = product.find('img', attrs={'src':re.compile('.jpg')})
    price_container = product.find('span', attrs={"class": "a-price-whole"})
    try:
        price = price_container.text
    except:
        price = "N/A"
    # Number of reviews
    num_review_container = product.find('span', attrs={"class": "a-size-base"})
    if (num_review_container != None):
        num_reviews = num_review_container.text
    else:
        num_reviews = "0"
    # Number of ratings
    ratings = product.find('span', attrs={'class':'a-icon-alt'})
    if ratings is not None:
            rating = ratings.text
    else:
        rating = '-1'
    productObject = {
        "image-url": image['src'],
        "title": name,
        "price": price,
        "reviews": num_reviews,
        "ratings": rating,
    }

    # Saving the scraped data in json format
    productArr.append(productObject)


with open('productData.json', 'w') as outfile:
    json.dump(productArr, outfile, indent=4)
    print ('----------Extraction of data is complete. Check json file.----------')  