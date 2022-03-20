from dis import dis
from multiprocessing.dummy import Array
from operator import add
from turtle import screensize, width
from typing import List
from unittest import result
from venv import create
import pygame, sys
import mysql.connector
from tkinter import*
pygame.init()
myfont = pygame.font.SysFont("monospace", 15)
text = ""
file = pygame.image.load(r'./assets/Yellow.png')
eventype = ""
pull_id = 0
# --------------------------------------------
# Works Cited/Referenced
# Code for displaying an image via Pygame: 
# https://www.geeksforgeeks.org/python-display-images-with-pygame/#:~:text=There%20are%20four%20basic%20steps,drawn%20on%20it%2C%20using%20image. 
# Code for DB Connection Stuff:
# https://www.w3schools.com/python/python_mysql_insert.asp 
#---------------------------------------------
mydb = mysql.connector.connect(
  host="192.9.227.213",
  user="hackathon",
  password="hackathon123",
  database = "hackathon1"
)
#Create event will be used following a series of user inputs to add the corresponding information to the database.
def createEvent(date, time, name, descr, location, Ev_type, mapx, mapy): # People count and ID will be auto updated.
    mycursor = mydb.cursor()
    sql = "INSERT INTO Event_Info (Date, Time, Event_Name, Event_Descr, Event_Location, Event_Type, Map_X, Map_Y) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    val = (date, time, name, descr, location, Ev_type, mapx, mapy)
    mycursor.execute(sql, val)
    mydb.commit()
# Testing create event here:
# createEvent("2022-01-17", "5:23:00", "Elden Ring Party", "Failing to kill Godrick for 90 hours", "Ninth Circle of Hell", "Green", 340, 340)
# createEvent("2022-02-28", "4:23:00", "Pizza eating comp", "Making bad decisions and also diabeetus", "The Tunnels", "Yellow", 1020, 400)
# createEvent("2022-03-05", "1:30:00", "Doing coke in the hub", "Crackhead", "HUB", "Red", 1200, 1200)
def initilize_arrays():
    mycursor = mydb.cursor()
    sql = "SELECT * FROM Event_Info"
    mycursor.execute(sql)
    rows = mycursor.fetchall()
    global ID_Coords
    ID_Coords = [None] * len(rows)
    i = 0
    for row in rows:
        ID_Coords[i] = (row[0], row[6], row[8], row[9])
        i += 1
# Dimensions of image to display
display_surface = pygame.display.set_mode((1920, 1080))
  
# Var with white RGB
white = (255, 255, 255)
black = (0, 0, 0)    
themeGreen = (64, 84, 39)
themeWhite = (240, 241, 238)
eventGreen = (105, 153, 93)
eventYellow = (250, 185, 21)
eventRed = (152, 71, 63)

    
# Assigning names to sprites
pygame.display.set_caption('Image')
pygame.display.set_caption('redImg')
pygame.display.set_caption('greenImg')
pygame.display.set_caption('yellowImg')
  
# Make surface for the sprites to display onto
map_background = pygame.image.load(r'./assets/campus-map.jpg')
official_icon = pygame.image.load(r'./assets/Red Event.png')
unofficial_icon = pygame.image.load(r'./assets/Green Event.png')
neutral_icon = pygame.image.load(r'./assets/Yellow Event.png')

#Adding the sprites for the buttons
addEventButton = pygame.image.load(r'./assets/AddEvent.png')
clearEventsButton = pygame.image.load(r'./assets/ClearEvents.png')
quitButton = pygame.image.load(r'./assets/QuitButton.png')

#Locations for the buttons
addEventButtonLocation = (1590, 5)
clearEventsButtonLocation = (1700, 5)
quitButtonLocation = (1810, 5)

# Print the map
display_surface.blit(map_background, (-384, -170))
#------TKINTER WINDOW POPUP SETUP-------
userInput = [None] * 6
fields = 'Date(YYYY-MM-DD', 'Time(HH:MM:SS)', 'Event Name', 'Description', 'Location', 'Type'

def popUp():
    root = Tk()
    ents = makeform(root, fields)
    root.bind('<Return>', (lambda event, e=ents: fetch(e)))   
    b1 = Button(root, text='Log',
                  command=(lambda e=ents: fetch(e)))
    b1.pack(side=LEFT, padx=5, pady=5)

    master = Tk()
    master.mainloop()

def fetch(entries):
    i = 0
    for entry in entries:
        text = entry[1].get()
        userInput[i] = text
        i += 1
    print(userInput)
# createEvent(userInput[0], userInput[1], userInput[2], userInput[3], userInput[4], userInput[5], mapx, mapy)
def makeform(root, fields):
    entries = []
    for field in fields:
        row = Frame(root)
        lab = Label(row, width=15, text=field, anchor='w')
        ent = Entry(row)
        row.pack(side=TOP, fill=X, padx=5, pady=5)
        lab.pack(side=LEFT)
        ent.pack(side=RIGHT, expand=YES, fill=X)
        entries.append((field, ent))
    return entries
#---------------------------------------

def update_screen():
    display_surface.blit(map_background, (-384, -170))
    for i in ID_Coords:
        event_type = str(i[1])
        if event_type == "Green":
            file = unofficial_icon
        elif event_type == "Red":
            file = official_icon
        else:
            file = neutral_icon
        display_surface.blit(file, (i[2] - 33, i[3] - 35))
    
    #Adding the buttons
    display_surface.blit(quitButton, (quitButtonLocation))
    display_surface.blit(clearEventsButton, (clearEventsButtonLocation))
    display_surface.blit(addEventButton, (addEventButtonLocation))
        
def print_result(ID):
    master = Tk()
    mycursor = mydb.cursor()
    sql = f"SELECT * FROM Event_Info WHERE ID={ID}"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    print(result)
    msg = Message(master, text = result)
    msg.config(bg='lightgreen', font=('times', 24, 'italic'))
    msg.pack()
    mainloop()

initilize_arrays()
update_screen()
while True :  
    # Loop keeps running until closing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
  
            # deactivates the pygame library and quit program
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                while 1:
                    pygame.event.clear()
                    event = pygame.event.wait()
                    if event.type == pygame.KEYUP:
                        key_in = event.key
                        if key_in == pygame.K_RETURN:
                            break
                        elif key_in == pygame.K_SPACE:
                            text += " "
                        elif key_in == pygame.K_BACKSPACE:
                            text = text[0:-1]
                        else:
                            temp = pygame.key.name(key_in)
                            text += temp
                    text_display = myfont.render(text, 1, (255,255,0))
                    display_surface.blit(text_display, (500, 500))
                    pygame.display.update()
            elif event.key == pygame.K_t:
                popUp()

        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            temp = list(pos)
            for i in ID_Coords:
                if abs(i[2] - temp[0]) < 35:
                    for n in ID_Coords:
                        if abs(n[3] - temp[1]) < 35:
                            pull_id = n[0]
            if pull_id != 0:
                print_result(pull_id)   
                pull_id = 0
        # Draws the surface object to the screen.  
    pygame.display.update()