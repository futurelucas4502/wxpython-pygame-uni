from floor import Floor
from player import Player
from pygame.locals import *
import pygame
import main

clock = pygame.time.Clock()


class Game():
    def __init__(self):
        self.screen = pygame.display.set_mode((940, 620), RESIZABLE)
        pygame.display.set_caption("Game")

        # Instantiate self.player. Right now, this is just a rectangle.
        self.player = Player()
        self.platform = Floor()
        self.start()

    def start(self):
        while True:
            clock.tick(200)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # pygame.QUIT == the x button on the window
                    pygame.display.quit()
                    pygame.quit()
                    main.gameRun = False

                elif event.type == pygame.KEYDOWN:  # Press down and handle the button press
                    if event.key == pygame.K_a:  # K_a == the key a
                        self.player.moving_left = True
                    elif event.key == pygame.K_d:
                        self.player.moving_right = True
                    elif event.key == pygame.K_w:
                        self.player.moving_up = True
                    elif event.key == pygame.K_s:
                        self.player.moving_down = True
                    elif event.key == pygame.K_p:
                        print(self.screen.get_size()[0])

                elif event.type == pygame.KEYUP:  # Handle the user stopping pressing the button
                    if event.key == pygame.K_a:
                        self.player.moving_left = False
                    elif event.key == pygame.K_d:
                        self.player.moving_right = False
                    elif event.key == pygame.K_w:
                        self.player.moving_up = False
                    elif event.key == pygame.K_s:
                        self.player.moving_down = False
            if main.gameRun == False:  # Prevent atttempting to draw on dead screen after window has been closed
                break
            self.player.update(self.screen)
            self.platform.update(self.screen)

            self.screen.fill((0, 0, 0))  # fill screen black
            # update screen contents here
            # Draw the self.player on the screen
            self.screen.blit(self.platform.surf, self.platform.rect)
            self.screen.blit(self.player.image, self.player.rect)
            # PyGame renders using a double buffer so draws the data hidden first then displays it after
            pygame.display.flip()
