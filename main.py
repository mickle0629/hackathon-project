# Various imports that were added automatically
from ctypes import pointer
from dis import dis
from multiprocessing.dummy import Array
from operator import add, truediv
from turtle import screensize, width
from typing import List
from venv import create
# manually added imports
import pygame, sys
import mysql.connector
from tkinter import*
# --------------------------------------------
# Works Cited/Referenced
# Code for displaying an image via Pygame: 
# https://www.geeksforgeeks.org/python-display-images-with-pygame/#:~:text=There%20are%20four%20basic%20steps,drawn%20on%20it%2C%20using%20image. 
# Code for DB Connection Stuff:
# https://www.w3schools.com/python/python_mysql_insert.asp 
# Tkinter Input Window Popup:
# https://python-course.eu/tkinter/entry-widgets-in-tkinter.php 
#---------------------------------------------
# Initializing pygame so we can use it
pygame.init()
# Pygame setup and variable declarations
myfont = pygame.font.SysFont("monospace", 15)
text = ""
file = pygame.image.load(r'./assets/Yellow.png')
eventype = ""
pull_id = 0

# Connecting to mySQL
mydb = mysql.connector.connect(
  host="192.9.227.213",
  user="hackathon",
  password="hackathon123",
  database = "hackathon1"
)
#Create event will be used following a series of user inputs to add the corresponding information to the database.
def createEvent(date, time, name, descr, location, Ev_type, mapx, mapy): # ID will be auto updated so it is not included
    mycursor = mydb.cursor()
    sql = "INSERT INTO Event_Info (Date, Time, Event_Name, Event_Descr, Event_Location, Event_Type, Map_X, Map_Y) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)" # SQL insert string
    val = (date, time, name, descr, location, Ev_type, mapx, mapy) # helps with the execute line
    mycursor.execute(sql, val)
    # Commit, then reinitialize arrays and update screen, which will place sprites at mapx and mapy
    mydb.commit()
    initilize_arrays()
    update_screen()

# initialize_arrays will grab all the current rows from the DB and assign ID, Type, X, and Y coordinates into an array of Tuples to be used later
# this will be used to update the array with new events
def initilize_arrays(): 
    mycursor = mydb.cursor()
    sql = "SELECT * FROM Event_Info" # SQL to grab all
    mycursor.execute(sql)
    rows = mycursor.fetchall() # Grab all the rows
    global ID_Coords # global so we can access it outside of the def
    ID_Coords = [None] * len(rows) 
    i = 0 # index val
    for row in rows: # array assignment
        ID_Coords[i] = (row[0], row[6], row[8], row[9])
        i += 1
# Dimensions of image to display
display_surface = pygame.display.set_mode((1920, 1080))
  
# Color assignments for later use // didnt end up using
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
  
# Variables we can call to display the sprites to a surface
map_background = pygame.image.load(r'./assets/campus-map.jpg')
official_icon = pygame.image.load(r'./assets/Red Event.png')
unofficial_icon = pygame.image.load(r'./assets/Green Event.png')
neutral_icon = pygame.image.load(r'./assets/Yellow Event.png')

#Adding the sprites for the buttons & Logos
addEventButton = pygame.image.load(r'./assets/AddEvent.png')
quitButton = pygame.image.load(r'./assets/QuitButton.png')
logo = pygame.image.load(r'./assets/Logo.png')

#Locations for the buttons
addEventButtonLocation = (1590, 5)
logoLocation = (1700, 5)
quitButtonLocation = (1810, 5)

# Print the map
display_surface.blit(map_background, (-384, -170))

#------TKINTER WINDOW POPUP SETUP-------# This was referenced code (view works cited at the top)
# Array that will store user input
userInput = [None] * 6
# Fields that will be displayed
fields = 'Date(YYYY-MM-DD', 'Time(HH:MM:SS)', 'Event Name', 'Description', 'Location', 'Type'

