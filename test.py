import io
from PIL import Image, ImageTk
import tkinter as tk
from urllib.request import urlopen
    


apiKeyMap = "pk.eyJ1Ijoic2hlbGxleWhhbiIsImEiOiJjazNzeWw1MnYwN2V5M21teDl4cW40MzR0In0.BvL2yQuNXzZLALCfNbFnKg"

endpoint = "https://api.mapbox.com/styles/v1/mapbox/streets-v11/static"

clong= "-122.4241"
clat= "37.78"
zoom= "14.25"

size = "600x600"

url = f"{endpoint}/{clong},{clat},{zoom}/{size}?access_token={apiKeyMap}"

root = tk.Tk()
image_bytes = urlopen(url).read()
data_stream = io.BytesIO(image_bytes)
pil_image = Image.open(data_stream)
tk_image = ImageTk.PhotoImage(pil_image)
label = tk.Label(root, image=tk_image, bg='brown')
label.grid()
root.mainloop()