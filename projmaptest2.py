
import requests

key = "pk.eyJ1Ijoic2hlbGxleWhhbiIsImEiOiJjazQxb2s4dGgwM2poM21vMHBsZ290YXE5In0.C9dP5-U53nwvj21NkG_oVQ"
endpoint= "https://api.mapbox.com/styles/v1/mapbox/streets-v11/static/"
clong= "-75.377349"
clat= "40.041158"
zoom= "10"
width= "300"
height= "300"
query= "?access_token="

#Latitude: 40.041158
#Longitude: -75.377349

url = endpoint+clong+","+clat+","+zoom+"/"+width+"x"+height+query+key
#https://api.mapbox.com/styles/v1/mapbox/streets-v11/static/-75.3773,40.0412,10/300x300?access_token=YOUR_MAPBOX_ACCESS_TOKEN
r = requests.get(url)
print(r)