# Activates the popup on use, prompting the user for input
def popUp(mapx, mapy):
    root = Tk() # Core of Tk() is activated
    ents = makeform(root, fields) # make the window
    b1 = Button(root, text='Log', # make log button, if pressed insert info into array
                  command=(lambda e=ents: fetch(e, mapx, mapy)))
    b1.pack(side=LEFT, padx=5, pady=5) # padding
    # these two lines will essentially call fetch and makeForm below, I am not too sure how it works
    # the reference docs are vague with it
    master = Tk()
    master.mainloop()

# get the entries, insert into array via for loop
def fetch(entries, mapx, mapy): 
    i = 0 #index
    for entry in entries: # For every prompt in the pop up, grab the user input and assign it to an array
        text = entry[1].get()
        userInput[i] = text
        i += 1
    # at the end of the array, append the location of the cursor at this moment so the sprite can be placed in the right place
    userInput.append(mapx)
    userInput.append(mapy)
    createEvent(userInput[0], userInput[1], userInput[2], userInput[3], userInput[4], userInput[5], mapx, mapy) # SQL insert 

# makeForm from what I understand will format the box just a little bit, still looks janky
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

# Update screen will run through the array from initialize_array() and display all current events on the map
def update_screen():
    display_surface.blit(map_background, (-384, -170)) # Print the actual whitworth map first
    for i in ID_Coords: # For each index in the array, determine what type of event, then print the corresponding sprite
        event_type = str(i[1])
        if event_type == "Green":
            file = unofficial_icon
        elif event_type == "Red":
            file = official_icon
        else:
            file = neutral_icon
        display_surface.blit(file, (i[2] - 33, i[3] - 35)) # display done here
    
    #Adding the buttons
    display_surface.blit(quitButton, (quitButtonLocation))
    display_surface.blit(logo, (logoLocation))
    display_surface.blit(addEventButton, (addEventButtonLocation))
        
# Print result will print out the information related to the event that was clicked on
def print_result(ID):
    # Tkinter setup here
    master = Tk()
    # SQL stuff
    mycursor = mydb.cursor()
    sql = f"SELECT * FROM Event_Info WHERE ID={ID}"
    mycursor.execute(sql)
    result = mycursor.fetchone()
    # Data formatting to make it look more readable
    output = ["Date: %s\n" % result[1]]
    output.append("Time: %s\n" % result[2])
    output.append("Title: %s\n" % result[3])
    output.append("Location: %s\n" % result[5])
    output.append("Description: %s" % result[4])
    msg = Message(master, text = "".join(output))
    # Specific font stuff
    msg.config(bg='white', font=('times', 18, 'italic'), aspect = 200, relief = RAISED)
    msg.pack()
    mainloop() # tkinter command

# Update the screen and init arrays before running our main loop
initilize_arrays()
update_screen()

#----------MAIN LOOP HERE----------#
while True :  
    # Loop keeps running until quit button is pressed, or it is alt f4'd or an equivalent
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # deactivates the pygame library and quit program
            pygame.quit()
            quit()
        # Complex logic to determine what each given keypress will do
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
            if pos[0] >= addEventButtonLocation[0] and pos[0] <= addEventButtonLocation[0] + 105 and pos[1] >= addEventButtonLocation[1] and pos[1] <= addEventButtonLocation[1]+56:
                wait = True
                while wait == True:
                    ev = pygame.event.get()
                    for event in ev:
                        if event.type == pygame.MOUSEBUTTONUP:
                            newpos = pygame.mouse.get_pos()
                            mapx = newpos[0]
                            mapy = newpos[1]
                            popUp(mapx, mapy)
                            wait = False
            elif pos[0] >= quitButtonLocation[0] and pos[0] <= quitButtonLocation[0] + 105 and pos[1] >= quitButtonLocation[1] and pos[1] <= quitButton[1]+56:
                pygame.quit()
            else:
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
#----------------------------------#

