#Importing libraries and other py files
import pygame

pygame.init() #Initialise pygame

#Menu Variables & Dictionaries
fonts = {
    "title" : "Assets//Fonts//BernardMTCondensedRegular.ttf",
    "body" : "Assets//Fonts//RockwellCondensedBold.ttf"
}
colours = {
    "darkGray" : (20, 20, 20),
    "cyan" : (18, 213, 194),
    "red" : (204, 51, 37),
    "white" : (255, 255, 255),
    "black" : (0, 0, 0)
}

backgroundImg = pygame.image.load("Assets/Menu/Background.png") #Load & scale menu background image.  
backgroundImg = pygame.transform.scale(backgroundImg, (1300, 720))

sfxVol = 0

class mainMenu: #Main menu class to create and update the main menu

    def __init__(self, surface):
        self.surface = surface
    
    #Function to draw a button 
    def drawButtonRect(self, backColour, strokeColour, sizex, sizey, x, y):  
        pygame.draw.rect(self.surface, backColour, (x, y, sizex, sizey), 0) #Draw background rectangle

        for i in range(4): #Draws button stroke
            pygame.draw.rect(self.surface, strokeColour, (x - i, y - i, sizex + 5, sizey + 5), 1)  #Draw 4 rectangles around as a stroke 

    #Function to render text 
    def renderText(self, text, font, fontSize, fontColour, x, y): 
        textFont = pygame.font.Font(font, fontSize) #Create the font
        text = textFont.render(text, True, fontColour) #Render the text
        self.surface.blit(text, (x, y)) #Blit the text to the screen

    #Function to render text shadow 
    def renderTextShadow(self, text, font, fontSize, shadowColour, x, y, shadowOffset): 
        textFont = pygame.font.Font(font, fontSize) #Create the font
        text = textFont.render(text, True, shadowColour) #Render the text shadow
        self.surface.blit(text, (x + shadowOffset, y + shadowOffset))

    #Function to render all menu elements, besides the sliders
    def renderMenu(self, difficulty, highScore, totalRuns, successfulRuns):
        self.surface.fill(colours["black"]) #Fill screen black to remove any unwanted assets from the screen
        self.surface.blit(backgroundImg, (0, 0)) #Blit the background image to the screen

        self.renderTextShadow('ECHOES OF THE DEEP', fonts["title"], 165, colours["black"], 10, 20, 10) #Render the game title
        self.renderText('ECHOES OF THE DEEP', fonts["title"], 165, colours["white"], 10, 20) 

        self.drawButtonRect(colours["darkGray"], colours["cyan"], 350, 90, 125, 275) #Render the play button and its text
        self.renderTextShadow('PLAY', fonts["title"], 75, colours["black"], 240, 276, 5) 
        self.renderText('PLAY', fonts["title"], 75, colours["white"], 240, 276) 

        self.drawButtonRect(colours["darkGray"], colours["cyan"], 350, 90, 125, 385) #Render the exit button and its text
        self.renderTextShadow('EXIT', fonts["title"], 75, colours["black"], 244, 386, 5) 
        self.renderText('EXIT', fonts["title"], 75, colours["white"], 244, 386) 

        self.drawButtonRect(colours["darkGray"], colours["cyan"], 495, 5, 640, 350) #Render the player stats title
        self.renderTextShadow('PLAYER STATS:', fonts["body"], 90, colours["black"], 600, 271, 7) 
        self.renderText('PLAYER STATS:', fonts["body"], 90, colours["white"], 600, 271) 

        self.renderTextShadow('Difficulty: ' + str(difficulty + 3-3), fonts["body"], 50, colours["black"], 675, 390, 5) #Render the difficulty statistic
        self.renderText('Difficulty: ' + str(difficulty + 3-3), fonts["body"], 50, colours["white"], 675, 390) 

        self.renderTextShadow('High Score: ' + str(highScore), fonts["body"], 50, colours["black"], 675, 450, 5) #Render the high score statistic
        self.renderText('High Score: ' + str(highScore), fonts["body"], 50, colours["white"], 675, 450) 

        self.renderTextShadow('Total Runs: ' + str(totalRuns), fonts["body"], 50, colours["black"], 675, 510, 5) #Render the total runs statistic
        self.renderText('Total Runs: ' + str(totalRuns), fonts["body"], 50, colours["white"], 675, 510) 

        self.renderTextShadow('Successful Runs: ' + str(successfulRuns), fonts["body"], 50, colours["black"], 675, 570, 5) #Render the successful runs statistic
        self.renderText('Successful Runs: ' + str(successfulRuns), fonts["body"], 50, colours["white"], 675, 570)

    #Function to render the game over screen
    def renderPauseScreen(self):
        self.surface.fill(colours["black"]) #Fill screen black to remove any unwanted assets from the screen
        self.surface.blit(backgroundImg, (0, 0)) #Blit the background image to the screen

        self.renderTextShadow('ECHOES OF THE DEEP', fonts["title"], 120, colours["black"], 180, 20, 7) #Render the game title
        self.renderText('ECHOES OF THE DEEP', fonts["title"], 120, colours["white"], 180, 20) 
        self.drawButtonRect(colours["darkGray"], colours["cyan"], 950, 5, 165, 160) #Render

        self.renderTextShadow('PAUSED', fonts["title"], 95, colours["black"], 500, 180, 7) #Render the game over title
        self.renderText('PAUSED', fonts["title"], 95, colours["white"], 500, 180) 

        self.drawButtonRect(colours["darkGray"], colours["cyan"], 223, 70, 520, 345) #Render the return button and its text
        self.renderTextShadow('RESUME', fonts["title"], 60, colours["black"], 548, 435, 5) 
        self.renderText('RESUME', fonts["title"], 60, colours["white"], 548, 345)

        self.drawButtonRect(colours["darkGray"], colours["cyan"], 290, 70, 485, 445) #Render the return button and its text
        self.renderTextShadow('QUIT GAME', fonts["title"], 60, colours["black"], 509, 445, 5) 
        self.renderText('QUIT GAME', fonts["title"], 60, colours["white"], 509, 445)

    #Function to render the game over screen
    def renderGameOver(self, score, highScore):
        self.surface.fill(colours["black"]) #Fill screen black to remove any unwanted assets from the screen
        self.surface.blit(backgroundImg, (0, 0)) #Blit the background image to the screen

        self.renderTextShadow('ECHOES OF THE DEEP', fonts["title"], 120, colours["black"], 180, 20, 7) #Render the game title
        self.renderText('ECHOES OF THE DEEP', fonts["title"], 120, colours["white"], 180, 20) 
        self.drawButtonRect(colours["darkGray"], colours["cyan"], 950, 5, 165, 160) #Render

        self.renderTextShadow('GAME OVER', fonts["title"], 95, colours["black"], 420, 180, 7) #Render the game over title
        self.renderText('GAME OVER', fonts["title"], 95, colours["white"], 420, 180) 

        self.drawButtonRect(colours["darkGray"], colours["cyan"], 570, 100, 350, 508) #Render the return button and its text
        self.renderTextShadow('RETURN TO MENU', fonts["title"], 75, colours["black"], 407, 515, 5) 
        self.renderText('RETURN TO MENU', fonts["title"], 75, colours["white"], 407, 515)

        self.renderTextShadow('Score: ' + str(score), fonts["body"], 50, colours["black"], 375, 370, 4) #Render the difficulty statistic
        self.renderText('Score: ' + str(score), fonts["body"], 50, colours["white"], 375, 370) 

        self.renderTextShadow('High Score: ' + str(highScore), fonts["body"], 50, colours["black"], 630, 370, 4) #Render the high score statistic
        self.renderText('High Score: ' + str(highScore), fonts["body"], 50, colours["white"], 630, 370)
    
    def renderHUD(self, health, maxHealth, score, difficulty, levelCount):
        fillWidth = 175 * health / maxHealth

        self.drawButtonRect(colours["darkGray"], colours["cyan"], 175, 40, 50, 650) #Render
        pygame.draw.rect(self.surface, colours["red"], (51, 651, fillWidth, 40), 0) #Draw background rectangle

        self.renderTextShadow(str(health) + ' / ' + str(maxHealth), fonts["body"], 36, colours["black"], 70, 655, 3) #Render the game title
        self.renderText(str(health) + ' / ' + str(maxHealth), fonts["body"], 36, colours["white"], 70, 655) 

        self.renderTextShadow('DIFFICULTY:  ' + str(difficulty + 3), fonts["title"], 44, colours["black"], 1045, 655, 3) #Render the game title
        self.renderText('DIFFICULTY:  ' + str(difficulty + 3), fonts["title"], 44, colours["white"], 1045, 655) 

        self.renderTextShadow('Score: ' + str(score), fonts["title"], 44, colours["black"], 665, 20, 3) #Render the game title
        self.renderText('Score: ' + str(score), fonts["title"], 44, colours["white"], 665, 20) 

        self.renderTextShadow('Level: ' + str(levelCount), fonts["title"], 44, colours["black"], 500, 20, 3) #Render the game title
        self.renderText('Level: ' + str(levelCount), fonts["title"], 44, colours["white"], 500, 20) 

    def renderLevelComplete(self):
        self.renderTextShadow('LEVEL COMPLETE!', fonts["title"], 165, colours["black"], 140, 260, 10) #Render the game title
        self.renderTextShadow('LEVEL COMPLETE!', fonts["title"], 165, colours["black"], 140, 260, -10) #Render the game title
        self.renderText('LEVEL COMPLETE!', fonts["title"], 165, colours["white"], 140, 260) 

