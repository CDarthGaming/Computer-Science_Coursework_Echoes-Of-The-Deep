import pygame, random, queue, os

from dataclasses import dataclass, field
from typing import Any

@dataclass(order=True)
class PrioritizedItem():
    priority: int
    item: Any=field(compare=False)

pygame.init()

#Constants
rows = 30
columns = 30
tileWidth = 10
scale = 10

#Stores directions
directions = {
    "left" : pygame.math.Vector2(-1, 0),
    "right" : pygame.math.Vector2(1, 0),
    "up" : pygame.math.Vector2(0, -1),
    "down" : pygame.math.Vector2(0, 1)
}

moveDirections = {
    "upLeft" : pygame.math.Vector2(-1, -1),
    "upRight" : pygame.math.Vector2(1, -1),
    "downLeft" : pygame.math.Vector2(-1, 1),
    "downRight" : pygame.math.Vector2(1, 1)
}

#Init
grid = []
rooms = []
entities = []
effects = []
player = None
levelCount = 1

score = 0
highScore = 0
previousScore = 0
totalRuns = 0
unsuccessfulRuns = 0
successfulRuns = 0
difficulty = 0

sfxVol = 0.5

#Stores the list of all tile types which entities cannot walk through
collidable = ["wall", "border", "player0", "lockedDoor", "enemy","health","loot0","loot1","loot2","loot3","loot4"]

#Stores all the different tile types within a list
tileTypesList = ["wall", "border", "floor", "player0", "door", "lockedDoor", "openDoor", "enemy0walk0","health","loot0","loot1","loot2","loot3","loot4"]

#Creates an empty dictionary for tile types
tileTypes = {}
#Iterates through each tileType within tileTypesList
for tileType in tileTypesList:
    #Forms the directory for the image of the tile to be accessed through concatenation
    directory = "Assets/DungeonTilemap/" + tileType + ".png"
    #Loads the image from the directory and scales it to a resolution of tileWidth x tileWidth pixels
    sprite = pygame.transform.scale(pygame.image.load(directory), (tileWidth * scale, tileWidth * scale))
    #Stores the sprite into the dictionary where its key is the name of the tileType
    tileTypes[tileType] = sprite

#Stores the list of all effect names and the number of frames they have
effectTypesList = {
    "hit" : 3,
    "death" : 4
}

#Creates an empty dictionary for effects to be stored within
effectTypes = {}

# Stores the list of all enemy types
enemyTypesList = ["enemy0", "enemy1", "enemy2", "enemy3"]

# Create an empty dictionary for enemy types
enemyTypes = {}

# Load enemy sprites and animations
for enemyType in enemyTypesList:
    enemyTypes[enemyType] = {
        "walkRight": [],
        "walkLeft": [],
        "attackRight": [],
        "attackLeft": []
    }
    
    # Load walk animation sprites
    for i in range(4):
        sprite = pygame.transform.scale(pygame.image.load(f"Assets/DungeonTilemap/{enemyType}walk{i}.png"), (tileWidth * scale, tileWidth * scale))
        enemyTypes[enemyType]["walkRight"].append(sprite)
        enemyTypes[enemyType]["walkLeft"].append(pygame.transform.flip(sprite, True, False))
    
    # Load attack animation sprites
    for i in range(2):
        sprite = pygame.transform.scale(pygame.image.load(f"Assets/DungeonTilemap/{enemyType}atk{i}.png"), (tileWidth * scale, tileWidth * scale))
        enemyTypes[enemyType]["attackRight"].append(sprite)
        enemyTypes[enemyType]["attackLeft"].append(pygame.transform.flip(sprite, True, False))

#Loads all the effects and organises them into a dictionary for later use
for effectType in effectTypesList:
    #Gets the number of frames of a particular type of effect
    numberOfFrames = effectTypesList[effectType]
    #Creates a list within the dictionary for the frames of the effect to be stored
    effectTypes[effectType] = []
    #Concatenates strings to form the directory of the folder which holds the effect frames
    folderDirectory = "Assets/effects/" + effectType + "/"
    #Loops through the individual frames within the folder
    for i in range(numberOfFrames):
        #Concatenates strings to form the directory of a frame 
        directory = folderDirectory + str(i) + ".png"
        #Loads the image from the directory as well as scaling the image to a resolution of tileWidth x tileWidth pixels
        sprite = pygame.transform.scale(pygame.image.load(directory), (tileWidth * scale, tileWidth * scale))
        #Stores the loaded sprite into the effectTypes dictionary 
        effectTypes[effectType].append(sprite)

