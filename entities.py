import pygame
from pygame.locals import *
import random

# Define a Player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'


class Player(pygame.sprite.Sprite):
    def __init__(self, size, pos):
        # Call the parent class (Sprite) constructor
        super().__init__()

        # Load the player image and get its rect
        self.playerRight = pygame.transform.scale(
            pygame.image.load('assets/player.png').convert_alpha(), size)
        self.playerLeft = pygame.transform.flip(pygame.transform.scale(
            pygame.image.load('assets/player.png').convert_alpha(), size), True, False)
        self.image = self.playerRight
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.y_velocity = 0
        self.size = size
        self.jumped = False
        self.hasKey = False

    def update(self, game):
        tempX = 0
        tempY = 0

        key = pygame.key.get_pressed()
        # Move left and right with edge collision detection
        # right edge of the window
        if key[K_d] and self.rect.right < game.screen.get_size()[0]:
            self.image = self.playerRight
            tempX += 3
        if key[K_a] and self.rect.left > 0:  # 0 will be the left edge of the window
            self.image = self.playerLeft
            tempX -= 3
        # 0 is top so if we want to go up we need to minus
        if key[K_SPACE] and self.jumped == False:
            self.y_velocity = -17.5
            self.jumped = True

        # Gravity
        self.y_velocity += 1  # Keep adding 1 to velocity to curve the gravity make the player go up and slow down then slowly come down like a curve

        if self.y_velocity > 10:  # Set terminal velocity to a max of 10
            self.y_velocity = 10

        tempY += self.y_velocity  # Store velocity in tempY so we have a copy of the number of tiles we're moving by so we can work out whether or not its safe to move without colliding

        # Collision

        for tile in game.world.level:
            block = pygame.Rect(tile[1][0], tile[1][1],
                                game.tileSize, game.tileSize)

            # Check for collision in x direction
            if block.colliderect(self.rect.x + tempX, self.rect.y, self.size[0], self.size[1]):
                if tile[0] == 3:  # If colliding with a key
                    game.world.level.remove(tile)
                    self.hasKey = True
                elif tile[0] == 4 or tile[0] == 5:  # If colliding with the door
                    if self.hasKey:
                        game.setup()
                        return
                elif tempX > 0:  # Moving right
                    tempX = block.left - self.rect.right
                elif tempX < 0:  # Moving left
                    tempX = block.right - self.rect.left

            # Check for collision in y direction
            elif block.colliderect(self.rect.x, self.rect.y + tempY, self.size[0], self.size[1]):
                if tile[0] == 3:  # If colliding with a key
                    game.world.level.remove(tile)
                    self.hasKey = True
                elif tile[0] == 4 or tile[0] == 5:  # If colliding with the door
                    if self.hasKey:
                        game.setup()
                        return
                else:
                    # Check if jumping and will hit head on block if they move then move them as close as they can get to the block without overlapping and come back down
                    # Prevent treating key like a normal block so dont stop when hit head on it just go through it
                    if self.y_velocity < 0:
                        tempY = block.bottom - self.rect.top
                        self.y_velocity = 0

                    elif self.y_velocity > 0:
                        tempY = block.top - self.rect.bottom

                    if self.rect.bottom == block.top:  # Allow players to hold space to jump
                        self.jumped = False

        self.rect.x += tempX
        self.rect.y += tempY

        # Draw Player
        game.screen.blit(self.image, self.rect)
        if game.debug:
            pygame.draw.rect(game.screen, (255, 0, 0), self.rect, 2)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.image.load("assets/enemy.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        # Random number between 1 and 0 aka true or false to decide original direction
        self.move_direction = bool(random.randint(0, 1))
        self.counter = 0

    def update(self, screen):
        if self.counter > 60:
            self.move_direction = not self.move_direction
            self.counter = 0
        if self.move_direction:
            self.rect.x += 1
        else:
            self.rect.x -= 1
        self.counter += 1
        screen.blit(self.image, self.rect)
