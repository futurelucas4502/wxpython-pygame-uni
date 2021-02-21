from pygame.locals import *
import pygame
import entities
import main
import random
import json
import configparser


class Game():
    def __init__(self):
        pygame.init()
        # Check if config is valid
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

        # Set screen information
        self.width = 1280
        self.height = 720
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Game")

        # Set font and fps clock sky and start level
        self.font = pygame.font.SysFont("Arial", 18)
        self.clock = pygame.time.Clock()
        self.sky = (173, 216, 230)
        self.level = 1

        # Set grid size to a 16:9 aspect ratio as my resolution is divisible by 8 and dividing by 8 * 10 would give me a perfect 16:9 but i want more tiles so we do 8 * 5
        self.tileMultiplier = 5
        self.tileSize = 8 * self.tileMultiplier
        self.tileWidth = self.width // self.tileSize
        self.tileHeight = self.height // self.tileSize

        # Prepare level assets which are 80x80 to use whatever grid_size scale we're using (use convert with non transparent and convert_alpha with transparent)
        self.grass = pygame.transform.scale(pygame.image.load(
            "assets/grass.png").convert(), (self.tileSize, self.tileSize))
        self.dirt = pygame.transform.scale(pygame.image.load(
            "assets/dirt.png").convert(), (self.tileSize, self.tileSize))
        self.key = pygame.transform.scale(pygame.image.load(
            "assets/key.png").convert_alpha(), (self.tileSize, self.tileSize))

        # Make player
        self.player = entities.Player((self.tileSize, self.tileSize*2), (0, self.height - self.tileSize*3))

        self.debug = False

        # Generate new world
        if self.config['settings']['experimental'] == "False":
            if self.worldGen():
                main.gameRun = False
        else:
            self.randWorldGen()

        # Finally Start game
        self.start()

    def randWorldGen(self):
        ''' Random world generation maybe to be added in the future very unfinished '''
        # Create an array with air gap at the top so that player can move at top of map
        array = [[0]*(self.tileWidth)]
        for row in range((self.tileHeight) - 3):
            subarray = []
            for tile in range(self.tileWidth):
                randNum = random.randint(0, 10)
                if randNum == 2:
                    subarray.append(randNum)
                else:
                    subarray.append(0)
            array.append(subarray)
        # So air gap above floor
        array.append([0]*(self.tileWidth))
        # So floor is solid
        array.append([2]*(self.tileWidth))

        self.world = array

    def worldGen(self):
        try:
            with open(f'levels/level{self.level}at{self.tileMultiplier}.json') as f:
                data = json.load(f)
                self.world = data
        except Exception as error:
            print(error)
            main.error = "No (more) level's found"
            return True

    def drawWorld(self):
        self.screen.fill(self.sky)
        try:
            # 9 rows in grid
            for row in range(self.tileHeight):
                # 16 columns in each row
                for tile in range(self.tileWidth):
                    # If current position in grid is 1 then it should be a grass block so show grass block
                    if self.world[row][tile] == 1:
                        self.screen.blit(
                            self.grass, (tile * self.tileSize, row * self.tileSize))
                    elif self.world[row][tile] == 2:
                        self.screen.blit(
                            self.dirt, (tile * self.tileSize, row * self.tileSize))
                    elif self.world[row][tile] == 3:
                        self.screen.blit(
                            self.key, (tile * self.tileSize, row * self.tileSize))
        except Exception as error:
            print(error)
            main.error = "It's possible worlds.json has invalid levels"
            return True

    def start(self):
        while main.gameRun:
            self.clock.tick(60)  # max fps is 60

            # Move player pos
            self.player.update(self.screen, self.screen.get_size()[1] - self.tileSize)

            # Draw world
            if self.drawWorld():
                main.gameRun = False

            # Draw the player on the screen
            self.screen.blit(self.player.image, self.player.rect)

            # Debugging
            if self.debug:
                self.drawGrid()
                self.screen.blit(self.updateFPS(), (10, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # pygame.QUIT == the x button on the window
                    main.gameRun = False

                elif event.type == pygame.KEYDOWN:  # Press down and handle the button press
                    if event.key == pygame.K_p:
                        # Debug on or off
                        self.debug = not self.debug

            # PyGame renders using a double buffer so draws the data hidden first then displays it after
            pygame.display.update()

        pygame.display.quit()
        pygame.quit()

    def drawGrid(self):
        for x in range(self.tileWidth):
            for y in range(self.tileHeight):
                pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(x*self.tileSize, y*self.tileSize,
                                                                           self.tileSize, self.tileSize), 1)

    def updateFPS(self):
        fps = str(int(self.clock.get_fps()))
        return self.font.render(fps, 1, (255, 255, 255))
