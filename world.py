import main
import pygame
import random
import configparser
import ast


class World():
    def __init__(self, game):
        # Check if config is valid
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

        # Create tile info
        self.tileWidth = game.width // game.tileSize
        self.tileHeight = game.height // game.tileSize
        self.tileSize = game.tileSize

        # Prepare level assets which are 80x80 to use whatever grid_size scale we're using (use convert with non transparent and convert_alpha with transparent)
        self.grass = pygame.transform.scale(pygame.image.load(
            "assets/grass.png").convert(), (self.tileSize, self.tileSize))
        self.dirt = pygame.transform.scale(pygame.image.load(
            "assets/dirt.png").convert(), (self.tileSize, self.tileSize))
        self.key = pygame.transform.scale(pygame.image.load(
            "assets/key.png").convert_alpha(), (self.tileSize, self.tileSize))
        self.doorTop = pygame.transform.scale(pygame.image.load(
            "assets/doorTop.png").convert_alpha(), (self.tileSize, self.tileSize))
        self.doorBottom = pygame.transform.scale(pygame.image.load(
            "assets/doorBottom.png").convert_alpha(), (self.tileSize, self.tileSize))

        # Set sky colour
        self.sky = (173, 216, 230)

        # Create a tile rect from any tile
        self.tileRect = self.grass.get_rect()

        # Generate new world
        if self.config['settings']['experimental'] == "False":
            if self.worldGen(game):
                main.gameRun = False
        else:
            self.randWorldGen()

    def randWorldGen(self):
        ''' Random world generation maybe to be added in the future very unfinished and could probably be optimised a lot also look into using perlin noise for level generation '''
        # Create an array with air gap at the top so that player can move at top of map
        array = [[0]*(self.tileWidth)]
        for row in range((self.tileHeight) - 3):
            subarray = []
            for tile in range(self.tileWidth):
                # TODO: Incredibly simple very random level generation look into perlin noise for alternative if time
                randNum = random.randint(0, 10)
                if randNum == 1:
                    subarray.append(randNum)
                else:
                    subarray.append(0)
            array.append(subarray)
        # So air gap above floor
        array.append([0]*(self.tileWidth))
        # So floor is solid
        array.append([1]*(self.tileWidth))

        # Convert to new coords format
        self.level = []
        for row in range(self.tileHeight):
            for col in range(self.tileWidth):
                if array[row][col] > 0:
                    self.level.append(
                        (array[row][col], (col * self.tileSize, row * self.tileSize)))

    def worldGen(self, game):
        try:
            with open(f'levels/level{game.level}at{game.tileMultiplier}') as f:
                self.level = ast.literal_eval(f.read()) # TODO: Convert to rects inside the level_editor saving but first see what things in the rect need to be changed bc its not x and y
        except Exception as error:
            print(error)
            main.error = "No (more) level's found or some kind of error occured. If there should be more levels try loading the level in world editor and resaving it :)"
            return True

    def update(self, screen, debug):
        screen.fill(self.sky)
        try:
            for tile in self.level:
                if tile[0] == 1:
                    screen.blit(self.grass, tile[1])
                elif tile[0] == 2:
                    screen.blit(self.dirt, tile[1])
                elif tile[0] == 3:
                    screen.blit(self.key, tile[1])
                elif tile[0] == 4:
                    screen.blit(self.doorTop, tile[1])
                elif tile[0] == 5:
                    screen.blit(self.doorBottom, tile[1])
                    # Debugging
                if debug:
                    self.tileRect.x, self.tileRect.y = tile[1]
                    pygame.draw.rect(screen, (0, 0, 255),
                                     self.tileRect, 2)

        except Exception as error:
            print(error)
            main.error = "It's possible the world file is corrupt"
            main.gameRun = False
