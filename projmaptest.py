

import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import imageio

key= "GYwDUxWmfj5OHNG5J8adH3AG8LQv8izj"
endpoint= "https://api.tomtom.com/routing/1/calculateRoute/"
query= "/xml?avoid=unpavedRoads&key="

#example ones
vlat= "40.0370601"
vlong= "-75.3457687"
danlat= "40.0452466"
danlong= "-75.4089339"

url= endpoint+vlat+","+vlong+":"+danlat+","+danlong+query+key
r = requests.get(url)
print(r) #response = 200 is good

#beautiful soup
c = r.content
soup = BeautifulSoup(c)
print(soup.prettify())

Points = soup.find_all('point') # Find all the tags that contain a point in our route
lat = []
long = []
for point in Points:
    lat.append(point['latitude'])
    long.append(point['longitude'])

lat = [float(x) for x in lat]
long = [float(x) for x in long]

#matplotlib
plt.scatter(long,lat)
plt.title('Route from TomTom API')
plt.show()

# z= "10" #what zoom they want -maybe drop down?idk
# zoom= "&zoom="+z
endpoint2= "https://api.tomtom.com/map/1/staticimage?layer=basic&style=main&format=png&center="#+zoom after png
query2= "&width=5120&height=5120&view=Unified&key="
#example ones
#centerlong= "52.379031"
#centerlat= "4.899886"
centerlat=(float(vlat)+float(danlat))/2
centerlong=(float(vlong)+float(danlong))/2

url2= endpoint2+str(centerlat)+"%2C%20"+str(centerlong)+query2+key
r2 = requests.get(url2)
print(r2) # Get the image for our map

# Import the library to read the image
im = imageio.imread(r2.content)# Read the image from the request


plt.figure(figsize=(20,20))# Create the figure
plt.imshow(im, origin = (centerlat,centerlong))# Show the image
plt.show()

plt.figure(figsize=(20,20))
plt.imshow(im, origin = (centerlat, centerlong))
plt.scatter(long,lat)
plt.show()