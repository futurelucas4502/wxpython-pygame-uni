import main
import pygame
import json
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

        # Prepare level assets which are 80x80 to use whatever grid_size scale we're using (use convert with non transparent and convert_alpha with transparent)
        self.grass = pygame.transform.scale(pygame.image.load(
            "assets/grass.png").convert(), (game.tileSize, game.tileSize))
        self.dirt = pygame.transform.scale(pygame.image.load(
            "assets/dirt.png").convert(), (game.tileSize, game.tileSize))
        self.key = pygame.transform.scale(pygame.image.load(
            "assets/key.png").convert_alpha(), (game.tileSize, game.tileSize))

        # Create a tile rect from any tile
        self.tileRect = self.grass.get_rect()

        # Generate new world
        if self.config['settings']['experimental'] == "False":
            if self.worldGen(game):
                main.gameRun = False
        else:
            self.randWorldGen(game)

    def randWorldGen(self,game):
        ''' Random world generation maybe to be added in the future very unfinished '''
        # Create an array with air gap at the top so that player can move at top of map
        array = [[0]*(self.tileWidth)]
        for row in range((self.tileHeight) - 3):
            subarray = []
            for tile in range(self.tileWidth):
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

        self.world = array

    def worldGen(self, game):
        if self.config["settings"]["json"]:
            try:
                with open(f'levels/level{game.level}at{game.tileMultiplier}.json') as f:
                    self.world = json.load(f)
            except Exception as error:
                print(error)
                main.error = "No (more) level's found"
                return True
        else:
            try:
                with open(f'levels/level{game.level}at{game.tileMultiplier}') as f:
                    self.world = ast.literal_eval(f)
            except Exception as error:
                print(error)
                main.error = "No (more) level's found"
                return True

    def draw(self, game):
        game.screen.fill(game.sky)
        if self.config["settings"]["json"] or self.config["settings"]["experimental"]: # random world loading only supports json loading
            try:
                # 9 rows in grid
                for row in range(self.tileHeight):
                    # 16 columns in each row
                    for tile in range(self.tileWidth):
                        # If current position in grid is 1 then it should be a grass block so show grass block
                        if self.world[row][tile] == 1:
                            game.screen.blit(
                                self.grass, (tile * game.tileSize, row * game.tileSize))
                        elif self.world[row][tile] == 2:
                            game.screen.blit(
                                self.dirt, (tile * game.tileSize, row * game.tileSize))
                        elif self.world[row][tile] == 3:
                            game.screen.blit(
                                self.key, (tile * game.tileSize, row * game.tileSize))
                        # Debugging
                        if game.debug:
                            if self.world[row][tile] != 0:
                                self.tileRect.x, self.tileRect.y = (
                                    tile * game.tileSize, row * game.tileSize)
                                pygame.draw.rect(
                                    game.screen, (0, 0, 255), self.tileRect, 2)

                            pygame.draw.rect(
                                game.screen, (255, 0, 0), game.player.rect, 2)
            except Exception as error:
                print(error)
                main.error = "It's possible the world file is corrupt"
                main.gameRun = False
        else:
            try:
                for tile in self.world:
                    if tile[0] == 1:
                        game.screen.blit(self.grass, tile[1])
                    elif tile[0] == 2:
                        game.screen.blit(self.dirt, tile[1])
                    elif tile[0] == 3:
                        game.screen.blit(self.key, tile[1])
                        # Debugging
                    if game.debug:
                        self.tileRect.x, self.tileRect.y = tile[1]
                        pygame.draw.rect(game.screen, (0, 0, 255),
                                        self.tileRect, 2)

                        pygame.draw.rect(game.screen, (255, 0, 0),
                                        game.player.rect, 2)

            except Exception as error:
                print(error)
                main.error = "It's possible the world file is corrupt"
                main.gameRun = False
