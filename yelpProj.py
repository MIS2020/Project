import pandas as pd
import numpy as np
import requests
import tkinter
import matplotlib.pyplot as plt
from tkinter import ttk
import mapbox
from PIL import Image, ImageTk
from urllib.request import urlopen
import io
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

apiKeyYelp = "Vf_kMcMZt6iW4-7OIxCtGtrAfayeobOiIYBw37cfDIorGutNbHVOKcWfhklmPGx6XodG16Us2o7O5ZRaC1RytNIcUghLuBF1hCK3q9V_U4CJLVztVZQtFLTui8vuXXYx"
endpoint = "https://api.yelp.com/v3/"
headers = {'Authorization': 'Bearer %s' % apiKeyYelp}

apiKeyMap = "pk.eyJ1Ijoic2hlbGxleWhhbiIsImEiOiJjazNzeWw1MnYwN2V5M21teDl4cW40MzR0In0.BvL2yQuNXzZLALCfNbFnKg"
rest = ""
rid = []
box = None
rat = []

#Function to run the main query
def query():
    global rest
    try:
        params = {}
        params['location'] = userInput.get()
        params['term'] = userInput1.get()
        params['sort_by'] = sort[sortOption.get()]
        query1 = f'businesses/search'
        url1 = endpoint + query1
        a = requests.get(url1, params=params, headers=headers).json()
        rest = a['businesses']
    except:
        noti = tkinter.Toplevel()
        noti.title("Error")
        label = tkinter.Label(noti, text = "Something is wrong. Try again!")
        label.grid()
        button = tkinter.Button(noti, text = "Close", command = noti.destroy)
        button.grid()
    else:
        return

#Function to display list of restaurants in combo box
def main():
    global rid
    global box
    drop = []
    for i in range(len(rest)):
        drop.append('Restaurant: ' + rest[i]['name'] + '; Cuisine: ' + rest[i]['categories'][0]['title'] + '; Rating: ' + str(rest[i]['rating']))
        rid.append(rest[i]['id'])
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
    win.title("Price Rating Graph")
    win.geometry("700x700")
    figure1 = plt.Figure(figsize=(7,5), dpi=100, frameon="False")
    ax1 = figure1.add_subplot(111)
    bar1 = FigureCanvasTkAgg(figure1, win)
    bar1.get_tk_widget().grid(row = 0)
    df.plot(kind='bar', x= 'Restaurant', y = 'Price', color = 'green', ax = ax1)
    ax1.set_title("Price Rating of Each Restaurant in the List", fontsize = "10")
    ax1.set_ylabel("Price Rating", fontsize = "9")
    ax1.set_xlabel("Restaurant Name", fontsize = "9")
    ax1.tick_params(labelsize = '7')
    ax1.set_ylim(0,4,1)


#Function displays graph of price rating vs restaurant rating ratio for each restaurant in the list
def ratio():
    global rat
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
    rat = [round(i/j,2) for i, j in zip(p, ra)] 
    #Create a dataframe
    data1 = {'Restaurant':r, 'Rating': ra, 'Price':p, 'Ratio':rat}
    df1 = pd.DataFrame(data1)
    print(df1)
    
    #Create graph
    win = tkinter.Toplevel()
    win.title("Price Rating Graph")
    win.geometry("700x700")
    figure1 = plt.Figure(figsize=(7,5), dpi=100, frameon="False")
    ax1 = figure1.add_subplot(111)
    bar1 = FigureCanvasTkAgg(figure1, win)
    bar1.get_tk_widget().grid(row = 0)
    df1.plot(kind='bar', x= 'Restaurant', y = 'Ratio', color = 'green', ax=ax1)
    ax1.set_title("Price Rating vs Restaurant Rating Ratio for Each Restaurant in the List")
    ax1.set_ylabel("Price Rating vs Restaurant Rating Ratio")
    ax1.set_xlabel("Restaurant Name")
    ax1.tick_params(labelsize = '7')


    #Modify the range of y-axis based on the value to make the graph clearer
    if (df1['Ratio'] > 1).any() == False:
        ax1.set_ylim(0, 1.1, 0.1)
    elif (df1['Ratio'] > 1).any() == True and (df1['Ratio'] > 2).any() == False:
        ax1.set_ylim(0, 2.2, 0.2)
    elif (df1['Ratio'] > 2).any() == True and (df1['Ratio'] > 3).any() == False:
        ax1.set_ylim(0, 3.5, step=0.5)
    else:
        ax1.set_ylim(0, 4.5, step=0.5)

    for n,k in enumerate(df1['Ratio']):
        ax1.text(n-1, k+5, str(k),
                color = "black", transform=ax1.transAxes)

    # xlocs = plt.xticks()
    # xlocs=[i for i in range(0,20)]
    # plt.xticks(xlocs)
    # for k, v in enumerate(df1['Ratio']):     
    #     plt.text(xlocs[k]-0.125 , v + 0.01, str(v))
    # plt.show()

