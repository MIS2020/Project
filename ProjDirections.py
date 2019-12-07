import pandas as pd
import requests
import matplotlib.pyplot as plt



coord = "-73.989,40.733;-74,40.733" 
apiKey = "pk.eyJ1Ijoic2hlbGxleWhhbiIsImEiOiJjazNzeWw1MnYwN2V5M21teDl4cW40MzR0In0.BvL2yQuNXzZLALCfNbFnKg"
endpoint = "https://api.mapbox.com/directions/v5/mapbox/driving-traffic/"
query='.json?access_token='

#/directions/v5/{profile}/{coordinates}

url = endpoint + coord + query + apiKey + "&overview=full" + "&steps=true"
r = requests.get(url).json()
#print(r)

dist= (r['routes'][0]['distance'])/1609.344 #in meters
dura= (r['routes'][0]['duration'])/60 #in seconds
start= r['waypoints'][0]['name']
end= r['waypoints'][1]['name']

print(f'Distance: {dist:.2f} miles away.')
print(f'Duration: {dura:.f} minutes away.')
print(f'Start Location: {start}') #starting street name
print(f'End Location: {end}') #ending street name

print(f'Directions: ')
c=0
steps = r['routes'][0]['legs'][0]
for d in range(len(steps)):
    c+=1
    print("Step "+str(c)+": "+r['routes'][0]['legs'][0]['steps'][d]['maneuver']['instruction'])
    
    



#maps
#how to show distance from specific location on a map
#show how far away from pinpointed location
#show that distance on a map
#popup with directions 

#see if you can make multiple locations pop up on map

