import pygame
from pygame.constants import K_SPACE, K_a, K_d, K_s, K_w

# Define a Player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'


class Player(pygame.sprite.Sprite):
	def __init__(self, size, pos):
		# Call the parent class (Sprite) constructor
		super().__init__()

		# Load the crab image and get its rect.
		self.image = pygame.transform.scale(pygame.image.load('assets/player.png').convert_alpha(), size)
		self.rect = self.image.get_rect()
		self.rect.x = pos[0]
		self.rect.y = pos[1]
		self.y_velocity = 0
		self.jumped = False

	def update(self, screen, bottom):
		key = pygame.key.get_pressed()
		# Move left and right with edge collision detection
		# right edge of the window
		if key[K_d] and self.rect.right < screen.get_size()[0]:
			self.rect.x += 3
		if key[K_a] and self.rect.left > 0:  # 0 will be the left edge of the window
			self.rect.x -= 3
		if key[K_SPACE] and self.jumped == False:
			self.y_velocity -= 10
			self.jumped = True
		if key[K_SPACE] == False:
			self.jumped = False

		# Gravity
		self.y_velocity += 1
		self.rect.y += self.y_velocity

		if self.y_velocity > 10:
			self.y_velocity = 10

		elif self.rect.bottom > bottom:
			self.rect.bottom = bottom
			self.y_velocity = 0
