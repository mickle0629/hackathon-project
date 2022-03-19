import pygame, sys
pygame.init()
# Credit For Code: 
# https://www.geeksforgeeks.org/python-display-images-with-pygame/#:~:text=There%20are%20four%20basic%20steps,drawn%20on%20it%2C%20using%20image. 

# Var with white RGB
white = (255, 255, 255)
    
# Dimensions of image to display
display_surface = pygame.display.set_mode((1920, 1080))
  
# Assigning names to sprites
pygame.display.set_caption('Image')
pygame.display.set_caption('redImg')
  
# Make surface for the sprites to display onto
image = pygame.image.load(r'./hackathon-project/campus-map.jpg')
redImg = pygame.image.load(r'./hackathon-project/Red.png')

while True :  
    # Repeated image display for the loop at the requested coordinates
    display_surface.blit(image, (-384, -170))
    display_surface.blit(redImg, (500, 500))
    # gets the pygame event stuff
    # if event is QUIT, halt the program
    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
  
            # deactivates the pygame library
            pygame.quit()
  
            # quit the program.
            quit()
  
        # Draws the surface object to the screen.  
    pygame.display.update() 