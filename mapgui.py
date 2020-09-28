import tkinter
from tkinter import *
from PIL import ImageTk, Image
import json
      

root = Tk()
root.title("Map")
frame = Frame(root)
frame.grid(column=0,row=0, sticky=(N,W,E,S) )
frame.columnconfigure(0, weight = 1)
frame.rowconfigure(0, weight = 1)
frame.pack()

choices = []

with open('rooms.json', encoding="utf8") as json_file:
   data = json.load(json_file)
   for floor in data["floor"]:
      for room in data["floor"][floor]:
         choices.append(room)

tkvar = StringVar(root)
tkvar.set('Galeria de acesso') # Default

popupMenu = OptionMenu(frame, tkvar, *choices)
popupMenu.pack()



Image.MAX_IMAGE_PIXELS = 1024000000
# root.geometry("1000x1000")
# root.resizable(width=FALSE, height= FALSE)

# Create canvas with size 1000x1000
canvas = Canvas(frame, width=1000, height=1000)
canvas.pack()
# canvas.configure(scrollregion=(-500, -500, 500, 500))

# Open image and resize to 1000x1000
floor = Image.open("Blueprint/PISO -1.png")
floorResized = floor.resize((1000,1000))

# Set pin icon
locationIcon = Image.open("Blueprint/location_icon.png")

tkimage = ImageTk.PhotoImage(floorResized)
pinIcon = ImageTk.PhotoImage(locationIcon)

canvas.create_image(0, 0, anchor=NW, image=tkimage)

def change_dropdown(*args):
   canvas.delete("roomPin")
   selectedRoom = tkvar.get()
   for floor in data["floor"]:
      for room in data["floor"][floor]:
         if (room == selectedRoom):
            for coord in data["floor"][floor][room]:
               canvas.create_image(coord[0], coord[1], anchor=NW, image=pinIcon, tags="roomPin")
            break

tkvar.trace('w', change_dropdown)

root.mainloop()