#Class to initialise a slider, as well as move, render and get
class Slider:
    def __init__(self, pos: list, size: tuple, initialValue : float, min: int, max: int, type, surface, sliderText, textx, texty):
        self.sliderType = type #Set slider type
        self.pos = pos #Set slider position

        self.size = size #Set slider size

        #Slider states
        self.hovered = False
        self.grabbed = False

        self.surface = surface #Set the surface for which the slider will be rendered on
        
        #Slider colour states
        self.buttonStates = {
        True:colours["white"],
        False:colours["cyan"]
        }

        self.sliderText = sliderText #Set slider text
        self.textx = textx #Set the x position of the slider text
        self.texty = texty #Set the y position of the slider text

        #Left, right, & top positions of the slider
        self.sliderLeftPos = self.pos[0] - (size[0]//2)
        self.sliderRightPos = self.pos[0] + (size[0]//2)
        self.sliderTopPos = self.pos[1] - (size[1]//2)

        #Set minimum, maximum and initial values for the slider
        self.min = min
        self.max = max
        self.initVal = initialValue
        self.initialValue  = (self.sliderRightPos - self.sliderLeftPos) * self.initVal  #Percentage value

        #Create the rectangles for the slider region and button
        self.containerRect = pygame.Rect(self.sliderLeftPos - 5, self.sliderTopPos, self.size[0] + 13, self.size[1] + 4)
        self.buttonRect = pygame.Rect(self.sliderLeftPos + self.initialValue - 5, self.sliderTopPos, 10, self.size[1])

        #Text Label
        self.text = pygame.font.Font(fonts["body"], 20).render(str(self.getValue()), True, colours["white"])
    
    #Function to move the slider
    def moveSlider(self, mouse_pos):
        pos = mouse_pos[0] #Set mouse position in the horizontal

        if pos < self.sliderLeftPos: #Check if mouse position is left of the slider
            pos = self.sliderLeftPos #Set slider left position to the mouse position

        if pos > self.sliderRightPos: #Check if mouse position is right of the slider
            pos = self.sliderRightPos #Set slider right position to the mouse position

        self.buttonRect.centerx = pos #Set slider centre position to the mouse position
    
    #Function to set hovered to True
    def hover(self):
        self.hovered = True
    
    #Function to render the slider
    def render(self):
        pygame.draw.rect(self.surface, colours["darkGray"], self.containerRect) #Draw slider region background
        pygame.draw.rect(self.surface, self.buttonStates[self.hovered], self.buttonRect) #Draw slider button
        for i in range(4): #Draw slider region stroke
            pygame.draw.rect(self.surface, colours["cyan"], (self.sliderLeftPos - i - 5, self.sliderTopPos - i,
                                                             self.size[0] + 13, self.size[1] + 4), 1)  
    #Function to get the value of the slider
    def getValue(self):
        global sfxVol

        valueRange = self.sliderRightPos - self.sliderLeftPos #Range of values
        buttonValue = self.buttonRect.centerx - self.sliderLeftPos #Button value
        
        value = int((buttonValue/valueRange)*(self.max-self.min)+self.min) #Actual value

        if self.sliderType == "musicVol": #Check if slider type is music
            pygame.mixer.music.set_volume(value/100) #Accordingly set music volume

        if self.sliderType == "sfxVol": #Check if slider type is music
            sfxVol = value/100
        
        self.initVal = value / 100
        return value #Return the value
    
    #Display the value of the slider
    def displayValue(self):
        mainMenu(self.surface).renderTextShadow(self.sliderText + str(int(self.getValue())),
                                                fonts["body"], 30, colours["black"], self.textx, self.texty, 3) #Render text shadow
        mainMenu(self.surface).renderText(self.sliderText + str(self.getValue()),
                                          fonts["body"], 30, colours["white"], self.textx, self.texty) #Render text

def getSfxVol():
    return sfxVol

#Class to create and check sliders
class sliderSetup:
    def __init__(self, surface):

        self.sliders = [
            Slider([208, 550], (150, 45), 0.5, 0, 100, 'musicVol', surface, 'Music Vol: ', 129, 493), #Create music volume slider
            Slider([398, 550], (150, 45), 0.5, 0, 100, 'sfxVol', surface, 'Sfx Vol: ', 335, 493) #Create sfx volume slider
        ]
            

        self.surface = surface #Set surface for the slider to drawn onto

    #Function to check the sliders for if they've been grabbed or are being hovered over
    def sliderCheck(self, gameState):
        mousePos = pygame.mouse.get_pos() #Get mouse position
        mouse = pygame.mouse.get_pressed() #Get mouse state


        for slider in self.sliders: #Loop through all sliders
            
            if gameState == "Paused" and slider.pos[0] < 400:
                slider.pos[0] += 326
                slider.pos[1] += 65
                slider.textx += 326
                slider.texty += 65
                slider.initialValue  = (slider.sliderRightPos - slider.sliderLeftPos) * slider.initVal
                slider.sliderLeftPos = slider.pos[0] - (slider.size[0]//2)
                slider.sliderRightPos = slider.pos[0] + (slider.size[0]//2)
                slider.sliderTopPos = slider.pos[1] - (slider.size[1]//2)
                slider.containerRect = pygame.Rect(slider.sliderLeftPos - 5, slider.sliderTopPos, slider.size[0] + 13, slider.size[1] + 4)
                slider.buttonRect = pygame.Rect(slider.sliderLeftPos + slider.initialValue - 5, slider.sliderTopPos, 10, slider.size[1])
            if gameState == "mainMenu" and slider.pos[0] > 400:
                slider.pos[0] -= 326
                slider.pos[1] -= 65
                slider.textx -= 326
                slider.texty -= 65
                slider.initialValue  = (slider.sliderRightPos - slider.sliderLeftPos) * slider.initVal
                slider.sliderLeftPos = slider.pos[0] - (slider.size[0]//2)
                slider.sliderRightPos = slider.pos[0] + (slider.size[0]//2)
                slider.sliderTopPos = slider.pos[1] - (slider.size[1]//2)
                slider.containerRect = pygame.Rect(slider.sliderLeftPos - 5, slider.sliderTopPos, slider.size[0] + 13, slider.size[1] + 4)
                slider.buttonRect = pygame.Rect(slider.sliderLeftPos + slider.initialValue - 5, slider.sliderTopPos, 10, slider.size[1])

            if slider.containerRect.collidepoint(mousePos): #Check if the mouse is colliding with the slider region
                
                if mouse[0]: #Check if mouse button left clicking is True
                    slider.grabbed = True #Set grabbed to True

            if not mouse[0]: #Check if the mouse is not clicking
                slider.grabbed = False #Set grabbed to False

            if slider.buttonRect.collidepoint(mousePos): #Check if the mouse is colliding with the slider button
                slider.hover() #Call the hover method of slider to set hovered to True

            if slider.grabbed: #Check if the slider is being grabbed
                slider.moveSlider(mousePos) #Call the mouseSlider method of slider to move the slider to the mouse position
                slider.hover() #Call the hover method of slider to set hovered to True
            else:
                slider.hovered = False #Otherwise set hovered to False

            slider.render() #Render the sliders
            slider.displayValue() #Display the slider text

def mainMenuMusic(): #Starts playing the main menu music
    pygame.mixer.music.load('Soundtracks/Track01.wav') #Load in the main menu music file
    pygame.mixer.music.play(-1, 0, 3000) #Play the music indefinitely

def drawHUD(screen, maxHitpoints, hitpoints):

    #Stores the background bar's width
    barWidth = 100
    #Stores the width of the fill bar
    #based on the percentage of the players hitpoints
    fillWidth = 100 * hitpoints / maxHitpoints

    #Draws both bars
    pygame.draw.rect(screen, (255, 0, 0), (170, 35, barWidth, 25))
    pygame.draw.rect(screen, (7, 186, 22), (170, 35, fillWidth, 25))

    #Draws text displaying hitpoints in numerical form
    hitpointsText = str(hitpoints) + "/" + str(maxHitpoints) + "hp"
    font = pygame.font.Font(fonts["body"], 24)
    image = font.render(hitpointsText, True, (255, 255, 255))
    screen.blit(image, (180, 40))