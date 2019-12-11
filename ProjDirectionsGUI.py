import tkinter
import matplotlib.pyplot as plt
import pandas as pd
import requests

def directions(rest, yourLoc):
    try:
        coord = rest.strip()+";"+yourLoc.strip() #-73.989,40.733 -74,40.733
        apiKey = "pk.eyJ1Ijoic2hlbGxleWhhbiIsImEiOiJjazNzeWw1MnYwN2V5M21teDl4cW40MzR0In0.BvL2yQuNXzZLALCfNbFnKg"
        endpoint = "https://api.mapbox.com/directions/v5/mapbox/driving-traffic/" #/directions/v5/{profile}/{coordinates}
        query='.json?access_token='

        url = endpoint + coord + query + apiKey + "&overview=full" + "&steps=true"
        r = requests.get(url).json()
        #print(r)

        lst1=[]
        
        dist= (r['routes'][0]['distance'])/1609.344 #in meters
        dura= (r['routes'][0]['duration'])/60 #in seconds
        start= r['waypoints'][0]['name']
        end= r['waypoints'][1]['name']

        a=(f'Distance: {dist:.2f} miles away.')
        b=(f'Duration: {dura:.0f} minutes away.')
        c=(f'Start Location: {start}') #starting street name
        d=(f'End Location: {end}') #ending street name

        lst1.append(a)
        lst1.append(b)
        lst1.append(c)
        lst1.append(d)

        print(f'Directions: ')
        ct=0
        steps = r['routes'][0]['legs'][0]
        for s in range(len(steps)):
            ct+=1
            e="Step "+str(ct)+": "+r['routes'][0]['legs'][0]['steps'][s]['maneuver']['instruction']
            lst1.append(e)

        newWindow(lst1)
        
    except:
        print("something went wrong :c")

def newWindow(lst2):
    window = tkinter.Toplevel(root)
    display = tkinter.Label(window, text=lst2, width=50, height=30) 
    #need to add code to display nicely
    display.pack() 

root = tkinter.Tk() #root object type = Tk
root.title("Directions")
root.geometry("300x300") #size

rest = tkinter.Label(root, text="Enter a location:")
rest.pack()

name1 = tkinter.StringVar(None) #None = no default value; blank entry box
userInput1 = tkinter.Entry(root, textvariable=name1, width=40) #Entry is always string
userInput1.pack()

yourLoc = tkinter.Label(root, text="Enter your location:")
yourLoc.pack()

name2 = tkinter.StringVar(None) #None = no default value; blank entry box
userInput2 = tkinter.Entry(root, textvariable=name2, width=40) #Entry is always string
userInput2.pack()

button = tkinter.Button(root,text="Show Directions",command=lambda:[directions(userInput1.get(), userInput2.get())])
button.pack()

#display window
root.mainloop()