#Stores list of sound names
soundNames = ["hit", "death", "roomComplete", "roomEnter"]

#Creates an empty dictionary for sound effects to be stored within
sounds = {}

#Loads all sound effects into the sounds dictionary
for soundName in soundNames:
    #Forms the directory for the particular sound to be loaded
    directory = "Assets/sfx/" + soundName + ".wav"
    #Stores the sound within the dictionary as a PyGame sound object
    sounds[soundName] = pygame.mixer.Sound(directory)

musicEnabled = True
soundEnabled = False

def loadStats():
    #Importing values from the program to the function
    global highScore, previousScore, unsuccessfulRuns, successfulRuns, difficulty

    if not os.path.isfile('playerStats.txt'): #Check if file exists
        playerStatsFile = open("playerStats.txt", "x") #Create file
        playerStatsFile.write('High Score: ' + str(0) #Write empty values to the file
                              + '\n' + 'Previous Score: ' + str(0) 
                              + '\n' + 'Unsuccessful Runs: ' + str(0) 
                              + '\n' + 'Successful Runs: ' + str(0) 
                              + '\n' + 'Difficulty: ' + str(0))
        playerStatsFile.close() #Close the file

    playerFile = open('playerStats.txt', 'r') #Open playerStats file
    for line in playerFile: #Check all lines in the file and get the values
        if 'High Score: ' in line: 
            highScore = int(line.replace('High Score: ', '')) 
        if 'Previous Score: ' in line: 
            previousScore = int(line.replace('Previous Score: ', ''))
        if 'Unsuccessful Runs: ' in line:
            unsuccessfulRuns = int(line.replace('Unsuccessful Runs: ', ''))
        if 'Successful Runs: ' in line:
            successfulRuns = int(line.replace('Successful Runs: ', ''))
        if 'Difficulty: ' in line:
            difficulty = int(line.replace('Difficulty: ', ''))
    playerFile.close() #Close the file

    totalRuns = unsuccessfulRuns + successfulRuns

    return highScore, previousScore, totalRuns, unsuccessfulRuns, successfulRuns, difficulty #Return the new values to the program 

class Tile():
    def __init__(self, x, y, tileType):
        self.x = x
        self.y = y
        self.tileType = tileType

    def getSprite(self):
        #Fetches the sprite from the tileTypes dictionary
        if self.tileType == "player":
            return player.getSprite()
        else:
            return tileTypes[self.tileType]

    #Draws tile
    def draw(self, screen):
        #Stores the result of the player being within bounds as a boolean
        xInBounds = player.x - 6.25 <= self.x <= player.x + 6.25
        yInBounds = player.y - 4 <= self.y <= player.y + 4

        #If both conditions are not met, then do not draw the tile
        if not(xInBounds and yInBounds): return
        
        #Calls the getSprite method to fetch the tile's sprite
        sprite = self.getSprite()
        #Gets the offset to position the focus towards the player
        offset = getOffset()
        #Converts the 2D array coordinates to position measured in pixels
        position = (self.x * tileWidth * scale + offset.x, self.y * tileWidth * scale + offset.y)

        #Draws the sprite at specified position
        screen.blit(sprite, position)

    def getNeighbours(self):
        neighbours = []
        for direction in directions.items():
            xNew = int(self.x + direction[1].x)
            yNew = int(self.y + direction[1].y)
            
            xInBounds = 1 <= xNew <= columns - 2
            yInBounds = 1 <= yNew <= rows - 2

            if not (xInBounds and yInBounds): continue
            
            neighbourTile = grid[yNew][xNew]
            neighbours.append(neighbourTile)
            
        return neighbours

    def getCost(self):
        if self.tileType == "floor":
            return 1
        elif self.tileType == "wall":
            return 5
        elif self.tileType == "health":
            return 999
        elif self.tileType == "loot0":
            return 999
        elif self.tileType == "loot1":
            return 999
        elif self.tileType == "loot2":
            return 999
        elif self.tileType == "loot3":
            return 999
        elif self.tileType == "loot4":
            return 999
        elif self.tileType == "border":
            return 999

class Effect(Tile):
    def __init__(self, x, y, tileType, frames):
        #Inherits method and attributes from the tile class
        super().__init__(x, y, tileType)

        #Stores the frames that the object will cycle through
        #throughout its lifetime
        self.frames = frames.copy()

        #Stores the lifetime of the effect based on the number of frames
        self.timer = len(self.frames) * 3
        self.initialTimer = self.timer

    def getSprite(self):
        #Get the current frame of the effect relative to how long the effect
        #has been around for
        frame = (self.initialTimer - self.timer) // 3
        #Returns the sprite that has been fetched
        return self.frames[frame]

    def update(self):
        #Decrements the timer
        self.timer -= 1
        #If the timer has reached 0 then remove the effect from the game
        if self.timer <= 0:
            effects.remove(self)

