import pygame
import json
import main
from os import path


class LevelEditor():
    def __init__(self):
        pygame.init()

        self.clock = pygame.time.Clock()

        # Define screen info
        self.tileMultiplier = 5
        self.tileSize = 8 * self.tileMultiplier
        self.width = 1280
        self.height = 720
        self.tileWidth = self.width // self.tileSize
        self.tileHeight = self.height // self.tileSize

        # Create screen

        self.screen = pygame.display.set_mode((self.width, self.height + 80))
        pygame.display.set_caption('Level Editor')

        # Load world assets
        self.dirt_img = pygame.transform.scale(pygame.image.load(
            'assets/dirt.png').convert(), (self.tileSize, self.tileSize))
        self.grass_img = pygame.transform.scale(pygame.image.load(
            'assets/grass.png').convert(), (self.tileSize, self.tileSize))
        self.key_img = pygame.transform.scale(pygame.image.load(
            'assets/key.png').convert_alpha(), (self.tileSize, self.tileSize))

        # Define image info and level counter
        self.num_images = 3
        self.level = 1

        # Define colours
        self.white = (255, 255, 255)
        self.blue = (173, 216, 230)

        self.font = pygame.font.SysFont("Arial", 24)

        # Create empty world with solid ground

        self.world_data = []
        for row in range(self.tileHeight - 1):
            r = [0] * self.tileWidth
            self.world_data.append(r)
        self.world_data.append([1] * self.tileWidth)

        # Create save code

        self.saveDialog = Button(self, text="Click me to confirm save", size=(
            250, 50), pos=self.screen.get_rect().center, command=self.save)

        self.start()

    # Draw any text e.g info text

    def draw_text(self, text, font, x, y):
        self.screen.blit(font.render(text, 1, (255, 255, 255)), (x, y))

    # Draw/render outline grid

    def draw_grid(self):
        for x in range(self.tileWidth):
            for y in range(self.tileHeight):
                pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(x*self.tileSize, y*self.tileSize,
                                                                           self.tileSize, self.tileSize), 1)

    # Draw/render the world

    def draw_world(self):
        for row in range(self.tileHeight):
            for col in range(self.tileWidth):
                if self.world_data[row][col] > 0:
                    if self.world_data[row][col] == 1:
                        # Grass blocks
                        self.screen.blit(
                            self.grass_img, (col * self.tileSize, row * self.tileSize))
                    elif self.world_data[row][col] == 2:
                        # Dirt blocks
                        self.screen.blit(
                            self.dirt_img, (col * self.tileSize, row * self.tileSize))
                    elif self.world_data[row][col] == 3:
                        # Key
                        self.screen.blit(
                            self.key_img, (col * self.tileSize, row * self.tileSize))

    def save(self):
        world_rects = []
        for row in range(self.tileHeight):
            for col in range(self.tileWidth):
                if self.world_data[row][col] > 0:
                    world_rects.append(
                        (self.world_data[row][col], (col * self.tileSize, row * self.tileSize)))
        with open(f'levels/level{self.level}at{self.tileMultiplier}', 'w') as file:
            file.write(str(world_rects))
        with open(f'levels/level{self.level}at{self.tileMultiplier}.json', 'w') as file:
            json.dump(self.world_data, file)
        self.saveDialog.shown = False

    def start(self):
        while main.levelEditorRun:

            self.clock.tick(60)

            # Draw sky
            self.screen.fill(self.blue)

            # Show the grid and draw the level tiles
            self.draw_grid()
            self.draw_world()

            # Info text
            self.draw_text(f'Level: {self.level}',
                           self.font, self.tileSize, self.height)
            self.draw_text('Press UP or DOWN to change level',
                           self.font, self.tileSize, self.height + 20)
            self.draw_text('Press S to save and L to load',
                           self.font, self.tileSize, self.height + 40)

            # Save dialog
            if self.saveDialog.shown:
                self.saveDialog.draw(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    main.levelEditorRun = False
                # Click to change tile
                elif event.type == pygame.MOUSEBUTTONDOWN and not self.saveDialog.shown:
                    pos = pygame.mouse.get_pos()
                    col = pos[0] // self.tileSize
                    row = pos[1] // self.tileSize
                    # Check click is within grid
                    if col < self.tileWidth and row < self.tileHeight and self.saveDialog.rect:
                        # Change tile
                        if pygame.mouse.get_pressed()[0] == 1:
                            self.world_data[row][col] += 1
                            if self.world_data[row][col] > self.num_images:
                                self.world_data[row][col] = 0
                        elif pygame.mouse.get_pressed()[2] == 1:
                            self.world_data[row][col] -= 1
                            if self.world_data[row][col] < 0:
                                self.world_data[row][col] = self.num_images

                # Up and down key presses to change level
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.level += 1
                    elif event.key == pygame.K_DOWN and self.level > 1:
                        self.level -= 1
                    # Load and save level
                    elif event.key == pygame.K_s:
                        self.saveDialog.shown = True
                    elif event.key == pygame.K_l:
                        # Load in level data
                        if path.exists(f'levels/level{self.level}at{self.tileMultiplier}.json'):
                            with open(f'levels/level{self.level}at{self.tileMultiplier}.json') as file:
                                self.world_data = json.load(file)

                # Save dialog handler
                self.saveDialog.event_handler(event)

            pygame.display.update()

        pygame.quit()


class Button():
    def __init__(self, editor, text="Button", pos=(50, 50), size=(50, 50), bgColour=((211, 211, 211), (190, 190, 190)), colour=(0, 0, 0), command=None):
        self.normalBtn = pygame.Surface(size)
        self.hoveredBtn = pygame.Surface(size)
        # Set command for use later
        self.command = command

        self.normalBtn.fill(bgColour[0])
        self.hoveredBtn.fill(bgColour[1])

        self.button = self.normalBtn
        self.rect = self.button.get_rect()

        text = editor.font.render(text, True, colour)
        textRect = text.get_rect(center=self.rect.center)

        # Attach the text to the surface of the button
        self.normalBtn.blit(text, textRect)
        self.hoveredBtn.blit(text, textRect)

        self.rect.center = pos
        self.shown = False

    def draw(self, surface):
        if self.hovered:
            self.button = self.hoveredBtn
        else:
            self.button = self.normalBtn
        surface.blit(self.button, self.rect)

    def event_handler(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.shown == True:
                if self.hovered:
                    if self.command:
                        self.command()
                else:
                    self.shown = False
