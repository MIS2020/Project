import pandas as pd
import numpy as np
import requests
import tkinter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk
import mapbox
from PIL import Image, ImageTk
from urllib.request import urlopen
import io
import polyline
from matplotlib.ticker import MaxNLocator

apiKeyYelp = "Vf_kMcMZt6iW4-7OIxCtGtrAfayeobOiIYBw37cfDIorGutNbHVOKcWfhklmPGx6XodG16Us2o7O5ZRaC1RytNIcUghLuBF1hCK3q9V_U4CJLVztVZQtFLTui8vuXXYx"
endpoint = "https://api.yelp.com/v3/"
headers = {'Authorization': 'Bearer %s' % apiKeyYelp}

apiKeyMap = "pk.eyJ1IjoidGh1Y3V5ZW4wNCIsImEiOiJjazQzc3Bwc3IwYmZnM3Fwazg2MGptaW50In0.d2ehvcaU3U4pjm5R1BoO1A"

#Create global variables
rest = ""
rid = []
box = None
rat = []
pathline = ""
userInput2 = None
window = None
endDes = ""
long = ""
lat = ""
button3 = None

#Function to run the main query
def query():
    global rest
    global rid
    rid = []
    try:
        params = {}
        params['location'] = userInput.get()
        params['term'] = userInput1.get()
        params['sort_by'] = sort[sortOption.get()]
        query1 = f'businesses/search'
        url1 = endpoint + query1
        a = requests.get(url1, params=params, headers=headers).json()
        rest = a['businesses']
        for i in range(len(rest)):
            rid.append(rest[i]['id'])
    except:
        noti = tkinter.Toplevel()
        noti.config(background = "#cfe3fc")
        noti.title("Error")
        label = tkinter.Label(noti, background = "#cfe3fc", text = "Something is wrong. Try again!")
        label.grid()
        button = tkinter.Button(noti, text = "Close", background = "#829dfc", command = noti.destroy)
        button.grid()
    else:
        return

#Function to display list of restaurants in combo box
def main():
    global box
    global button3

    #Hide the map button when the ratio is not calculated yet
    if str(type(button3)) == "<class 'tkinter.Button'>" :
        button3.grid_remove()

    drop = []
    for i in range(len(rest)):
        drop.append(str(i) + '. Restaurant: ' + rest[i]['name'] + '; Cuisine: ' + rest[i]['categories'][0]['title'] + '; Rating: ' + str(rest[i]['rating']))
    box = ttk.Combobox(root, width = 90, values = drop)
    box.set("Select an option from the list to get more information")
    box.grid(columnspan = 4, row=4)
    
#Function to display graph of price rating for each restaurant
def graph():
    r = []
    p = [] 
    for i in range(len(rest)):
        #Get restaurants names
        r.append(rest[i]['name'])
        #Retrieve price information for each restaurant in the list
        query2 = f'businesses/'
        url2 = endpoint + query2 + str(rest[i]['id'])
        b = requests.get(url2, headers=headers).json()
        try:
            b['price']
        except:
            p.append(0)
        else:
            if b['price'] == '$':
                p.append(1)
            elif b['price'] == '$$':
                p.append(2)
            elif b['price'] == '$$$':
                p.append(3)
            else:
                p.append(4)
    #Create a dataframe
    data = {'Restaurant':r, 'Price':p}
    df = pd.DataFrame(data)
    
    #Create graph
    win = tkinter.Toplevel()
    win.title("Price Range Graph")
    win.geometry("1000x700")
    win.config(background = "#cfe3fc")
    figure1 = plt.Figure(figsize=(10,10), dpi=100, frameon="False")
    ax1 = figure1.add_subplot(211)
    bar1 = FigureCanvasTkAgg(figure1, win)
    bar1.get_tk_widget().grid(row = 0)
    df.plot(kind='bar', x= 'Restaurant', y= 'Price', color = '#829dfc', ax = ax1)
    ax1.set_title("Price Range of Each Restaurant in the List", fontsize = "10")
    ax1.set_ylabel("Price Range ($ - $$$$)", fontsize = "9")
    ax1.set_xlabel("Restaurant Name", fontsize = "9")
    ax1.tick_params(labelsize = '7')
    ax1.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax1.set_ylim(0,4)

