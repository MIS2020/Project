import requests
import matplotlib.pyplot as plt
import pandas as pd
import imageio
import io
from PIL import Image, ImageTk
import tkinter as tk
import tkinter
from urllib.request import urlopen
import polyline

#calculates that weird string of characters next to path
def route(rest, yourLoc): 
    # from here
    coord = rest.strip()+";"+yourLoc.strip()
    apiKey = "pk.eyJ1Ijoic2hlbGxleWhhbiIsImEiOiJjazNzeWw1MnYwN2V5M21teDl4cW40MzR0In0.BvL2yQuNXzZLALCfNbFnKg"
    endpoint = "https://api.mapbox.com/directions/v5/mapbox/driving-traffic/" 
    query='.json?access_token='

    rturl = endpoint + coord + query + apiKey + "&overview=full" + "&steps=true"
    r = requests.get(rturl).json()
    # to here is all the same as getting the directions just diff names but it doesnt matter
    plst=[] 
    dire = r['routes'][0]['legs'][0] 
    for d in range(len(dire)): #list of directions coordinates
        a=r['routes'][0]['legs'][0]['steps'][d]['maneuver']['location']
        plst.append(a)

    pathline= polyline.encode(plst,6) #osm is 6 and mapbox uses osm ,,,, i think ??
    #polyline needs a list of each direction coordinate to plot the route
    return pathline

# #example ones
# alat= "40.0370601"
# along= "-75.3457687"
# blat= "40.0452466"
# blong= "-75.4089339"

# rest= f'{alat},{along}' 
# yourLoc= f'{blat},{blong}'

apiKeyMap = "pk.eyJ1Ijoic2hlbGxleWhhbiIsImEiOiJjazQxb2s4dGgwM2poM21vMHBsZ290YXE5In0.C9dP5-U53nwvj21NkG_oVQ"
endpoint2 = "https://api.mapbox.com/styles/v1/mapbox/streets-v11/static"
pline= route(rest, yourLoc)

pin1= "pin-s-a+000"+f'({along},{alat})' #lon,lat #black start
pin2= "pin-s-b+ff0000"+f'({blong},{blat})' #red end
path= "path-5+0080ff-0.5"+f'({pline})' #blue line
size2 = "500x300"

url2 = f'{endpoint2}/{pin1},{pin2},{path}/auto/{size2}?access_token={apiKeyMap}'

root = tk.Tk()
image_bytes = urlopen(url2).read()
data_stream = io.BytesIO(image_bytes)
pil_image = Image.open(data_stream)
tk_image = ImageTk.PhotoImage(pil_image)
label = tk.Label(root, image=tk_image, bg='brown')
label.grid()
root.mainloop() #show image
