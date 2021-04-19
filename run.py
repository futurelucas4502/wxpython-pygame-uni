import wx
import main
import configparser
from menu import Menu
from game import Game
from level_editor import LevelEditor


def game():
    app = wx.App()
    Menu(200, None, title="Main Menu", size=(300, 400),
         style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))

    if main.msg != "":  # Message Handler
        wx.MessageDialog(None, main.msg, main.title,
                         wx.OK | wx.ICON_ERROR if main.error else wx.ICON_NONE).ShowModal()
        main.error = False
        main.msg = ""
        main.title = ""

    app.MainLoop()  # When i click the start game button the gameRun variable gets changed to True then closes the menu meaning line 14 below runs
    if main.gameRun:
        Game()  # Start the game

        # Save score data
        config = configparser.ConfigParser()
        config.read('config.ini')
        if int(config['players'][main.player]) < main.score:
            config['players'][main.player] = str(main.score)
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        return True  # Game has finished or been closed so return True to open the menu
    if main.levelEditorRun:
        LevelEditor()  # Start the game
        return True  # Game has finished or been closed so return True to open the menu