def query3():
    a = ""
    lst = []
    endpoint = "https://api.mapbox.com/styles/v1/mapbox/streets-v11/static"

    size = "500x800"
    # clong= "-122.4241"
    # clat= "37.78"
    # zoom= "14.25"
    # url = f"{endpoint}/{clong},{clat},{zoom}/{size}?access_token={apiKeyMap}"

    for i in range(len(rest)):
        if rat[i] >= 0.2 and rat[i] <= 0.5:
            lst.append(f"pin-s-{i}+008000({rest[i]['coordinates']['longitude']},{rest[i]['coordinates']['latitude']})")
        elif rat[i] > 0.5 and rat[i] <= 1:
            lst.append(f"pin-s-{i}+ffff1a({rest[i]['coordinates']['longitude']},{rest[i]['coordinates']['latitude']})")
        elif rat[i] > 1 and rat[i] <= 2:
            lst.append(f"pin-s-{i}+ff751a({rest[i]['coordinates']['longitude']},{rest[i]['coordinates']['latitude']})")
        else:
            lst.append(f"pin-s-{i}+e60000({rest[i]['coordinates']['longitude']},{rest[i]['coordinates']['latitude']})")

    for i in range(len(lst)-1):
        a = a + lst[i] + ","
    a = a + lst[20]
    print(a)

    url = f"{endpoint}/{a}/auto/{size}?access_token={apiKeyMap}"
    return url

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
    win = tkinter.Toplevel()
    win.title("Restaurant detail")
    win.geometry("800x500")
    query2 = f'businesses/'
    url2 = endpoint + query2 + rid[box.current()]
    a = requests.get(url2, headers=headers).json()
    label = tkinter.Label(win, text = f"Restaurant: {a['name']}")
    label.grid(sticky = "W")
    label1 = tkinter.Label(win, text = f"Phone: {a['display_phone']}")
    label1.grid(sticky = "W")
    label2 = tkinter.Label(win, text = f"Address: {a['location']['display_address'][0]}, {a['location']['display_address'][1]}")
    label2.grid(sticky = "W")
    #Avoid program to crash if there is no price information
    try:
        a['price']
    except:
        label3 = tkinter.Label(win, text = "No price information")
        label3.grid(sticky = "W")
    else:
        label3 = tkinter.Label(win, text = f"Price rating: {a['price']}")
        label3.grid(sticky = "W")
    #Avoid program to crash if there is no hours information
    try:
        a['hours']
    except:
        label4 = tkinter.Label(win, text = "No hours information")
        label4.grid(sticky = "W")
    else:
        label5 = tkinter.Label(win, text = f"Open now: {a['hours'][0]['is_open_now']}")
        label5.grid(sticky = "W")
        for z in range(len(a['hours'][0]['open'])):
            if a['hours'][0]['open'][z]['day'] == 0:
                label6 = tkinter.Label(win, text = f"Monday: {':'.join(a['hours'][0]['open'][z]['start'][i:i+2] for i in range(0, len(a['hours'][0]['open'][z]['start']), 2))} - {':'.join(a['hours'][0]['open'][z]['end'][i:i+2] for i in range(0, len(a['hours'][0]['open'][z]['end']), 2))}")
                label6.grid(sticky = "W")
            elif a['hours'][0]['open'][z]['day'] == 1:
                label7 = tkinter.Label(win, text = f"Tuesday: {':'.join(a['hours'][0]['open'][z]['start'][i:i+2] for i in range(0, len(a['hours'][0]['open'][z]['start']), 2))} - {':'.join(a['hours'][0]['open'][z]['end'][i:i+2] for i in range(0, len(a['hours'][0]['open'][z]['end']), 2))}")
                label7.grid(sticky = "W")
            elif a['hours'][0]['open'][z]['day'] == 2:
                label8 = tkinter.Label(win, text = f"Wednesday: {':'.join(a['hours'][0]['open'][z]['start'][i:i+2] for i in range(0, len(a['hours'][0]['open'][z]['start']), 2))} - {':'.join(a['hours'][0]['open'][z]['end'][i:i+2] for i in range(0, len(a['hours'][0]['open'][z]['end']), 2))}")
                label8.grid(sticky = "W")
            elif a['hours'][0]['open'][z]['day'] == 3:
                label9 = tkinter.Label(win, text = f"Thursday: {':'.join(a['hours'][0]['open'][z]['start'][i:i+2] for i in range(0, len(a['hours'][0]['open'][z]['start']), 2))} - {':'.join(a['hours'][0]['open'][z]['end'][i:i+2] for i in range(0, len(a['hours'][0]['open'][z]['end']), 2))}")
                label9.grid(sticky = "W")
            elif a['hours'][0]['open'][z]['day'] == 4:
                label10 = tkinter.Label(win, text = f"Friday: {':'.join(a['hours'][0]['open'][z]['start'][i:i+2] for i in range(0, len(a['hours'][0]['open'][z]['start']), 2))} - {':'.join(a['hours'][0]['open'][z]['end'][i:i+2] for i in range(0, len(a['hours'][0]['open'][z]['end']), 2))}")
                label10.grid(sticky = "W")
            elif a['hours'][0]['open'][z]['day'] == 5:
                label11 = tkinter.Label(win, text = f"Saturday: {':'.join(a['hours'][0]['open'][z]['start'][i:i+2] for i in range(0, len(a['hours'][0]['open'][z]['start']), 2))} - {':'.join(a['hours'][0]['open'][z]['end'][i:i+2] for i in range(0, len(a['hours'][0]['open'][z]['end']), 2))}")
                label11.grid(sticky = "W")
            else:
                label12 = tkinter.Label(win, text = f"Sunday: {':'.join(a['hours'][0]['open'][z]['start'][i:i+2] for i in range(0, len(a['hours'][0]['open'][z]['start']), 2))} - {':'.join(a['hours'][0]['open'][z]['end'][i:i+2] for i in range(0, len(a['hours'][0]['open'][z]['end']), 2))}")
                label12.grid(sticky = "W")
    long = a['coordinates']['longitude']
    lat = a['coordinates']['latitude']

    #Create textbox for user input of their location coordinates
    yourLoc = tkinter.Label(win, text="Enter your location:")
    yourLoc.grid(row = 0, column = 4, sticky = "W")
    name1 = tkinter.StringVar(None) #None = no default value; blank entry box
    userInput2 = tkinter.Entry(win, textvariable=name1, width=40) #Entry is always string
    userInput2.grid(row = 0, column = 5, sticky = "W")

    #Create button to show directions
    button3 = tkinter.Button(win, text="Show Directions", command=lambda:[direction(query1(long,lat,loc(userInput2.get())))])
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
        endpoint = "https://api.mapbox.com/directions/v5/mapbox/driving-traffic/" #/directions/v5/{profile}/{coordinates}
        query='.json?access_token='

        url = endpoint + coord + query + apiKeyMap + "&overview=full" + "&steps=true"
        r = requests.get(url).json()
        #Prevent program from crashing if coordinates are wrong
        if r['code'] == "InvalidInput":
            noti = tkinter.Toplevel()
            noti.title("Error")
            label = tkinter.Label(noti, text = "Something went wrong!")
            label.grid()
            button = tkinter.Button(noti, text = "Close", command = noti.destroy)
            button.grid()
        return r 
    #Prevent program from crashing if coordinates are wrong
    except:
        noti = tkinter.Toplevel()
        label = tkinter.Label(noti, text = "Something went wrong!")
        label.grid()
        button = tkinter.Button(noti, text = "Close", command = noti.destroy)
        button.grid()

