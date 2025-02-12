#Importing libraries and other py files
import pygame
import sys
import random
import math
import Menu as menuFile
#import Player as playerFile
import GenerateDungeon as dungeonFile

#Initialisation  
pygame.init()
clock = pygame.time.Clock()

#Window Variables
windowDimensions = 1300, 720 #The dimensions that the window will be set to.  
gameName = "Echoes of the Deep" #The caption of the window.

#Game Variables
gameState = "mainMenu" #The state of the game

#Music Variables
gameMusicList = ["Soundtracks/Track02.wav", "Soundtracks/Track03.wav", "Soundtracks/Track04.wav"]  #Game music directories

#Screen
screen = pygame.display.set_mode(windowDimensions) #Pygame function to create the window to the specified width and height.  
pygame.display.set_caption(gameName) #Pygame function to set the window caption.
icon = pygame.display.set_icon(pygame.image.load('Assets\icon.png'))

def gameMusic(): #Stats playing the main menu music
    pygame.mixer.music.load(gameMusicList[random.randrange(0,3)]) #Load in one of the 3 game music files
    pygame.mixer.music.play(-1, 0, 2000) #Start playing


def saveStats(highScore, previousScore, difficulty, unsuccessfulRuns, successfulRuns):

    playerStatsFile = open('playerStats.txt', 'w') #Open File and then save data to the file

    playerStatsFile.write('High Score: ' + str(highScore) +
                          '\n' + 'Previous Score: ' + str(previousScore) +
                          '\n' + 'Unsuccessful Runs: ' + str(unsuccessfulRuns) +
                          '\n' + 'Successful Runs: ' + str(successfulRuns) +
                          '\n' + 'Difficulty: ' + str(difficulty))

    playerStatsFile.close()  #Close the file, prevents unwanted edits to the file

def eventHandler():
    global gameState

    checkButtons()

    for event in pygame.event.get(): #Checks for inputs
            
            if event.type == pygame.QUIT: #Check if quit pressed
                if gameState == "mainMenu":
                    closeGame()
                elif gameState == "Game":
                    gameState = "mainMenu"
                    pauseGame()

            if event.type == pygame.KEYDOWN: #Check if escape pressed
                if event.key == pygame.K_ESCAPE:
                    if gameState == "mainMenu":
                        closeGame()
                    elif gameState == "Game":
                        gameState = "Paused"
                        pauseGame()
                    elif gameState == "Paused":
                        gameState = "Game"
                        resumeGame()
    
    return gameState

def closeGame():
    pygame.quit()
    sys.exit()

def getMousePos():
    mousePos = pygame.mouse.get_pos() #Get the position of the mouse cursor

    return mousePos

def getMouseClick():
    mouseClick = pygame.mouse.get_pressed() #Detect when the player clicks

    return mouseClick

def checkButtons():
    global gameState
    mousePos = getMousePos()
    mouseClick = getMouseClick()

    if mousePos[0] > 100 and mousePos[0] < 375 and mousePos[1] > 275 and mousePos[1] < 365 and gameState == "mainMenu": #Check if mouse clicked play button
        if mouseClick[0] == 1:
            gameState = "Game"
            startGame()

    if mousePos[0] > 100 and mousePos[0] < 375 and mousePos[1] > 385 and mousePos[1] < 475 and gameState == "mainMenu": #Check if mouse clicked exit button
        if mouseClick[0] == 1:
            closeGame()

    if mousePos[0] > 350 and mousePos[0] < 920 and mousePos[1] > 508 and mousePos[1] < 608 and gameState == "gameOver": #Check if mouse clicked return to menu button
        if mouseClick[0] == 1:
            gameState = "mainMenu"
            Menu()

    if mousePos[0] > 520 and mousePos[0] < 743 and mousePos[1] > 330 and mousePos[1] < 400 and gameState == "Paused": #Check if mouse clicked resume button
        if mouseClick[0] == 1:
            gameState = "Game"
            resumeGame()

    if mousePos[0] > 485 and mousePos[0] < 775 and mousePos[1] > 430 and mousePos[1] < 500 and gameState == "Paused": #Check if mouse clicked quit game button
        if mouseClick[0] == 1:
            gameState = "gameOver"
            endGame()
    
    return gameState

