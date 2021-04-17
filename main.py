import run
import pygame
gameRun = False
levelEditorRun = False
error = False
msg = ""
title = ""


def main():
    if run.game():  # Runs the game and returns True when it's done to rerun main and open the menu again
        main()
    else:
        pygame.quit()


if __name__ == '__main__':
    main()
