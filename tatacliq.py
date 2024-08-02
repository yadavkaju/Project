import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import csv
import time
from datetime import datetime

PDP_List = []

headers = {
    'accept': 'application/json',
    'content-type': 'application/x-www-form-urlencoded',
}

df = pd.read_excel("Sample Listing IDs and PDP Links.xlsx")

for i, row in df.iterrows():
    product_url = row['PDP Links']

params = {
    'url': product_url
}

response = requests.post(
    'http://43.205.6.219:8000/internalrequirement/tatacliq/productdetailpage',
    params=params,
    headers=headers,
)

json_data = json.loads(response.text)

try:
    title = json_data['title']
except:
    title = ''

try:
    brand = json_data['brand']
except:
    brand = ""

try:
    PDP_status = json_data['pdp_status']
except:
    PDP_status = ""

try:
    unique_id = json_data['unique_id']['productListingId']
except:
    unique_id = ""

try:
    varient = json_data['variant']['varation detail']
except:
    varient = ""

try:
    description = json_data['description']
except:
    description = ""

try:
    PDP_url = json_data['url']
except:
    PDP_url = ''

try:
    colour = json_data['attributes']['productColor']
except:
    colour = ''

try:
    listed_sizes_status = json_data['availability']['listed_sizes_status']
except:
    listed_sizes_status = ''
try:
    size_guide_availability = json_data['availability']['size_guide_availability']
except:
    size_guide_availability = ''
try:
    sold_by_info = json_data['Seller_details']['sold_by_info']
except:
    sold_by_info = ''

try:
    season = json_data['extras']['season']
except:
    season = ''
try:
    discount = json_data['price']['discount']
except:
    discount = ''
try:
    buy_now = json_data['availability']['buy_now_status']
except:
    buy_now = ''

current_date = datetime.now().date()

PDP_dict = {
    'Date' : current_date,
    'PDP URL' : PDP_url,
    'PDP status': PDP_status,
    'Title': title,
    'Brand Name': brand,
    'Product Listing Id': unique_id,
    'Colour' : colour,
    'Listed size status' : listed_sizes_status,
    'size guide' : size_guide_availability,
    'Sold by info' : sold_by_info,
    'Discount' : discount,
    'Season' : season,
    'Buy now' : buy_now,

    'varient': varient,
    'description': description
}

price = json_data['price']
for key, value in price.items():
    if key == 'discount':
        continue
    PDP_dict[key] = value

rating = json_data['rating']
for key, value in rating.items():
    PDP_dict[key] = value


attribute = json_data['attributes']
for key, value in attribute.items():
    if key == 'productColor':
        continue
    PDP_dict[key] = value

manufacturing_details = json_data['manufacturing_details']
for key, value in manufacturing_details.items():
    PDP_dict[key] = value

seller_details = json_data['Seller_details']
for key, value in seller_details.items():
    if key == 'sold_by_info':
        continue
    PDP_dict[key] = value

extras = json_data['extras']
for key, value in extras.items():
    PDP_dict[key] = value

try:
    images = json_data['images']
    for index, value in enumerate(images):
        PDP_dict[f"image_{index + 1}"] = value
except:
    images = ""

PDP_List.append(PDP_dict)

df = pd.DataFrame(PDP_List)
df.to_csv('tatacliq.csv', index=None)
print('done')
