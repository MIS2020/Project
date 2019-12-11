import tkinter
import matplotlib.pyplot as plt
import pandas as pd
import requests

def query1(rest, yourLoc):
    try:
        coord = rest.strip()+";"+yourLoc.strip() #-73.989,40.733 -74,40.733
        apiKey = "pk.eyJ1Ijoic2hlbGxleWhhbiIsImEiOiJjazNzeWw1MnYwN2V5M21teDl4cW40MzR0In0.BvL2yQuNXzZLALCfNbFnKg"
        endpoint = "https://api.mapbox.com/directions/v5/mapbox/driving-traffic/" #/directions/v5/{profile}/{coordinates}
        query='.json?access_token='

        url = endpoint + coord + query + apiKey + "&overview=full" + "&steps=true"
        r = requests.get(url).json()
        return r
        
    except:
        print("Something went wrong :c")

def direction(r):
    window = tkinter.Toplevel(root)
    
    dist= (r['routes'][0]['distance'])/1609.344 #in meters
    dura= (r['routes'][0]['duration'])/60 #in seconds
    start= r['waypoints'][0]['name']
    end= r['waypoints'][1]['name']

    label = tkinter.Label(window, text = f'Distance: {dist:.2f} miles away')
    label.grid(sticky = "W") 
    label1 = tkinter.Label(window, text = f'Duration: {dura:.0f} minutes away')
    label1.grid(sticky = "W") 
    label2 = tkinter.Label(window, text = f'Start Location: {start}') #starting street name
    label2.grid(sticky = "W") 
    label3 = tkinter.Label(window, text = f'End Location: {end}') #ending street name
    label3.grid(sticky = "W")
    label4 = tkinter.Label(window, text = "Directions:")
    label4.grid(sticky = "W")

    ct=0
    steps = r['routes'][0]['legs'][0]['steps']
    for s in range(len(steps)):
        ct+=1
        label5 = tkinter.Label(window, text = f"Step {str(ct)}: {steps[s]['maneuver']['instruction']}")
        label5.grid(sticky = "W")

root = tkinter.Tk() #root object type = Tk
root.title("Directions")
root.geometry("300x300") #size

rest = tkinter.Label(root, text="Enter a location:")
rest.grid(sticky = "W")

name1 = tkinter.StringVar(None) #None = no default value; blank entry box
userInput1 = tkinter.Entry(root, textvariable=name1, width=40) #Entry is always string
userInput1.grid(row = 0, column = 1, sticky = "W")

yourLoc = tkinter.Label(root, text="Enter your location:")
yourLoc.grid(row = 1, sticky = "W")

name2 = tkinter.StringVar(None) #None = no default value; blank entry box
userInput2 = tkinter.Entry(root, textvariable=name2, width=40) #Entry is always string
userInput2.grid(row = 1, column = 1, sticky = "W")

button = tkinter.Button(root,text="Show Directions",command=lambda:[direction(query1(userInput1.get(), userInput2.get()))])
button.grid(row = 2, column = 1, sticky = "W")

#display window
root.mainloop()
