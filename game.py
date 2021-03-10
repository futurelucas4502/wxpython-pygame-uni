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
        self.level = 0

        # Set grid size to a 16:9 aspect ratio as my resolution is divisible by 8 and dividing by 8 * 10 would give me a perfect 16:9 but i want more tiles so we do 8 * 5
        self.tileMultiplier = 5
        self.tileSize = 8 * self.tileMultiplier

        self.debug = False

        # Create small key for using in overlay to show player has key collected
        self.key = pygame.transform.scale(pygame.image.load(
            "assets/key.png").convert_alpha(), (int(self.tileSize // 1.25), int(self.tileSize // 1.25)))

        # Setup the level and character
        self.setup()

        # Finally Start game
        self.start()

    def setup(self):
        # Increment level
        self.level += 1
        # Make player
        self.player = entities.Player(
            (self.tileSize, self.tileSize*2), (0, self.height - self.tileSize*3))

        # Make world
        self.world = World(self)

    def start(self):
        while main.gameRun:
            self.clock.tick(60)  # max fps is 60

            # Draw world
            self.world.update(self.screen, self.debug)
            # Draw player above bottom row
            self.player.update(self)

            # Game info
            self.updateGameInfo()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # pygame.QUIT == the x button on the window
                    main.gameRun = False

                elif event.type == pygame.KEYDOWN:  # Press down and handle the button press
                    if event.key == pygame.K_p:
                        # Debug on or off
                        self.debug = not self.debug

            # PyGame renders using a double buffer so draws the data hidden first then displays it after this is better than flip as flip redraws everything whereas this only draws whats changed so its much faster and just better
            pygame.display.update()

        pygame.display.quit()

    def updateGameInfo(self):
        # can return None in very very rare instances so the code below will fix that as non null coelessing characters arent in python yet but there is a request for them here: https://www.python.org/dev/peps/pep-0505/
        fps = str(int(self.clock.get_fps()))
        if fps == "" or fps == None:
            fps = "00"
        self.screen.blit(self.font.render(fps, 1, (255, 255, 255)), (10, 7.5))
        if self.player.hasKey:
            self.screen.blit(self.key, (1240, 7.5))