#Function displays graph of price rating vs restaurant rating ratio for each restaurant in the list
def ratio():
    global rat
    global button3

    r = []
    ra = []
    p = [] 
    for i in range(len(rest)):
        #Get restaurants names
        r.append(rest[i]['name'])
        #Get restaurants ratings
        ra.append(rest[i]['rating'])
        #Retrieve price information for each restaurant in the list
        query2 = f'businesses/'
        url2 = endpoint + query2 + str(rest[i]['id'])
        b = requests.get(url2, headers=headers).json()
        try:
            b['price']
        except:
            p.append(0)
        else:
            if b['price'] == '$':
                p.append(1)
            elif b['price'] == '$$':
                p.append(2)
            elif b['price'] == '$$$':
                p.append(3)
            else:
                p.append(4)
    rat = []
    for j, i in zip(ra, p):
        if i != 0:
            rat.append(round(j/i,2)) 
        else:
            rat.append(0)

    #Color code based on ratio values
    label = []
    for i in range(len(rat)):
        if rat[i] <= 2 and rat[i] >= 1:
            label.append("Expected")
        elif rat[i] > 2:
            label.append("Good")
        elif rat[i] == 0:
            label.append("NA")
        else:
            label.append("Bad")
    colors = []
    for i in range(len(label)):
        if label[i] == "Expected":
            colors.append("yellow")
        elif label[i] == "Good":
            colors.append("green")
        elif label[i] == "Bad":
            colors.append("red")
        else:
            colors.append("grey")

    #Create a dataframe
    data1 = {'Restaurant':r, 'Rating': ra, 'Price':p, 'Ratio':rat, 'Label': label}
    df1 = pd.DataFrame(data1)
    print(df1)

    #Create graph
    win = tkinter.Toplevel()
    win.title("Rating-Price Ratio Graph")
    win.geometry("1000x700")
    win.config(background = "#cfe3fc")
    figure1 = plt.Figure(figsize=(10,10), dpi=100, frameon="False")
    ax1 = figure1.add_subplot(211)
    bar1 = FigureCanvasTkAgg(figure1, win)
    bar1.get_tk_widget().grid(row = 0)
    df1.plot(kind='bar', x= 'Restaurant', y = 'Ratio', color = colors, ax=ax1)
    ax1.get_legend().remove()
    plt.show()
    ax1.set_title("Restaurant Rating vs Price Range Ratio for Each Restaurant in the List")
    ax1.set_ylabel("Number of Stars per 1 $")
    ax1.set_xlabel("Restaurant Name")
    ax1.tick_params(labelsize = '7')

    #Create button to show map
    button3 = tkinter.Button(root, text="Map", width = 15, background = "#829dfc", command = lambda: [mapp(query3())])
    button3.grid (row = 3, column = 6)


#Function runs query to get static map
def query3():
    a = ""
    lst = []
    endpoint = "https://api.mapbox.com/styles/v1/mapbox/streets-v11/static"
    size = "500x800"

    #Create pin; pin color changes based on ratio
    for i in range(len(rest)):
        if rat[i] > 2:
            lst.append(f"pin-s-{i}+008000({rest[i]['coordinates']['longitude']},{rest[i]['coordinates']['latitude']})")
        elif rat[i] >= 1 and rat[i] <= 2:
            lst.append(f"pin-s-{i}+ffff1a({rest[i]['coordinates']['longitude']},{rest[i]['coordinates']['latitude']})")
        elif rat[i] == 0:
            lst.append(f"pin-s-{i}+a6a6a6({rest[i]['coordinates']['longitude']},{rest[i]['coordinates']['latitude']})")
        else:
            lst.append(f"pin-s-{i}+e60000({rest[i]['coordinates']['longitude']},{rest[i]['coordinates']['latitude']})")

    for i in range(len(lst)-1):
        a = a + lst[i] + ","

    c = userInput3.get()

    #Add pin of your location when provided
    if c != '':
        a = a + lst[19] + f",pin-s-y+829dfc({loc(c)})" 
    else:
        a = a + lst[19]

    url = f"{endpoint}/{a}/auto/{size}?access_token={apiKeyMap}"
    return url

#Function displays static map
def mapp(url):
    image_bytes = urlopen(url).read()
    data_stream = io.BytesIO(image_bytes)
    pil_image = Image.open(data_stream)
    tk_image = ImageTk.PhotoImage(pil_image)
    label = tkinter.Label(root, image=tk_image, bg='black')
    label.grid(row = 5, column = 7)
    win.mainloop() #Why must have this for map to appear?

