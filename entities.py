import pygame
from pygame.constants import K_SPACE, K_a, K_d, K_s, K_w

# Define a Player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'


class Player(pygame.sprite.Sprite):
	def __init__(self, size, pos):
		# Call the parent class (Sprite) constructor
		super().__init__()

		# Load the player image and get its rect
		self.playerRight = pygame.transform.scale(pygame.image.load('assets/player.png').convert_alpha(), size)
		self.playerLeft = pygame.transform.flip(pygame.transform.scale(pygame.image.load('assets/player.png').convert_alpha(), size), True, False)
		self.image = self.playerRight
		self.rect = self.image.get_rect()
		self.rect.x = pos[0]
		self.rect.y = pos[1]
		self.y_velocity = 0

	def update(self, screen, bottom):
		key = pygame.key.get_pressed()
		# Move left and right with edge collision detection
		# right edge of the window
		if key[K_d] and self.rect.right < screen.get_size()[0]:
			self.image = self.playerRight
			self.rect.x += 3
		if key[K_a] and self.rect.left > 0:  # 0 will be the left edge of the window
			self.image = self.playerLeft
			self.rect.x -= 3
		if key[K_SPACE]:
			self.y_velocity -= 10

		# Collision

		# for tile in 

		# Gravity
		self.y_velocity += 1
		self.rect.y += self.y_velocity

		if self.y_velocity > 10:
			self.y_velocity = 10

		if self.rect.bottom > bottom:
			self.rect.bottom = bottom
			self.y_velocity = 0
