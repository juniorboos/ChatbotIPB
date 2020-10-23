import nltk
from nltk.stem import WordNetLemmatizer
import pickle
import numpy as np
import sqlite3
from datetime import datetime
import numpy as np
import json
from keras.models import load_model
from PIL import ImageTk
import PIL.Image
import json
import random
import locale
import speech_recognition as sr

import pyttsx3
engine = pyttsx3.init()

locale.setlocale(locale.LC_TIME, 'pt_PT')

r = sr.Recognizer()

lemmatizer = WordNetLemmatizer()
conn = sqlite3.connect('tutorial.db')
c = conn.cursor()
model = load_model('chatbot_model.h5')
intents = json.loads(open('intents.json', encoding='utf-8').read())
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))

global global_context
global_context = []

with open('rooms.json', encoding="utf8") as json_file:
      data = json.load(json_file)

def clean_up_sentence(sentence):
   # tokenize the pattern - split words into array
   sentence_words = nltk.word_tokenize(sentence)
   # stem each word - create short form for word
   sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
   return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence

def bow(sentence, words, show_details=True):
   # tokenize the pattern
   sentence_words = clean_up_sentence(sentence)
   # bag of words - matrix of N words, vocabulary matrix
   bag = [0]*len(words)  
   for s in sentence_words:
      for i,w in enumerate(words):
         if w == s: 
               # assign 1 if current word is in the vocabulary position
               bag[i] = 1
               if show_details:
                  print ("found in bag: %s" % w)
   return(np.array(bag))

context = {}

def predict_class(sentence, model):
   # filter out predictions below a threshold
   p = bow(sentence, words,show_details=False)
   res = model.predict(np.array([p]))[0]
   ERROR_THRESHOLD = 0.25
   results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
   # sort by strength of probability
   results.sort(key=lambda x: x[1], reverse=True)
   return_list = []
   for r in results:
      return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
   return return_list

def getResponse(message, ints, intents_json, userID='123', show_details=True):
   tag = ints[0]['intent']
   # print(tag)
   list_of_intents = intents_json['intents']
   for i in list_of_intents:
      if(i['tag']== tag):
         # print(i)
         # set context for this intent if necessary
         if 'context' in i:
            if show_details: print ('context:', i['context'])
            context[userID] = i['context']
            global global_context
            global_context = context[userID]
         # check if this intent is contextual and applies to this user's conversation
         if 'context_filter' in i:
            print('Tem um contexto: ', i['context_filter'])
            # if (i['context_filter'] == 'search_class_by_student'):
            #     c.execute('SELECT login FROM docente WHERE nome = ?', (name,))
            #     data = c.fetchone()
            #     print(data[0])
            #     result = 'Your login is ' + data[0]
            #     return result
         if not 'context_filter' in i or \
            (userID in context and 'context_filter' in i and i['context_filter'] == context[userID]):
            if show_details: 
               print ('tag:', i['tag'])
               print ('User context: ', context[userID])
            # a random response from the intent
            # if (tag == 'class_search'):
            #     print ('Message: ', message)
               # c.execute('SELECT login FROM docente WHERE nome = ?', (message,))
               # data = c.fetchone()
               # print(data[0])
               # result = data[0]
               # print(i)
            result = random.choice(i['responses'])
         break
   return result


def search_class_by_student(msg):
   print("Entrouuuuuu")
   c.execute('SELECT LOGIN FROM docente WHERE NOME = ?', (msg,))
   data = c.fetchone()
   print(data[0])
   c.execute('SELECT ID_AULA FROM aula_docente WHERE LOGIN = ?', (data[0],))
   # data = c.fetchall()
   data = c.fetchone()
   # newData = tuple(np.array([np.array(x[0]) for x in data]))
   print(data[0])
   # print(newData[0])
   c.execute('SELECT ID_SALA, INICIO, FIM FROM aula WHERE ID = ?', (data[0],))
   dataAula = c.fetchone()
   print(dataAula)
   
   dataInicio = datetime.strptime(dataAula[1], '%Y-%m-%d %H:%M:%S')
   dataFim = datetime.strptime(dataAula[2], '%Y-%m-%d %H:%M:%S')
   c.execute('SELECT NOME FROM sala WHERE id = ?', (dataAula[0],))
   dataSala = c.fetchone()
   # c.close
   # conn.close()
   res = 'Sua aula começa ' + dataInicio.strftime('%A') + ' às ' + dataInicio.strftime('%H:%M') + ' no local ' + dataSala[0]
   print(res)
   return res

