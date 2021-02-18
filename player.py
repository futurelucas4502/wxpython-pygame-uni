import pygame

# Define a Player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'


class Player(pygame.sprite.Sprite):
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()

        # Load the crab image and get its rect.
        self.image = pygame.transform.scale(
            pygame.image.load('assets/crab.png'), (94, 62))
        self.rect = self.image.get_rect()

        # Directional data that we can set to true or false to move left and right
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self, screen):
        # Move left and right with edge collision detection
        # right edge of the window
        if self.moving_right and self.rect.right < screen.get_size()[0]:
            screen.get_size()[0]
            self.rect.x += 1
        if self.moving_left and self.rect.left > 0:  # 0 will be the left edge of the window
            self.rect.x -= 1
        # 0 will be the top edge of the window
        if self.moving_down and self.rect.bottom < screen.get_size()[1]:
            self.rect.y += 1
        if self.moving_up and self.rect.top > 0:  # bottom edge of the window
            self.rect.y -= 1