def Menu(): #Initialisation of menu
    global gameState

    pygame.mixer.music.fadeout(750)
    menuFile.mainMenuMusic() #Play main menu music

    while gameState == "mainMenu": #Loop for when the player is on the mainMenu
        menuFile.mainMenu(screen).renderMenu(dungeonFile.difficulty, dungeonFile.highScore, dungeonFile.totalRuns, dungeonFile.successfulRuns) #Create the main menu
        sliders.sliderCheck(gameState) #Check sliders for changes
        dungeonFile.sfxVol = menuFile.getSfxVol()
        pygame.display.update() #Update the display
        eventHandler()

def startGame():
    dungeonFile.startGame()
    screen.fill(menuFile.colours["black"])  
    pygame.mixer.music.fadeout(750)
    gameMusic()
    dungeonFile.generateLevel()
    dungeonFile.spawnPlayer()
    Game()

def startLevel():
    screen.fill(menuFile.colours["black"])  
    pygame.mixer.music.fadeout(750)
    gameMusic()
    dungeonFile.generateLevel()
    dungeonFile.spawnPlayer()
    Game()

def resumeGame():
    screen.fill(menuFile.colours["black"])  
    pygame.mixer.music.unpause()
    Game()

def pauseGame():
    global gameState

    pygame.mixer.music.pause()

    while gameState == "Paused": #Loop for when the player is in a game
        menuFile.mainMenu(screen).renderPauseScreen()
        menuFile
        sliders.sliderCheck(gameState) #Check sliders for changes
        dungeonFile.sfxVol = menuFile.getSfxVol()
        pygame.display.update() #Update display
        eventHandler()

def Game():
    global gameState
    clock = pygame.time.Clock()
    
    while gameState == "Game": #Loop for when the player is in a game
        pygame.display.update() #Update display
        eventHandler()
        dungeonFile.update()
        if dungeonFile.player.hitpoints <= 0:
            gameState = "gameOver"
            endGame()
        screen.fill(menuFile.colours["black"])  
        dungeonFile.drawGame(screen)
        menuFile.mainMenu(screen).renderHUD(dungeonFile.player.hitpoints, dungeonFile.player.maxHitpoints, dungeonFile.score, dungeonFile.difficulty, dungeonFile.levelCount)
        areAllRoomsCompleted()
        pygame.display.update()

def endGame():
    pygame.mixer.music.fadeout(750)

    if dungeonFile.score > dungeonFile.highScore:
        dungeonFile.highScore = dungeonFile.score
    
    dungeonFile.unsuccessfulRuns += 1
    dungeonFile.totalRuns = dungeonFile.unsuccessfulRuns + dungeonFile.successfulRuns
    updateDifficulty(dungeonFile.score, dungeonFile.difficulty, dungeonFile.previousScore)

    saveStats(dungeonFile.highScore, dungeonFile.previousScore, dungeonFile.difficulty, dungeonFile.unsuccessfulRuns, dungeonFile.successfulRuns)

    dungeonFile.levelCount = 1

    while gameState == "gameOver": #Loop for when the player is in a game
        menuFile.mainMenu(screen).renderGameOver(dungeonFile.score, dungeonFile.highScore)
        pygame.display.update() #Update display
        eventHandler()

def areAllRoomsCompleted():
    #Iterates through each room
    for room in dungeonFile.rooms:
        #If a single room is found to be not completed, then return false
        if room.completed == False:
            return False
    #If no rooms left have been not completed, then return true
    newLevel()

def updateDifficulty(score, difficulty, previousScore):
    if score > previousScore and difficulty < 3:
        if score - previousScore >= 2000:
            difficulty += 1

    if previousScore > score and difficulty > -3:
        if previousScore - score >= 1999:
            difficulty -= 1

    print(previousScore)
    print(score)
    print(difficulty)
    dungeonFile.difficulty = difficulty
    dungeonFile.previousScore = dungeonFile.score

def newLevel():
    #Increments level by 1
    dungeonFile.levelCount += 1

    menuFile.mainMenu(screen).renderLevelComplete()
    pygame.display.update()

    #Restarts game
    startLevel()
    Game()

sliders = menuFile.sliderSetup(screen) #Initialise sliders

dungeonFile.loadStats()
Menu()