#Function prints the detail of a restaurant in a pop up window
def detail():
    global userInput2
    global endDes
    global long
    global lat

    win = tkinter.Toplevel()
    win.title("Restaurant detail")
    # win.geometry("800x500")
    win.config(background = "#cfe3fc")
    query2 = f'businesses/'
    url2 = endpoint + query2 + rid[box.current()]
    a = requests.get(url2, headers=headers).json()
    endDes = a['name']
    label = tkinter.Label(win, background = "#cfe3fc", text = f"Restaurant: {a['name']}")
    label.grid(sticky = "W")
    label1 = tkinter.Label(win, background = "#cfe3fc", text = f"Phone: {a['display_phone']}")
    label1.grid(sticky = "W")
    label2 = tkinter.Label(win, background = "#cfe3fc", text = f"Address: {a['location']['display_address'][0]}, {a['location']['display_address'][1]}")
    label2.grid(sticky = "W")
    
    #Avoid program to crash if there is no price information
    try:
        a['price']
    except:
        label3 = tkinter.Label(win, background = "#cfe3fc", text = "No price information")
        label3.grid(sticky = "W")
    else:
        label3 = tkinter.Label(win, background = "#cfe3fc", text = f"Price rating: {a['price']}")
        label3.grid(sticky = "W")
    
    #Avoid program to crash if there is no hours information
    try:
        a['hours']
    except:
        label4 = tkinter.Label(win, background = "#cfe3fc", text = "No hours information")
        label4.grid(sticky = "W")
    else:
        if a['hours'][0]['is_open_now'] == "True":
            label5 = tkinter.Label(win, background = "#cfe3fc", text = f"Open now: Yes")
        else:
            label5 = tkinter.Label(win, background = "#cfe3fc", text = f"Open now: No")
        label5.grid(sticky = "W")
        for z in range(len(a['hours'][0]['open'])):
            if a['hours'][0]['open'][z]['day'] == 0:
                label6 = tkinter.Label(win, background = "#cfe3fc", text = f"Monday: {':'.join(a['hours'][0]['open'][z]['start'][i:i+2] for i in range(0, len(a['hours'][0]['open'][z]['start']), 2))} - {':'.join(a['hours'][0]['open'][z]['end'][i:i+2] for i in range(0, len(a['hours'][0]['open'][z]['end']), 2))}")
                label6.grid(sticky = "W")
            elif a['hours'][0]['open'][z]['day'] == 1:
                label7 = tkinter.Label(win, background = "#cfe3fc", text = f"Tuesday: {':'.join(a['hours'][0]['open'][z]['start'][i:i+2] for i in range(0, len(a['hours'][0]['open'][z]['start']), 2))} - {':'.join(a['hours'][0]['open'][z]['end'][i:i+2] for i in range(0, len(a['hours'][0]['open'][z]['end']), 2))}")
                label7.grid(sticky = "W")
            elif a['hours'][0]['open'][z]['day'] == 2:
                label8 = tkinter.Label(win, background = "#cfe3fc", text = f"Wednesday: {':'.join(a['hours'][0]['open'][z]['start'][i:i+2] for i in range(0, len(a['hours'][0]['open'][z]['start']), 2))} - {':'.join(a['hours'][0]['open'][z]['end'][i:i+2] for i in range(0, len(a['hours'][0]['open'][z]['end']), 2))}")
                label8.grid(sticky = "W")
            elif a['hours'][0]['open'][z]['day'] == 3:
                label9 = tkinter.Label(win, background = "#cfe3fc", text = f"Thursday: {':'.join(a['hours'][0]['open'][z]['start'][i:i+2] for i in range(0, len(a['hours'][0]['open'][z]['start']), 2))} - {':'.join(a['hours'][0]['open'][z]['end'][i:i+2] for i in range(0, len(a['hours'][0]['open'][z]['end']), 2))}")
                label9.grid(sticky = "W")
            elif a['hours'][0]['open'][z]['day'] == 4:
                label10 = tkinter.Label(win, background = "#cfe3fc", text = f"Friday: {':'.join(a['hours'][0]['open'][z]['start'][i:i+2] for i in range(0, len(a['hours'][0]['open'][z]['start']), 2))} - {':'.join(a['hours'][0]['open'][z]['end'][i:i+2] for i in range(0, len(a['hours'][0]['open'][z]['end']), 2))}")
                label10.grid(sticky = "W")
            elif a['hours'][0]['open'][z]['day'] == 5:
                label11 = tkinter.Label(win, background = "#cfe3fc", text = f"Saturday: {':'.join(a['hours'][0]['open'][z]['start'][i:i+2] for i in range(0, len(a['hours'][0]['open'][z]['start']), 2))} - {':'.join(a['hours'][0]['open'][z]['end'][i:i+2] for i in range(0, len(a['hours'][0]['open'][z]['end']), 2))}")
                label11.grid(sticky = "W")
            else:
                label12 = tkinter.Label(win, background = "#cfe3fc", text = f"Sunday: {':'.join(a['hours'][0]['open'][z]['start'][i:i+2] for i in range(0, len(a['hours'][0]['open'][z]['start']), 2))} - {':'.join(a['hours'][0]['open'][z]['end'][i:i+2] for i in range(0, len(a['hours'][0]['open'][z]['end']), 2))}")
                label12.grid(sticky = "W")
    long = a['coordinates']['longitude']
    lat = a['coordinates']['latitude']

    #Create textbox for user input of their location coordinates
    yourLoc = tkinter.Label(win, background = "#cfe3fc", text="Enter your location:")
    yourLoc.grid(row = 0, column = 4, sticky = "W")
    name1 = tkinter.StringVar(None) #None = no default value; blank entry box
    userInput2 = tkinter.Entry(win, textvariable=name1, width=40) #Entry is always string
    userInput2.grid(row = 0, column = 5, sticky = "W")

    #Create button to show directions
    button3 = tkinter.Button(win, background = "#829dfc", text="Show Directions", command=lambda:[direction(query1(long,lat,loc(userInput2.get()))), dmap()])
    button3.grid(row = 0, column = 6, sticky = "W")

