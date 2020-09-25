import tkinter
from tkinter import *
from PIL import ImageTk, Image

root = Tk()
root.title("Map")
Image.MAX_IMAGE_PIXELS = 1024000000
# root.geometry("960x720")
# root.resizable(width=FALSE, height= FALSE)

my_img = Image.open("PISO-1-Model2.png")
resized = ImageTk.PhotoImage(my_img.resize((1000,1000)))

my_label = Label(image=resized)
my_label.pack()


root.mainloop()

