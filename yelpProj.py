#Tiffany Nguyen
#Section 001

import pandas as pd
import requests
import tkinter

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

root = tkinter.Tk()
root.title("Food")
root.geometry("1000x1200")

label = tkinter.Label(root, text = "Enter a city, state:")
label.grid(row=0, sticky = "W")
userInput = tkinter.Entry(root, width = 50)
userInput.grid(row=0, column = 1)

label1 = tkinter.Label(root, text = "Enter what you want to find:")
label1.grid(row = 1)
userInput1 = tkinter.Entry(root, text="Restaurants, cuisines, food", width = 50)
userInput1.grid(row = 1, column = 1)

def test(a):
    for i in range(len(a)):
        print(a[i]['id'])
        return a[i]['id']

def lst(a):
    for i in range(len(a)):
        b = tkinter.Button(root, height=5, width=50, text = 'Restaurant: ' + a[i]['name'] + '\n Category: ' + a[i]['categories'][0]['title'] + '\n Rating: ' + str(a[i]['rating']) + '\n Address: ' + a[i]['location']['display_address'][0] + ", " + a[i]['location']['display_address'][1], command = test(rest))
        b.grid(row = i+2, column = 1)

lst(rest)
root.mainloop()

