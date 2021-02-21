import wx
import main
from menu import Menu
from game import Game


def game():
    app = wx.App()
    Menu(None, title="Main Menu", size=(250, 250),
              style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
    if main.error != "": # Error handler
        wx.MessageDialog(None, main.error, "An error occured",
                         wx.OK | wx.ICON_ERROR).ShowModal()
        main.error = ""
    app.MainLoop()  # When i click the start game button the gameRun variable gets changed to True then closes the menu meaning line 14 below runs
    if main.gameRun:
        Game()  # Start the game
        return True  # Game has finished or been closed so return True to open the menu