#The entity class defines an object which can move around the level and attack other entities.
class Entity(Tile):
    #Takes in coordinates and tileType as parameters to be used
    #in the constructor method
    def __init__(self, x, y, tileType):
        #Inherits method and attributes from the tile class
        super().__init__(x, y, tileType)

        #The hitpoints attribute is decreased when the entity
        #attacked by other entities
        self.maxHitpoints = 0
        self.hitpoints = self.maxHitpoints
        #The power attribute determines the damage that
        #this entity can deal to other entities
        self.power = 1

    #Moves the entity in a direction
    def move(self, direction):
        #Sets the x attribute of the entity according to the x component of the direction vector object
        self.x += int(direction.x)
        #Sets the y attribute of the entity according to the y component of the direction vector object
        self.y += int(direction.y)

    def getTargetEntity(self, direction):
        x = self.x + direction.x
        y = self.y + direction.y
        for entity in entities:
            if entity.x == x and entity.y == y:
                return entity

    def willCollide(self, x, y):
        for entity in entities:
            if entity.x == x and entity.y == y and entity != self:
                return True
        return False

    def attack(self, targetEntity):
        #Deducts hitpoints from the target entity
        targetEntity.hitpoints -= self.power
        #Calls the create effect function
        createEffect(targetEntity.x, targetEntity.y, "hit")
        #Plays hit sound
        playSound("hit")
        
#The health class defines the health object which can heal the player.
class Health(Entity):
    def __init__(self, x, y, tileType, room):
        #Inherits methods and attributes from parent class
        super().__init__(x, y, tileType)
        #Ensures tile type is "health"
        self.tileType = "health"
        #Stores the room the health has spawned 
        self.room = room

        #Set attributes of the enemy according to the level count
        global levelCount
        self.hitpoints = 1

    def update(self):
        global score

        if self.hitpoints <= 0:
            #Increasing health
            player.hitpoints += random.randint(16, 35) + (5 * levelCount) + (5 * difficulty)
            if player.hitpoints > player.maxHitpoints:
                player.hitpoints = player.maxHitpoints

            #Remove all references of object
            entities.remove(self)
            self.room.loot.remove(self)

            score += 25 + (8 * difficulty) + (25 * levelCount) #Increase score upon collect
        
#The lootlvl1 class defines the level 1 loot object that the play can collect for score.
class LootLvl1(Entity):
    def __init__(self, x, y, tileType, room):
        super().__init__(x, y, tileType) #Inherits methods and attributes from parent class

        self.tileType = "loot0" #Sets the tiletype
        self.room = room #Stores the room the object has spawned 
        self.hitpoints = 2 #Health of the object

    def update(self):
        global score

        if self.hitpoints <= 0:
            #Increasing score
            score += 50 + (-8 * difficulty)

            #Remove all references of object
            entities.remove(self)
            self.room.loot.remove(self)
        
#The lootlvl2 class defines the level 1 loot object that the play can collect for score.
class LootLvl2(Entity):
    def __init__(self, x, y, tileType, room):
        super().__init__(x, y, tileType) #Inherits methods and attributes from parent class

        self.tileType = "loot1" #Sets the tiletype
        self.room = room #Stores the room the object has spawned 
        self.hitpoints = 3 #Health of the object

    def update(self):
        global score

        if self.hitpoints <= 0:
            #Increasing score
            score += 100 + (-16 * difficulty)

            #Remove all references of object
            entities.remove(self)
            self.room.loot.remove(self)
        
#The lootlvl3 class defines the level 1 loot object that the play can collect for score.
class LootLvl3(Entity):
    def __init__(self, x, y, tileType, room):
        super().__init__(x, y, tileType) #Inherits methods and attributes from parent class

        self.tileType = "loot2" #Sets the tiletype
        self.room = room #Stores the room the object has spawned 
        self.hitpoints = 5 #Health of the object

    def update(self):
        global score

        if self.hitpoints <= 0:
            #Increasing score
            score += 200 + (-32 * difficulty)

            #Remove all references of object
            entities.remove(self)
            self.room.loot.remove(self)
        
