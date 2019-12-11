

import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import imageio

vlat= "40.0370601"
vlong= "-75.3457687"
danlat= "40.0452466"
danlong= "-75.4089339"
r = requests.get("https://api.tomtom.com/routing/1/calculateRoute/"+vlat+","+vlong+":"+danlat+","+danlong+"/xml?avoid=unpavedRoads&key=GYwDUxWmfj5OHNG5J8adH3AG8LQv8izj")
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

r2 = requests.get("https://api.tomtom.com/map/1/staticimage?layer=basic&style=main&format=png&bbox=-122.577756%2C37.636133%2C-122.361772%2C37.841723&view=Unified&key=GYwDUxWmfj5OHNG5J8adH3AG8LQv8izj")
print(r2) # Get the image for our map (MAKE SURE YOU PUT YOUR API KEY IN)

# Import the library to read the image
im = imageio.imread(r2.content)# Read the image from the request

plt.figure(figsize=(20,20))# Create the figure
plt.imshow(im, extent = (-122.577756,-122.361772,37.636133,37.841723))# Show the image
plt.show()

plt.figure(figsize=(20,20))
plt.imshow(im, extent = (-122.577756,-122.361772,37.636133,37.841723))
plt.scatter(long,lat)
plt.show()