import pygame

class Floor(pygame.sprite.Sprite):
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()

        # Create sprite variables
        self.surf = pygame.Surface((320, 10))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
    
    def update(self, screen):
        self.rect.y = screen.get_size()[1]-10