def chatbot_response(msg):
   print('---------')
   global global_context
   print('GLOBAL: ', global_context)
   if (global_context == ['search_class_by_student']):
      print('search_class_by_student')
      res = search_class_by_student(msg)
      print('Res: '+res)
      global_context = []
      return res
   if (global_context == ['search_classroom_by_number']):
      print('search_classroom_by_number')
      global_context = []
      floor = searchRoom(msg)
      if (floor != False):
         res = msg+' fica no piso '+floor+'.'
      else:
         res = 'Não foi possível encontrar, tente novamente.'
      return res
   else:
      print('else')
      ints = predict_class(msg, model)
      res = getResponse(msg, ints, intents)
      return res


#Creating GUI with tkinter
import tkinter
from tkinter import *


def send():
   global global_context

   if global_context == ['search_class_by_student']:
      msg = EntryBox.get("1.0",'end-1c').strip()
      EntryBox.delete("0.0",END)
   else:
      with sr.Microphone() as source:
         # read the audio data from the default microphone
         audio_data = r.record(source, duration=4)
         print("Recognizing...")
         # convert speech to text
         msg = r.recognize_google(audio_data, language="pt-BR")
         print(msg)

   if msg != '':
      ChatLog.config(state=NORMAL)
      ChatLog.insert(END, "You: " + msg + '\n\n')
      ChatLog.config(foreground="#442265", font=("Verdana", 12 ))
   
      res = chatbot_response(msg)
      ChatLog.insert(END, "Bot: " + res + '\n\n')
         
      ChatLog.config(state=DISABLED)
      ChatLog.yview(END)

      engine.say(res)
      engine.runAndWait()
 

def searchRoom(msg):
   canvas.delete("roomPin")
   # selectedRoom = tkvar.get()
   for floor in data["floor"]:
      for room in data["floor"][floor]:
         if (room.lower() == msg.lower()):
            print("Blueprint/PISO "+floor+".png")
            # floorImage = PIL.Image.open("Blueprint/PISO "+floor+".png")
            # floorResized = floorImage.resize((1000,1000))
            # tkimage = ImageTk.PhotoImage(master=base, image=floorResized)
            canvas.create_image(0, 0, anchor=NW, image=tkimage[floor])
            for coord in data["floor"][floor][room]:
               canvas.create_image(coord[0], coord[1], anchor=NW, image=pinIcon, tags="roomPin")
            return floor
            break
   return False

base = Tk()
base.title("Hello")
base.geometry("1400x1000")
base.resizable(width=FALSE, height=FALSE)

#Create Chat window
ChatLog = Text(base, bd=0, bg="white", height="8", width="50", font="Arial",)

ChatLog.config(state=DISABLED)

#Bind scrollbar to Chat window
scrollbar = Scrollbar(base, command=ChatLog.yview, cursor="heart")
ChatLog['yscrollcommand'] = scrollbar.set

#Create Button to send message
SendButton = Button(base, font=("Verdana",12,'bold'), text="Send", width="12", height=5,
                    bd=0, bg="#32de97", activebackground="#3c9d9b",fg='#ffffff',
                    command= send )

#Create the box to enter message
EntryBox = Text(base, bd=0, bg="white",width="29", height="5", font="Arial")
#EntryBox.bind("<Return>", send)

canvas = Canvas(base, width=1000, height=1000)

#Place all components on the screen
scrollbar.place(x=376,y=6, height=886)
ChatLog.place(x=6,y=6, height=886, width=370)
EntryBox.place(x=128, y=901, height=90, width=265)
SendButton.place(x=6, y=901, height=90)
canvas.place(x=400, y=0, height=1000, width=1000)

PIL.Image.MAX_IMAGE_PIXELS = 1024000000
# Open image and resize to 1000x1000
# floor = "-1"
tkimage={}
floorImage = PIL.Image.open("Blueprint/PISO -1.png")
floorResized = floorImage.resize((1000,1000))
tkimage["-1"] = ImageTk.PhotoImage(master=base, image=floorResized)
floorImage = PIL.Image.open("Blueprint/PISO 0.png")
floorResized = floorImage.resize((1000,1000))
tkimage["0"] = ImageTk.PhotoImage(master=base, image=floorResized)
# floorResized.save('resized piso 0.png')
# Set pin icon
locationIcon = PIL.Image.open("Blueprint/location_icon.png")

# tkimage = ImageTk.PhotoImage(master=base, image=floorResized)
pinIcon = ImageTk.PhotoImage(master=base, image=locationIcon)

# canvas.create_image(0, 0, anchor=NW, image=tkimage)

base.mainloop()
