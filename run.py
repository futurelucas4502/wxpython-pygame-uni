import wx
import pygame
import main
from game import Game
from menu import Menu
pygame.init()


def game():
    menu = wx.App()
    Menu(None, title="Game Menu", size=(250, 250),
         style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
    menu.MainLoop()  # When i click the start game button the gameRun variable gets changed to True then closes the menu meaning line 14 below runs
    if main.gameRun:
        Game()  # Start the game
        return True  # Game has finished or been closed so return True to open the menu
