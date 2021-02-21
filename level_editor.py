import pygame
import json
from os import path

pygame.init()

clock = pygame.time.Clock()

# Define screen info
tileMultiplier = 5
tileSize = 8 * tileMultiplier
width = 1280
height = 720
tileWidth = width // tileSize
tileHeight = height // tileSize

# Create screen

screen = pygame.display.set_mode((width, height + 80))
pygame.display.set_caption('Level Editor')


# Load world assets
dirt_img = pygame.transform.scale(pygame.image.load(
    'assets/dirt.png').convert(), (tileSize, tileSize))
grass_img = pygame.transform.scale(pygame.image.load(
    'assets/grass.png').convert(), (tileSize, tileSize))
key_img = pygame.transform.scale(pygame.image.load(
    'assets/key.png').convert_alpha(), (tileSize, tileSize))


# Define image info and level counter
num_images = 3
level = 1


# Define colours
white = (255, 255, 255)
blue = (173, 216, 230)

font = pygame.font.SysFont("Arial", 24)

# Create empty world with solid ground

world_data = []
for row in range(tileHeight - 1):
    r = [0] * tileWidth
    world_data.append(r)
world_data.append([1] * tileWidth)

# Draw any text e.g info text


def draw_text(text, font, x, y):
    screen.blit(font.render(text, 1, (255, 255, 255)), (x, y))


# Draw/render outline grid

def draw_grid():
    for x in range(tileWidth):
        for y in range(tileHeight):
            pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(x*tileSize, y*tileSize,
                                                                  tileSize, tileSize), 1)

# Draw/render the world


def draw_world():
    for row in range(tileHeight):
        for col in range(tileWidth):
            if world_data[row][col] > 0:
                if world_data[row][col] == 1:
                    # Grass blocks
                    screen.blit(grass_img, (col * tileSize, row * tileSize))
                elif world_data[row][col] == 2:
                    # Dirt blocks
                    screen.blit(dirt_img, (col * tileSize, row * tileSize))
                elif world_data[row][col] == 3:
                    # Key
                    screen.blit(key_img, (col * tileSize, row * tileSize))


run = True
while run:

    clock.tick(60)

    # Draw sky
    screen.fill(blue)

    # Show the grid and draw the level tiles
    draw_grid()
    draw_world()

    # Info text
    draw_text(f'Level: {level}', font, tileSize, height)
    draw_text('Press UP or DOWN to change level', font, tileSize, height + 20)
    draw_text('Press S to save and L to load', font, tileSize, height + 40)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # Click to change tile
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            col = pos[0] // tileSize
            row = pos[1] // tileSize
            # Check click is within grid
            if col < tileWidth and row < tileHeight:
                # Change tile
                if pygame.mouse.get_pressed()[0] == 1:
                    world_data[row][col] += 1
                    if world_data[row][col] > num_images:
                        world_data[row][col] = 0
                elif pygame.mouse.get_pressed()[2] == 1:
                    world_data[row][col] -= 1
                    if world_data[row][col] < 0:
                        world_data[row][col] = num_images

        # Up and down key presses to change level
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                level += 1
            elif event.key == pygame.K_DOWN and level > 1:
                level -= 1
            # Load and save level
            elif event.key == pygame.K_s:
                # Save level data
                with open(f'levels/level{level}at{tileMultiplier}.json', 'w') as file:
                    json.dump(world_data, file)
            elif event.key == pygame.K_l:
                # Load in level data
                if path.exists(f'levels/level{level}at{tileMultiplier}.json'):
                    with open(f'levels/level{level}at{tileMultiplier}.json') as file:
                        world_data = json.load(file)

    pygame.display.update()

pygame.quit()
