import wx
import main


class Menu(wx.Frame):
    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super(Menu, self).__init__(*args, **kw)
        # Set font and size for window
        self.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.BOLD))

        # Create a panel in the frame
        self.panel = wx.Panel(self)

        # Create button column
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        # Draw start button
        self.startBtn = wx.Button(
            self.panel, label="Start Game", size=(50, 0))
        # Bind events to start button to allow it to be clicked like an event listener really
        self.startBtn.Bind(wx.EVT_BUTTON, self.start)

        # Draw other buttons
        self.scoreBtn = wx.Button(
            self.panel, label="Highscores", size=(50, 0))
        # Bind events to start button to allow it to be clicked like an event listener really
        self.scoreBtn.Bind(wx.EVT_BUTTON, self.score)
        self.settingsBtn = wx.Button(
            self.panel, label="Settings", size=(50, 0))
        # Bind events to start button to allow it to be clicked like an event listener really
        self.settingsBtn.Bind(wx.EVT_BUTTON, self.settings)
        self.quitBtn = wx.Button(
            self.panel, label="Quit", size=(50, 0))
        # Bind events to start button to allow it to be clicked like an event listener really
        self.quitBtn.Bind(wx.EVT_BUTTON, self.onQuit)
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
        self.panel.SetSizer(self.sizer)

        # Centre the window on screen
        self.Centre()

        # Force Show GUI
        self.Show(True)

    def onQuit(self, e):
        self.Close()

    def start(self, e):
        main.gameRun = True
        self.Close()

    def score(self, e):
        pass

    def settings(self, e):
        pass
