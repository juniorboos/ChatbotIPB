import tkinter
from tkinter import *
from PIL import ImageTk, Image
import json
      

root = Tk()
root.title("Map")
Image.MAX_IMAGE_PIXELS = 1024000000
# root.geometry("1000x1000")
# root.resizable(width=FALSE, height= FALSE)

# Create canvas with size 1000x1000
canvas = Canvas(root, width=1000, height=1000)
canvas.pack()
canvas.configure(scrollregion=(-500, -500, 500, 500))

# Open image and resize to 1000x1000
floor = Image.open("Blueprint/PISO -1.png")
floorResized = floor.resize((1000,1000))
floorResized.save('resizedfloor.png')

# Set pin icon
locationIcon = Image.open("Blueprint/location_icon.png")

choices = []

with open('rooms.json', encoding="utf8") as json_file:
   data = json.load(json_file)
   for floor in data["floor"]:
      for room in data["floor"][floor]:
         choices.append(room)
         for coord in data["floor"][floor][room]:
            floorResized.paste(locationIcon, (coord[0], coord[1]), locationIcon)

print(choices)
tkimage = ImageTk.PhotoImage(floorResized)
pinIcon = ImageTk.PhotoImage(locationIcon)

canvas.create_image(0, 0, anchor='center', image=tkimage)


root.mainloop()