#Get coordinates for the start location the user enter
def loc(address):
    geocoder = mapbox.Geocoder(access_token=apiKeyMap)
    response = geocoder.forward(address)
    geo = response.json()
    loc = f"{geo['features'][0]['center'][0]},{geo['features'][0]['center'][1]}"
    return loc

#Function runs query that gives direction
def query1(dlong, dlat, yourLoc='-75.339692,40.037123'):
    try:
        coord = f'{yourLoc.strip()};{dlong},{dlat}'
        endpoint = "https://api.mapbox.com/directions/v5/mapbox/driving-traffic/"
        query='.json?access_token='

        url = endpoint + coord + query + apiKeyMap + "&overview=full" + "&steps=true"
        r = requests.get(url).json()
    
    #Prevent program from crashing if coordinates are wrong
    except:
        noti = tkinter.Toplevel()
        noti.config(background = "#cfe3fc")
        label = tkinter.Label(noti, background = "#cfe3fc",  text = "Something went wrong!")
        label.grid()
        button = tkinter.Button(noti, background = "#829dfc", text = "Close", command = noti.destroy)
        button.grid()

    else:
        #Prevent program from crashing if coordinates are wrong
        if r['code'] == "InvalidInput" or r['code'] == "NoRoute":
            noti = tkinter.Toplevel()
            noti.config(background = "#cfe3fc")
            noti.title("Error")
            label = tkinter.Label(noti, background = "#cfe3fc", text = "Something went wrong!")
            label.grid()
            button = tkinter.Button(noti, background = "#829dfc", text = "Close", command = noti.destroy)
            button.grid()
        return r 