#Function displays direction
def direction(r):
    window = tkinter.Toplevel()
    window.title("Directions")
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

#Create main window
root = tkinter.Tk()
root.title("List of Restaurants")
root.geometry("1200x1200")
root.resizable(True,True)

#Create textbox for user input of location
label = tkinter.Label(root, text = "Enter a city, state:")
label.grid(row=0, sticky = "W")
userInput = tkinter.Entry(root, width = 15)
userInput.grid(row=0, column = 1)

#Create textbox for user input of term
label1 = tkinter.Label(root, text = "Enter what you want to find:")
label1.grid(row = 1, sticky = "W")
userInput1 = tkinter.Entry(root, text="Restaurants, cuisines, food", width = 15)
userInput1.grid(row = 1, column = 1)

#Create radio button for sorting options
sort = ["best_match", "rating", "review_count", "distance"]
sortOption = tkinter.IntVar()
sortOption.set(0)
for x in range(len(sort)):
    r = tkinter.Radiobutton(root, text = sort[x], variable = sortOption, value = x)
    r.grid(row = 2, column = x)

#Create button to run query
button = tkinter.Button(root, text="Go!", command = lambda: [query(), main()])
button.grid (row = 1, column = 2)

#Create button to show price rating graph
button1 = tkinter.Button(root, text="Price rating", width = 15, command = lambda: [graph()])
button1.grid (row = 0, column = 6)

#Create button to show ratio graph
button2 = tkinter.Button(root, text="Ratio", width = 15, command = lambda: [ratio()])
button2.grid (row = 1, column = 6)

#Create button to show map
button3 = tkinter.Button(root, text="Map", width = 15, command = lambda: [mapp(query3())])
button3.grid (row = 2, column = 6)

#Create button to show restaurant details
button4 = tkinter.Button(root, text = "Show detail", width = 15, command = lambda: [detail()])
button4.grid(row = 3, column = 6)

#Display window
root.mainloop()
