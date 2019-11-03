from bs4 import BeautifulSoup
import requests
import pandas as pd
import json

privacy_dic = {}

product_list = []

soup = BeautifulSoup(open("privacy.html"), 'html.parser')
for a in soup.find_all('a', href=True):
    str = a['href']
    if ('/en/privacynotincluded/' in str and '/products/' in str):
        link = "https://foundation.mozilla.org" + str
        product_list.append(link)

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def get_each_product(url):
    ratings = []
    filtered_ratings = []
    privacy_dic ={}
    name_str_list = url.split('products/')
    name_str = name_str_list[1]
    name_str = name_str[0:len(name_str)-1]
    r = requests.get(url, headers=headers)
    product = BeautifulSoup(r.content, 'html.parser')
    for a in product.find_all('div', attrs={'class': 'rating'}):
        #ratings.append(a.getText())
        ratings.append(a.getText().replace("\n", "").replace(" ",""))
        filtered_ratings = ratings[1:6]
    privacy_dic['Product name'] = name_str
    privacy_dic['Encryption'] = filtered_ratings[0]
    privacy_dic['Security updates'] = filtered_ratings[1]
    privacy_dic['Strong password'] = filtered_ratings[2]
    privacy_dic['Manages vulnerabilities'] = filtered_ratings[3]
    privacy_dic['Privacy policy'] = filtered_ratings[4]
    return privacy_dic


privacy_dic_all = []
for product_url in product_list:
    privacy_dic = get_each_product(product_url)
    privacy_dic_all.append(privacy_dic)


with open('data.json', 'w') as f:
    json.dump(privacy_dic_all, f, indent = 4)