import pandas as pd
import requests


# coord = 
# apiKey = "GYwDUxWmfj5OHNG5J8adH3AG8LQv8izj"
# endpoint = 
# query=

# #/directions/v5/{profile}/{coordinates}

# url = endpoint + coord + query + apiKey 
# r = requests.get(url).json()
# #print(r)

# coord = "-73.989,40.733;-74,40.733" 
# apiKey = "pk.eyJ1Ijoic2hlbGxleWhhbiIsImEiOiJjazNzeWw1MnYwN2V5M21teDl4cW40MzR0In0.BvL2yQuNXzZLALCfNbFnKg"
# endpoint = "https://api.mapbox.com/directions/v5/mapbox/driving-traffic/"
# query='.json?access_token='

# #/directions/v5/{profile}/{coordinates}

# url = endpoint + coord + query + apiKey + "&overview=full" + "&steps=true"
# r = requests.get(url).json()
# #print(r)

url = "https://api.tomtom.com/map/1/tile/basic/main/10/1/3.pbf?view=Unified&key=*****"
r = requests.get(url).json()
print(r)