#The lootlvl4 class defines the level 1 loot object that the play can collect for score.
class LootLvl4(Entity):
    def __init__(self, x, y, tileType, room):
        super().__init__(x, y, tileType) #Inherits methods and attributes from parent class

        self.tileType = "loot3" #Sets the tiletype
        self.room = room #Stores the room the object has spawned 
        self.hitpoints = 10 #Health of the object

    def update(self):
        global score

        if self.hitpoints <= 0:
            #Increasing score
            score += 500 + (-64 * difficulty)

            #Remove all references of object
            entities.remove(self)
            self.room.loot.remove(self)
        
#The lootlvl5 class defines the level 1 loot object that the play can collect for score.
class LootLvl5(Entity):
    def __init__(self, x, y, tileType, room):
        super().__init__(x, y, tileType) #Inherits methods and attributes from parent class

        self.tileType = "loot4" #Sets the tiletype
        self.room = room #Stores the room the object has spawned 
        self.hitpoints = 20 #Health of the object

    def update(self):
        global score

        if self.hitpoints <= 0:
            #Increasing score
            score += 2000 + (250 * levelCount)

            #Remove all references of object
            entities.remove(self)
            self.room.loot.remove(self)
        
#The enemy class defines the enemy object which inherits methods and attributes from the entity class
class Enemy(Entity):
    def __init__(self, x, y, tileType, room):
        #Inherits methods and attributes from parent class
        super().__init__(x, y, tileType)
        #Ensures tile type is "enemy"
        self.tileType = "enemy"
        #Stores the room the enemy has spawned 
        self.room = room
        #Cooldown for enemy movement/attacks
        self.defaultActionTimer = 20 + -1 * difficulty
        self.actionTimer = self.defaultActionTimer

        #Set attributes of the enemy according to the level count
        global levelCount
        self.hitpoints = int((4 + difficulty) + (levelCount / 1.75))
        self.power = int(levelCount / 3)
        if self.power == 0:
            self.power = 1
        if self.hitpoints == 0:
            self.hitpoints = 1

        # Randomly choose an enemy type
        self.enemyType = random.choice(enemyTypesList)
        self.sprites = enemyTypes[self.enemyType]
        self.facing = "right"
        self.animationIndex = 0
        self.animationSpeed = self.defaultActionTimer
        self.lastState = "walk"

    def update(self):
        global score
        
        if self.actionTimer > 0:
            #Decrements the action timer
            self.actionTimer -= 1
        else:
            #Calls the decide action method
            self.decideAction()

        if self.hitpoints <= 0:
            #Create death effect and play death sound
            createEffect(self.x, self.y, "death")
            playSound("death")

            #Increasing score
            score += 75 + (10 * difficulty) + (25 * levelCount)

            #Spawn loot
            self.room.spawnLoot(self.x, self.y)

            #Remove all references of enemy
            entities.remove(self)
            self.room.enemies.remove(self)

        self.animate()

    def animate(self):
        if self.lastState == "walk":
            self.walkAnimate()
        elif self.lastState == "atk":
            self.attackAnimate()

    def walkAnimate(self):
        if self.actionTimer > 0 and self.lastState == "walk":
            self.animationIndex += 1
            if self.animationIndex >= (len(self.sprites["walkRight"]) * self.animationSpeed):
                self.animationIndex = 0

    def attackAnimate(self):
        if self.actionTimer > 0 and self.lastState == "atk":
            self.animationIndex += 1
            if self.animationIndex >= (len(self.sprites["attackRight"]) * self.animationSpeed):
                self.animationIndex = 0

    def getSprite(self):
        if self.lastState == "atk":
            if self.facing == "left":
                return self.sprites["attackLeft"][self.animationIndex // self.animationSpeed]
            else:
                return self.sprites["attackRight"][self.animationIndex // self.animationSpeed]
        elif self.lastState == "walk":
            if self.facing == "left":
                return self.sprites["walkLeft"][self.animationIndex // self.animationSpeed]
            else:
                return self.sprites["walkRight"][self.animationIndex // self.animationSpeed]

    def getDirection(self):
        #Returns a vector based on the player's position from the enemy
        if self.x > player.x:
            self.facing = "left"
            return directions["left"]
        elif self.x < player.x:
            self.facing = "right"
            return directions["right"]
        elif self.y < player.y:
            return directions["down"]
        elif self.y > player.y:
            return directions["up"]

    def getWalkDirection(self):
        #Returns a vector based on the player's position from the enemy
        if self.x > player.x and self.y > player.y:
            self.facing = "left"
            return moveDirections["upLeft"]
        elif self.x < player.x and self.y > player.y:
            self.facing = "right"
            return moveDirections["upRight"]
        elif self.x > player.x and self.y < player.y:
            self.facing = "left"
            return moveDirections["downLeft"]
        elif self.x > player.x and self.y < player.y:
            self.facing = "right"
            return moveDirections["downRight"]
        elif self.x > player.x:
            self.facing = "left"
            return directions["left"]
        elif self.x < player.x:
            self.facing = "right"
            return directions["right"]
        elif self.y < player.y:
            return directions["down"]
        elif self.y > player.y:
            return directions["up"]

    def decideAction(self):
        self.lastx = self.x
        self.lasty = self.y
        self.lastMovement = "vertical"

        #Resets the action timer
        self.actionTimer = self.defaultActionTimer
        #Gets direction of the player
        direction = self.getWalkDirection()

        #Gets the target entity
        targetEntity = self.getTargetEntity(direction)

        #Gets the tile at that direction
        nextTile = grid[int(self.y + direction.y)][int(self.x + direction.x)]
        #Checks if the enemy will collide with another entity at that tile's position
        if self.willCollide(nextTile.x, nextTile.y):
            #If it does and the entity it has collided into is a player
            if targetEntity == player:
                if direction.x != 0 and direction.y != 0:
                    direction = self.getDirection()
                    self.move(direction)
                    self.lastState = "walk"
                else:
                    #Then call the attack method while passing in the player object
                    self.attack(player)
                    self.lastState = "atk"
        else:
            #Calls the move method with the direction calculated
            self.move(direction)
            self.lastState = "walk"

def createEffect(x, y, effectType):
    #Creates effect object at the given coordinates
    effect = Effect(x, y, "effect", effectTypes[effectType])
    #Stores the effect in a list as a reference
    effects.append(effect)

#The player class defines the player object which inherits methods and attributes from the entity class.
#It also defines its own methods and attributes that is specific to the player.
class Player(Entity):
    #Takes in coordinates and tileType as parameters to be used in the constructor method
    def __init__(self, x, y, tileType):
        #Inherits method and attributes from the entity class
        super().__init__(x, y, tileType)
        #Sets the tileType attribute to "player" as the player object
        self.tileType = "player"
        self.facing = "right"
        self.atk = False
        self.lastState = "walk"

        #This attribute is used as a cooldown on moving the player
        self.defaultMoveTimer = 12 + 2 * difficulty
        self.moveTimer = self.defaultMoveTimer
        self.defaultAttackTimer = 16
        self.attackTimer = self.defaultAttackTimer

        #Redefines hitpoints for the player
        self.maxHitpoints = 65 + (-10 * difficulty) + ((7 + (levelCount*2)) * (levelCount - 1))
        self.hitpoints = self.maxHitpoints

        self.power = 1 + int(levelCount / 5)


        self.spritesRight = []
        for i in range(4):
            self.spritesRight.append(pygame.transform.scale(pygame.image.load("Assets/DungeonTilemap/player" + str(i) + ".png"), (tileWidth * scale, tileWidth * scale)))
        self.spritesLeft = []
        for sprite in self.spritesRight:
            self.spritesLeft.append(pygame.transform.flip(sprite, True, False))

        self.animationIndex = 0
        self.animationSpeed = self.defaultMoveTimer

        self.spritesRightAttack = []
        for i in range(2):
            self.spritesRightAttack.append(pygame.transform.scale(pygame.image.load("Assets/DungeonTilemap/playeratk" + str(i) + ".png"), (tileWidth * scale, tileWidth * scale)))
        self.spritesLeftAttack = []
        for sprite in self.spritesRightAttack:
            self.spritesLeftAttack.append(pygame.transform.flip(sprite, True, False))

        self.attackAnimationIndex = 0
        self.attackAnimationSpeed = self.defaultAttackTimer

    #Gets the player's movement-related key presses and executes methods depending on the input
    def getDirection(self):
        direction = None

        #Gets all the keys pressed and executes the move method with the direction associated with it
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and keys[pygame.K_w]:
            direction = moveDirections["upLeft"]
        elif keys[pygame.K_d] and keys[pygame.K_w]:
            direction = moveDirections["upRight"]
        elif keys[pygame.K_a] and keys[pygame.K_s]:
            direction = moveDirections["downLeft"]
        elif keys[pygame.K_d] and keys[pygame.K_s]:
            direction = moveDirections["downRight"]
        elif keys[pygame.K_a]:
            direction = directions["left"]
        elif keys[pygame.K_d]:
            direction = directions["right"]
        elif keys[pygame.K_w]:
            direction = directions["up"]
        elif keys[pygame.K_s]:
            direction = directions["down"]

        return direction
    
    def doAction(self):
        print(self.moveTimer)
        #Decrements the cooldowns 
        if self.moveTimer > 0:
            self.moveTimer -= 1

        if self.attackTimer > 0:
            self.attackTimer -= 1

        #Gets direction based on player input
        direction = self.getDirection()

        if direction == directions["left"]:
            self.facing = "left"
        elif direction == directions["right"]:
            self.facing = "right"

        if direction:
            #Gets the entity that the player may walk into
            targetEntity = self.getTargetEntity(direction)

            #If the entity does not exist then move towards direction
            if self.moveTimer <= 0 and not targetEntity:
                #MoveTimer attribute set to 20 once the player moves
                self.moveTimer = self.defaultMoveTimer
                #Calls move method
                self.move(direction)
                self.lastState = "walk"
            #If the entity does exist then attack entity towards direction
            elif self.attackTimer <= 0 and targetEntity:
                self.attackTimer = self.defaultAttackTimer
                self.attack(targetEntity)
                self.lastState = "atk"

    #This move method has been redefined to account for collisions with walls and the movement cooldown
    def move(self, direction):
        self.x += int(direction.x)
        self.y += int(direction.y)

        #Gets the tile from the 2D array at the new position of the player
        nextTile = grid[self.y][self.x]
        #If the tileType of the tile classifies as a colidable tile, then the movement is reversed
        if self.willCollide(nextTile.x, nextTile.y) or nextTile.tileType in collidable:
            self.x -= int(direction.x)
            self.y -= int(direction.y)

    def update(self):
        self.doAction()
        if self.lastState == "atk":
            self.attackAnimate()
        if self.lastState == "walk":
            self.walkAnimate()

    def walkAnimate(self):
        # Update the animation index based on the movement
        if self.moveTimer > 0 and self.lastState == "walk":
            self.animationIndex += 1
            if self.animationIndex >= (len(self.spritesRight) * self.animationSpeed):
                self.animationIndex = 0

    def attackAnimate(self):
    # Update the animation index based on the attack
        if self.attackTimer > 0 and self.lastState == "atk":
            self.attackAnimationIndex += 1
            if self.attackAnimationIndex >= (len(self.spritesRightAttack) * self.attackAnimationSpeed):
                self.attackAnimationIndex = 0

    def getSprite(self):
        # Get the current sprite based on the facing direction and animation index
        if self.lastState == "atk":
            if self.facing == "left":
                return self.spritesLeftAttack[self.attackAnimationIndex // self.attackAnimationSpeed]
            else:
                return self.spritesRightAttack[self.attackAnimationIndex // self.attackAnimationSpeed]
        if self.lastState == "walk":
            if self.facing == "left":
                return self.spritesLeft[self.animationIndex // self.animationSpeed]
            else:
                return self.spritesRight[self.animationIndex // self.animationSpeed]
            
class Room():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width 
        self.height = height

        self.enemies = []
        self.loot = []
        self.borders = []
        self.floors = []

        for row in range(self.height):
            for col in range(self.width):
                tile = grid[self.y + row][self.x + col]
                if tile.tileType == "border":
                    self.borders.append(tile)
                elif tile.tileType == "floor":
                    self.floors.append(tile)

        self.door = self.getRandomBorderTile()
        self.active = False
        self.completed = False
        self.lootSpawned = False

    def isRoomOverlapping(self, x, y, width, height):
        for row in range(height + 2):
            for col in range(width + 2):
                xInBounds = self.x - 1 <= x + col <= self.x + self.width + 1
                yInBounds = self.y - 1 <= y + row <= self.y + self.height + 1

                if xInBounds and yInBounds: return True

    def getSpawnTile(self):
        #Calculates coordinates of random tile within the room
        x = self.x + random.randint(1, self.width - 2)
        y = self.y + random.randint(1, self.height - 2)
        while x == player.x and y == player.y:
            x = self.x + random.randint(1, self.width - 2)
            y = self.y + random.randint(1, self.height - 2)            
        #Gets the tile from the coordinates
        tile = grid[y][x]
        #Returns the tile
        return tile

    def unlockRoom(self):
        self.door.tileType = "openDoor"
        self.spawnHealth()

        for i in range(0, (int(difficulty * levelCount/2))):
            spawnTile = self.getSpawnTile()
            self.spawnLoot(spawnTile.x, spawnTile.y)

        self.lootSpawned = True

    def completeRoom(self):
        self.completed = True
        self.active = False

        #Plays complete sound
        playSound("roomComplete")
            
    def activateRoom(self):
        self.active = True
        self.door.tileType = "lockedDoor"
        self.spawnEnemies()

        #Plays room enter sound
        playSound("roomEnter")

    def spawnEnemies(self):
        global levelCount
        chances = [0, 1, 2, 3]
        chance = random.choice(chances)
        if not chance == 0:
            number = random.randint(0, 1) + int(difficulty/3) + int(levelCount/3)
            for i in range(number):        
                #Gets the spawn tile
                spawnTile = self.getSpawnTile()
                #Creates an enemy object
                enemy = Enemy(spawnTile.x, spawnTile.y, "enemy", self)
                #Appends it to the entities list
                entities.append(enemy)
                #Appends it to the room's enemy list
                self.enemies.append(enemy)

    def spawnHealth(self):
        spawnChance = 3
        chanceNum = random.randint(0, 10)
        lvlCountNum = int(levelCount/5)
        if lvlCountNum == 0:
            lvlCountNum = 1
        for i in range(0, lvlCountNum):
            if chanceNum >= spawnChance and levelCount == 3:
                spawnTile = self.getSpawnTile()
                health = Health(spawnTile.x, spawnTile.y, "health", self)
                entities.append(health)
                self.loot.append(health)

    def spawnLoot(self, x, y):
        chances = [1, 0.6, 0.377, 0.2, 0.1, 0.003, -1]
        chosenItem = ((random.randrange(0, 100000)) / 100000)
        print(chosenItem)

        if chosenItem <= chances[0] and chosenItem > chances[1]:
            return
        elif chosenItem <= chances[1] and chosenItem > chances[2]:
            print("lvl1 loot")
            lootItem = LootLvl1(x, y, "loot0", self)
        elif chosenItem <= chances[2] and chosenItem > chances[3]:
            print("lvl2 loot")
            lootItem = LootLvl2(x, y, "loot1", self)
        elif chosenItem <= chances[3] and chosenItem > chances[4]:
            print("lvl3 loot")
            lootItem = LootLvl3(x, y, "loot2", self)
        elif chosenItem <= chances[4] and chosenItem > chances[5]:
            print("lvl4 loot")
            lootItem = LootLvl4(x, y, "loot3", self)
        elif chosenItem <= chances[5] and chosenItem > chances[6]:
            print("lvl5 loot")
            lootItem = LootLvl5(x, y, "loot4", self)

        if chosenItem <= chances[1]:
            entities.append(lootItem)
            self.loot.append(lootItem)

    def isContainingPlayer(self):
        xInBounds = self.x < player.x < self.x + self.width - 2
        yInBounds = self.y < player.y < self.y + self.height - 2

        return xInBounds and yInBounds

    #Runs every frame
    def update(self):
        #Checks if the room has not been visited and if
        #the player is inside the room
        if self.completed == False and self.isContainingPlayer() and self.active == False:
            #Actives the room (locks the door, spawns enemies)
            self.activateRoom()

        #Checks if the room is currently active and that there are no more enemies remaining
        if self.active == True and self.lootSpawned == False and len(self.enemies) == 0:
            #Spawns loot and unlocks the door
            self.unlockRoom()

        #Checks if the room is currently active and that there is no more loot remaining
        if self.completed == False and self.lootSpawned == True and len(self.loot) == 0:
            #Completes the room
            self.completeRoom()

        updateElements(self.enemies)
        updateElements(self.loot)

    def getRandomBorderTile(self):
        return random.choice(self.borders)

def playSound(soundName):
    #Accesses a sound object from the sounds dictionary and plays it
    sounds[soundName].set_volume(sfxVol)
    sounds[soundName].play()

def getOffset():
    #Calculates the offset relative to the player using the constants, scale and tilewidth.
    offset = pygame.math.Vector2(-player.x * scale * tileWidth + 6 * scale * tileWidth,
                                 -player.y * scale * tileWidth + 3.25 * scale * tileWidth)
    #Returns offset calculated 
    return offset
            
def drawGrid(screen):
    for row in range(rows):
        for col in range(columns):
            tile = grid[row][col]
            tile.draw(screen)

def generateLevel():
    global grid, rooms, entities, levelCount, rows, columns
    
    grid = []
    rooms = []
    entities = []

    #Increase room size as the level count increases
    rows = 15 + int(2 * levelCount)
    columns = 15 + int(2 * levelCount)
    
    for row in range(rows):
        grid.append([])
        for col in range(columns):
            tile = Tile(col, row, "wall")
            grid[row].append(tile)

    count = 0
    while True:
        if generateRoom() == "stop": break
        count += 1

    for i in range(len(rooms)):
        if i == 0: continue
        generateCorridor(rooms[i], rooms[i - 1])

    #Iterates through all the rooms
    for room in rooms:
        #Sets the tiletype of the entry point of each room to "door"
        room.door.tileType = "door"
        

def isRoomOverlapping(x, y, width, height):
    for room in rooms:
        if room.isRoomOverlapping(x, y, width, height): return True

def calculateRoomPositionAndSize():
    width = random.randint(5, (10 + (1*int(levelCount / 2))))
    height = random.randint(5, (10 + (1*int(levelCount / 2))))
    x = random.randint(2, columns - 2 - width)
    y = random.randint(2, rows - 2 - height)

    return width, height, x, y

def generateRoom():
    tries = 0
    width, height, x, y = calculateRoomPositionAndSize()
    while isRoomOverlapping(x, y, width, height):
        tries += 1
        if tries >= 500: return "stop"
        width, height, x, y = calculateRoomPositionAndSize()
    
    for row in range(height):
        for col in range(width):
            tile = grid[y + row][x + col]
            tile.tileType = "border"

    for row in range(height - 2):
        for col in range(width - 2):
            tile = grid[y + row + 1][x + col + 1]
            tile.tileType = "floor"

    grid[y][x].tileType = "wall"
    grid[y + height - 1][x].tileType = "wall"
    grid[y][x + width - 1].tileType = "wall"
    grid[y + height - 1][x + width - 1].tileType = "wall"

    room = Room(x, y, width, height)
    rooms.append(room)

    grid[y][x].tileType = "border"
    grid[y + height - 1][x].tileType = "border"
    grid[y][x + width - 1].tileType = "border"
    grid[y + height - 1][x + width - 1].tileType = "border"

def getDistanceFromTiles(tile1, tile2):
    tile1Pos = pygame.Vector2(tile1.x, tile1.y)
    tile2Pos = pygame.Vector2(tile2.x, tile2.y)
    distance = tile1Pos.distance_to(tile2Pos)
    return distance

def aStar(startTile, goalTile):
    frontier = queue.PriorityQueue()
    frontier.put(PrioritizedItem(0, startTile))
    
    cameFrom = dict()
    costSoFar = dict()
    cameFrom[startTile] = None
    costSoFar[startTile] = 0

    while not frontier.empty():   
        currentTile = frontier.get().item

        for nextTile in currentTile.getNeighbours():
            if nextTile == goalTile: return cameFrom, currentTile
            
            newCost = costSoFar[currentTile] + nextTile.getCost()
            
            if nextTile not in costSoFar or newCost < costSoFar[nextTile]:
                costSoFar[nextTile] = newCost
                cameFrom[nextTile] = currentTile
                
                priority = newCost + getDistanceFromTiles(nextTile, goalTile) 
                frontier.put(PrioritizedItem(priority, nextTile))

def generateCorridor(room1, room2):
    #Calculates path from room1's door to room2's door
    cameFrom, currentTile = aStar(room1.door, room2.door)
    #Backtracks the dictionary returned

    while currentTile in cameFrom:
        #Turns each tile within the dictionary into a floor
        currentTile.tileType = "floor"
        currentTile = cameFrom[currentTile]
    
    #The tile type of the entry point for both rooms are set to "floor"
    room1.door.tileType = "floor"
    room2.door.tileType = "floor"

#Function to get the first non-collidable tile
def getNextEmptyTile():
    #Iterates through the 2D array
    for row in range(rows):
        for col in range(columns):
            #Gets the tile at a position
            tile = grid[row][col]
            #Checks if the tile is not collidable, if it isn't then return
            #the tile whereas if it is collidable, then check the next tile
            if tile.tileType not in collidable:
                return tile

#Procedure which calls the draw method of every entity
def drawEntities(screen):
    #Loops through all entities
    for entity in entities:
        #Calls each entity's draw method
        entity.draw(screen)

def drawEffects(screen):
    for effect in effects:
        effect.draw(screen)

#Draws all the necessary components within the game
def drawGame(screen):
    #Draws the 2D array grid in a graphically representable form
    drawGrid(screen)
    #Draws entities on-top of the grid
    drawEntities(screen)
    #Draws effects on-top of entities
    drawEffects(screen)

def updateElements(elements):
    for element in elements:
        element.update()

def update():
    updateElements(rooms)
    updateElements(effects)
    player.update()

def spawnPlayer():
    global player
    
    #Gets the next empty tile
    spawnTile = getNextEmptyTile()
    #Instantiates a player object at position (5, 5)
    player = Player(spawnTile.x, spawnTile.y, "player")
    #Appends the player object into the entities list
    entities.append(player)

def startGame():
    global levelCount, score
    score = 0

pygame.quit()