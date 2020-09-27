import tkinter
from tkinter import *
from PIL import ImageTk, Image
import json
      

root = Tk()
root.title("Map")
Image.MAX_IMAGE_PIXELS = 1024000000
# root.geometry("1000x1000")
# root.resizable(width=FALSE, height= FALSE)
canvas = Canvas(root, width=1000, height=1000)
canvas.pack()
canvas.configure(scrollregion=(-500, -500, 500, 500))

floor = Image.open("Blueprint/PISO -1.png")
# floorResized = ImageTk.PhotoImage(floor.resize((1000,1000)))
floorResized = floor.resize((1000,1000))
floorResized.save('resizedfloor.png')

locationIcon = Image.open("Blueprint/location_icon.png")

# floorResized.paste(locationIcon, (500, 400), locationIcon)
floorResized.paste(locationIcon, (761, 113), locationIcon)
# floorResized.paste(locationIcon, (724, 374), locationIcon)

with open('rooms.json', encoding="utf8") as json_file:
   data = json.load(json_file)
   for floor in data["floor"]:
      for room in data["floor"][floor]:
         for coord in data["floor"][floor][room]:
            floorResized.paste(locationIcon, (coord[0], coord[1]), locationIcon)

tkimage = ImageTk.PhotoImage(floorResized)
pinIcon = ImageTk.PhotoImage(locationIcon)


canvas.create_image(0, 0, anchor='center', image=tkimage)
# canvas.create_oval(-500, -500, 500, 500, fill="red")


# pin = Label(root, image=pinIcon).place(x=0,y=0)


root.mainloop()