#Function displays direction
def direction(r):
    global pathline
    global window
    global userInput2
    global endDes

    window = tkinter.Toplevel()
    window.config(background = "#cfe3fc")
    window.title("Directions")
    dist= (r['routes'][0]['distance'])/1609.344 #in meters
    dura= (r['routes'][0]['duration'])/60 #in seconds
    if r['waypoints'][0]['name'] == '':
        start = userInput2.get()
    else:
        start = r['waypoints'][0]['name']
    if r['waypoints'][1]['name'] == '':
        end = endDes
    else:
        end = r['waypoints'][1]['name']

    label = tkinter.Label(window, background = "#cfe3fc", text = f'Distance: {dist:.2f} miles away')
    label.grid(sticky = "W") 
    label1 = tkinter.Label(window, background = "#cfe3fc", text = f'Duration: {dura:.0f} minutes away')
    label1.grid(sticky = "W") 
    label2 = tkinter.Label(window, background = "#cfe3fc", text = f'Start Location: {start}') #starting street name
    label2.grid(sticky = "W") 
    label3 = tkinter.Label(window, background = "#cfe3fc", text = f'End Location: {end}') #ending street name
    label3.grid(sticky = "W")
    label4 = tkinter.Label(window, background = "#cfe3fc", text = "Directions:")
    label4.grid(sticky = "W")

    ct=0
    steps = r['routes'][0]['legs'][0]['steps']
    for s in range(len(steps)):
        ct+=1
        label5 = tkinter.Label(window, background = "#cfe3fc", text = f"Step {str(ct)}: {steps[s]['maneuver']['instruction']}")
        label5.grid(sticky = "W")

    plst=[] 
    dire = r['routes'][0]['legs'][0]['steps']
    #list of directions coordinates
    for d in range(len(dire)): 
        plst.append(tuple(dire[d]["maneuver"]["location"]))

    pathline = polyline.encode(plst, geojson = True)

#Function displays map direction
def dmap():
    global userInput2
    global window
    global long
    global lat

    endpoint2 = "https://api.mapbox.com/styles/v1/mapbox/streets-v11/static"

    pin1= "pin-s-a+000"+f'({loc(userInput2.get())})' #lon,lat #black start
    pin2= "pin-s-b+ff0000"+f'({long},{lat})' #red end
    path= "path-5+829dfc-0.75"+f'({pathline})' #blue line
    size2 = "500x300"

    url2 = f'{endpoint2}/{pin1},{pin2},{path}/auto/{size2}?access_token={apiKeyMap}'

    #Display map on GUI
    image_bytes = urlopen(url2).read()
    data_stream = io.BytesIO(image_bytes)
    pil_image = Image.open(data_stream)
    tk_image = ImageTk.PhotoImage(pil_image)
    label = tkinter.Label(window, image=tk_image, bg='black')
    label.grid()
    win.mainloop() #Why must have this for map to appear?

#Create main window
root = tkinter.Tk()
root.title("List of Restaurants")
root.geometry("1200x1200")
root.config(background = "#cfe3fc")

#Create textbox for user input of location
label = tkinter.Label(root, text = "Enter a city, state:")
label.config(background = "#cfe3fc")
label.grid(row=0, sticky = "W")
userInput = tkinter.Entry(root, width = 15)
userInput.grid(row=0, column = 1)

#Create textbox for user input of term
label1 = tkinter.Label(root, text = "Enter what you want to find:")
label1.config(background = "#cfe3fc")
label1.grid(row = 1, sticky = "W")
userInput1 = tkinter.Entry(root, width = 15)
userInput1.grid(row = 1, column = 1)

#Create radio button for sorting options
sort = ["best_match", "rating", "review_count", "distance"]
sortOption = tkinter.IntVar()
sortOption.set(0)
for x in range(len(sort)):
    r = tkinter.Radiobutton(root, text = sort[x], variable = sortOption, value = x, background = "#cfe3fc")
    r.grid(row = 2, column = x)

#Create user input of their location
label3 = tkinter.Label(root, text = "Enter your location:")
label3.config(background = "#cfe3fc")
label3.grid(row = 3, sticky = "W")
userInput3 = tkinter.Entry(root, width = 15)
userInput3.grid(row = 3, column = 1)

#Create button to run query
button = tkinter.Button(root, text="Go!", background = "#829dfc", command = lambda: [query(), main()])
button.grid (row = 1, column = 2)

#Create button to show price rating graph
button1 = tkinter.Button(root, text="Price Range", background = "#829dfc", width = 15,  command = lambda: [graph()])
button1.grid (row = 0, column = 6)

#Create button to show ratio graph
button2 = tkinter.Button(root, text="Ratio", background = "#829dfc", width = 15, command = lambda: [ratio()])
button2.grid (row = 1, column = 6)

#Create button to show restaurant details
button4 = tkinter.Button(root, text = "Show Detail", background = "#829dfc", width = 15, command = lambda: [detail()])
button4.grid(row = 2, column = 6)

#Display window
root.mainloop()
