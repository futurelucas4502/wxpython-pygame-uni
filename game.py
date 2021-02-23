from world import World
from pygame.locals import *
import pygame
import entities
import main


class Game():
    def __init__(self):
        pygame.init()

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

        # Make player
        self.player = entities.Player(
            (self.tileSize, self.tileSize*2), (0, self.height - self.tileSize*3))

        # Make world
        self.world = World(self)

        self.debug = False

        # Finally Start game
        self.start()

    def start(self):
        while main.gameRun:
            self.clock.tick(60)  # max fps is 60

            # Move player pos
            self.player.update(self.screen, self.screen.get_size()[
                               1] - self.tileSize)

            # Draw world
            self.world.draw(self)

            # Draw the player on the screen
            self.screen.blit(self.player.image, self.player.rect)

            # FPS
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

    def updateFPS(self):
        fps = str(int(self.clock.get_fps()))
        return self.font.render(fps, 1, (255, 255, 255))
