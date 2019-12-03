#Tiffany Nguyen
#Section 001

import pandas as pd
import requests
import matplotlib.pyplot as plt

userID = "2B41kI-lDbSxtgcBq-lSSw"

apiKey = "1VQkKQlVhQa5yHwWtx4fyfoLMTf1pZGwAoSAhp3TrpGdUpXuSnJxy8H3eiZYfKEGoYJhZPZjBg9_g8CnhMspqfrQxegqusHwPZcFRaGheRcp2bp9HLWRZjuyBPjaXXYx"

endpoint = "https://api.yelp.com/v3/"

name = input("Please enter a city and/or state or 'Done' if you want to exit: ")
term = input("Please enter what you want to look for in the desired location: ")
order = input("Please choose how you want to sort the result (best_match, rating, review_count or distance): ")

headers = {'Authorization': 'Bearer %s' % apiKey}

params = {}

params['location'] = name
params['term'] = term
params['sorty_by'] = order

query1 = f'businesses/search'
url = endpoint + query1
a = requests.get(url, params=params, headers=headers).json()

rest = a['businesses']

if order == "rating":
    print("*Note that the rating sort is not strictly sorted by the rating value, but by an adjusted rating value that takes into account the number of ratings")

for i in rest:
    print("Name: " + i['name'])
    print("Cuisine: " + i['categories'][0]['title'])
    print(i['rating'])
    print(i['location']['display_address'])
    print("ID: " + i['id'])
    print("__________")

