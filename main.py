from venv import create
import pygame, sys
import mysql.connector
pygame.init()
myfont = pygame.font.SysFont("monospace", 15)
text = ""
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
def createEvent(date, time, name, descr, location, Ev_type): # People count and ID will be auto updated.
    mycursor = mydb.cursor()
    sql = "INSERT INTO Event_Info (Date, Time, Event_Name, Event_Descr, Event_Location, Event_Type) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (date, time, name, descr, location, Ev_type)
    mycursor.execute(sql, val)
    mydb.commit()
# Testing create event here:
# createEvent("2022-01-01", "3:00:00", "Smash Tournament", "Smashy Tourny", "Duvall", "Green")


# Var with white RGB
white = (255, 255, 255)
    
# Dimensions of image to display
display_surface = pygame.display.set_mode((1920, 1080))
  
# Assigning names to sprites
pygame.display.set_caption('Image')
pygame.display.set_caption('redImg')
pygame.display.set_caption('greenImg')
pygame.display.set_caption('yellowImg')
  
# Make surface for the sprites to display onto
map_background = pygame.image.load(r'./assets/campus-map.jpg')
official_icon = pygame.image.load(r'./assets/Red.png')
unofficial_icon = pygame.image.load(r'./assets/Green.png')
neutral_icon = pygame.image.load(r'./assets/Yellow.png')
# Print the map
display_surface.blit(map_background, (-384, -170))


label = myfont.render("Hello World!", 1, (255,255,0))

while True :  
    # Loop keeps running until closing
    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
  
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

        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            temp = list(pos)
            temp[0] -= 50
            temp[1] -= 50
            pos = tuple(temp)
            display_surface.blit(official_icon, (pos))
            display_surface.blit(label, (pos))


        # Draws the surface object to the screen.  
    pygame.display.update()