#Tiffany Nguyen
#Section 001

import pandas as pd
import requests
import matplotlib.pyplot as plt

apiKey = "90c2a938d1b174d15e832ec7ba110778"

endpoint="https://developers.zomato.com/api/v2.1/"

def suggestion(a):
    print("Here is the list of the locations with the input you enter. Please choose the ID associated with the location you want!")
    for i in a:
        print("ID: " + str(i['id']))
        print("City Name: " + i['name'])
        print("State: " + i['state_name'])
        print("Country: " + i['country_name'])
        print("_______")

def cuisineList(a):
    for i in a:
            print("cuisine ID: " + str(i['cuisine']['cuisine_id']))
            print("cuisine Name: " + str(i['cuisine']['cuisine_name']))
            print("_______")

#Allow multiple entries using a loop
while True:
    #Allow user to enter in city name and country code
    name = input("Please enter a city or country or 'Done' if you want to exit: ")
    if name in ("Done","done","DONE"):
        break
    query1 = f'cities?q={name}'
    url1 = endpoint + query1 + "&apikey=" + apiKey
    a = requests.get(url1).json()
    locSug = a['location_suggestions']
    if locSug == []:
        print("Sorry, we cannot find any city or country with your input in it in our database. Please enter the information again.")
    else:
        suggestion(locSug)
        cityid = input("Please enter the city ID of the location you want from the list above: ")
        query2 = f'location_details?entity_id={cityid}&entity_type=city'
        url2 = endpoint + query2 + "&apikey=" + apiKey
        b = requests.get(url2).json()
        print(f'The popularity rating of {b["city"]} is {b["popularity"]}/5.00 and the nightlife rating is {b["nightlife_index"]}/5.00')
        print(f'The top cuisines at your chosen location is {b["top_cuisines"]}')
        query3 = f'cuisines?city_id={cityid}'
        url3 = endpoint + query3 + "&apikey=" + apiKey
        c = requests.get(url3).json()
        cuisine = c['cuisines']
        # cuisineList(cuisine)
        query4 = f'collections?city_id={cityid}'
        url4 = endpoint + query4 + "&apikey=" + apiKey
        d = requests.get(url4).json()
        col = d["collections"]
        for i in col:
            print("Collection ID: " + str(i["collection"]["collection_id"]))
            print("Collection title: " + i["collection"]["title"])
            print("Description: " + i["collection"]["description"])
            print("_______")

        