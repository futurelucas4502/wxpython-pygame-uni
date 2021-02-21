import wx
import main
import os
import configparser


class Menu(wx.Frame):

    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super().__init__(*args, **kw)
        # Set font and size for window
        self.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.BOLD))

        # Create a panel in the frame
        self.main = Main(self, size=self.GetVirtualSize())
        self.settings = Settings(self, size=self.GetVirtualSize())
        self.settings.Hide()  # Might be a better way of doing this if there is I can't find it

        # Centre the window on screen
        self.Centre()

        # Check game config exists if not make it with default properties
        self.config = configparser.ConfigParser()
        if not os.path.exists('config.ini'):
            self.config.add_section('settings')
            self.config.add_section('highscores')

            self.config['settings']['experimental'] = "False"

            with open('config.ini', 'w') as configfile:
                self.config.write(configfile)

        # Catch window closing
        self.Bind(wx.EVT_CLOSE, self.onClose)

        # Show GUI
        self.Show(True)

    def onClose(self, e):
        # canVeto means if its not a force close it'll ask the user if theyre sure they want to close and close normally
        if e.CanVeto():
            if wx.MessageBox("Are you sure you want to quit?", "Please confirm", wx.ICON_QUESTION | wx.YES_NO) != wx.YES:
                e.Veto()
                return

        self.Destroy() # If force closed just close

class Main(wx.Panel):

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        # Create button column
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        # Draw buttons
        self.startBtn = wx.Button(self, label="Start Game", size=(50, 0))
        self.scoreBtn = wx.Button(self, label="Highscores", size=(50, 0))
        self.settingsBtn = wx.Button(self, label="Settings", size=(50, 0))
        self.quitBtn = wx.Button(self, label="Quit", size=(50, 0))

        # Add things to button column
        # Adds padding to the top to push it to the bottom
        self.sizer.AddSpacer(20)

        # Horizontal center and 20 padding on all sides so buttons arent bunched together
        self.sizer.Add(self.startBtn, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 20)
        self.sizer.AddSpacer(10)
        self.sizer.Add(self.scoreBtn, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 20)
        self.sizer.AddSpacer(10)
        self.sizer.Add(self.settingsBtn, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 20)
        self.sizer.AddSpacer(10)
        self.sizer.Add(self.quitBtn, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 20)

        # Adds padding to the bottom to push it to the top so it ends up in the center
        self.sizer.AddSpacer(20)

        # Tells panel to add a sizer child and uses the one we just made
        self.SetSizer(self.sizer)
        # Bind events to the buttons to allow them to be clicked like an event listener really
        self.startBtn.Bind(wx.EVT_BUTTON, self.start)
        self.scoreBtn.Bind(wx.EVT_BUTTON, self.score)
        self.settingsBtn.Bind(wx.EVT_BUTTON, self.settings)
        self.quitBtn.Bind(wx.EVT_BUTTON, self.onQuit)
        self.Layout()

    def onQuit(self, e):
        self.GetParent().Close()

    def start(self, e):
        main.gameRun = True
        self.GetParent().Destroy()

    def score(self, e):
        pass

    def settings(self, e):
        if self.IsShown():
            self.GetParent().SetTitle("Settings")
            self.Hide()
            self.GetParent().settings.Show()


class Settings(wx.Panel):

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        # Create button column
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        # Tells panel to add a sizer child and uses the one we just made
        self.sizer.AddStretchSpacer()
        self.SetSizer(self.sizer)
        self.Layout()
