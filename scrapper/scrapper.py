from bs4 import BeautifulSoup
import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# https://www.dakcoffeeroasters.com/shop 
# https://fivewayscoffee.com/collections/coffee-for-vat-override 
# https://manhattancoffeeroasters.com/catalog/coffee 
# https://amatterofconcrete.com/product-category/coffee/all/ 
# https://friedhats.com/pages/shop 
# https://www.andy-roasters.be/coffee/filter/ 
# https://shop.gardellicoffee.com/14-coffees

final_df = pd.DataFrame()


url = "https://fivewayscoffee.com"
webpage = requests.get('https://fivewayscoffee.com/collections/coffee-for-vat-override ')

# 3.:
soup = BeautifulSoup(webpage.content, "html.parser")

Product_info = soup.find_all('div', class_='product-card-info')

# Extract and print the text content of each <a> tag
new_links = []
for info in Product_info:
    a_tags = info.find_all('a')

    for a_tag in a_tags:
            new_links.append(a_tag['href'])


second_list = []

for i in range(len(new_links)):
      if new_links[i] not in second_list:
            second_list.append(new_links[i])

for i in range(1,3):
    full_url = url + second_list[i]
    
    webpage = requests.get(full_url)
    soup = BeautifulSoup(webpage.content, 'html.parser')
    product_description = soup.find('div', class_='product-short-description rte')
    image = soup.find('div', class_ = 'product-single__media product-single__media-image aspect-ratio aspect-ratio--adapt')
    links = image.find_all('a')
    image_links = [link.get('href') for link in links]
    image_link = "https:" + image_links[0]
    para = product_description.find_all('p')
    details = {}
    for detail in para:
        if detail.find('strong'):
            key = detail.find('strong').text.strip()
            value = detail.contents[-1].strip()
            details[key] = value
    product_title_div = soup.find('div', class_='product-title-container')

    product_title = product_title_div.find('h1', class_='product-title').text.strip()

        # Extract product price
    product_price = soup.find('span', class_='amount').text.strip()
    details['Product_des'] = para[0]
    details['image_link'] = image_link
    details['product_title'] = product_title
    details['product_price'] = product_price


    df = pd.DataFrame([details])

    final_df = final_df._append(df)

final_df.to_csv("sample2.csv")

                



