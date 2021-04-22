import run
import pygame
gameRun = False
levelEditorRun = False
error = False
msg = ""
title = ""
player = ""

def main():
    # Runs the game and returns True when it's done to rerun main and open the menu again
    if run.game():
        main()
    else:
        pygame.quit()


if __name__ == '__main__':
    main()
