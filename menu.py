import wx
import main
import os
import configparser
import ast


class Menu(wx.Frame):

    def __init__(self, settingsSize, *args, **kw):
        # ensure the parent's __init__ is called
        super().__init__(*args, **kw)

        # Non window code start

        # Check game config exists if not make it with default properties
        self.config = configparser.ConfigParser()

        if not os.path.exists('config.ini'):
            self.config.add_section('settings')
            self.config.add_section('highscores')
            self.config.add_section('general')
            self.config['general']['players'] = "[]"

            self.config['settings']['experimental'] = "False"

            with open('config.ini', 'w') as configfile:
                self.config.write(configfile)

        self.config.read('config.ini')

        # Set font and size for window
        self.SetFont(wx.Font(wx.FontInfo(15)))

        # Create a panel in the frame
        self.main = Main(self, size=self.GetVirtualSize())
        self.settings = Settings(self, size=(self.GetVirtualSize()[0], self.GetVirtualSize()[1] - settingsSize))
        self.settings.Hide()  # Might be a better way of doing this if there is I can't find it

        # Centre the window on screen
        self.Centre()

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

        self.Destroy()  # If force closed just close


class Main(wx.Panel):

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        # Create button column
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        self.players = []
        [self.players.append(player)
         for player in ast.literal_eval(self.GetParent().config['general']['players'])]

        # Draw window user selected heading
        self.playerLabel = wx.StaticText(
            self, label="Selected Player: None", style=wx.ALIGN_CENTRE)
        self.playerLabel.SetFont(wx.Font(wx.FontInfo(15).Bold()))
        self.playerLabel.Wrap(260)

        self.infoLabel = wx.StaticText(
            self, label="Make new players from the settings", style=wx.ALIGN_CENTRE)
        self.infoLabel.SetFont(wx.Font(wx.FontInfo(10)))

        # Draw user selector
        self.playerCombo = wx.ComboBox(self, choices=self.players)

        # Draw buttons
        self.startBtn = wx.Button(self, label="Start Game", size=(50, 0))
        self.scoreBtn = wx.Button(self, label="Highscores", size=(50, 0))
        self.settingsBtn = wx.Button(self, label="Settings", size=(50, 0))
        self.levelEditorBtn = wx.Button(
            self, label="Level Editor", size=(50, 0))
        self.quitBtn = wx.Button(self, label="Quit", size=(50, 0))

        # Add things to button column
        # Adds padding to the top to push it to the bottom
        self.sizer.AddSpacer(20)

        # Add the user selection code to the sizer
        self.sizer.Add(self.playerLabel, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 20)
        self.sizer.Add(self.infoLabel, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 20)
        self.sizer.Add(self.playerCombo, 1, wx.EXPAND | wx.ALL, 20)

        # Horizontal center and 20 padding on all sides so buttons arent bunched together
        self.sizer.Add(self.startBtn, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 20)
        self.sizer.AddSpacer(10)
        self.sizer.Add(self.scoreBtn, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 20)
        self.sizer.AddSpacer(10)
        self.sizer.Add(self.settingsBtn, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 20)
        self.sizer.AddSpacer(10)
        self.sizer.Add(self.levelEditorBtn, 1,
                       wx.EXPAND | wx.LEFT | wx.RIGHT, 20)
        self.sizer.AddSpacer(10)
        self.sizer.Add(self.quitBtn, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 20)

        # Adds padding to the bottom to push it to the top so it ends up in the center
        self.sizer.AddSpacer(20)

        # Tells panel to add a sizer child and uses the one we just made
        self.SetSizer(self.sizer)

        # Bind event to the user selection combo box
        self.playerCombo.Bind(wx.EVT_COMBOBOX, self.OnPlayerCombo)
        # Bind events to the buttons to allow them to be clicked like an event listener really
        self.startBtn.Bind(wx.EVT_BUTTON, self.start)
        self.scoreBtn.Bind(wx.EVT_BUTTON, self.score)
        self.settingsBtn.Bind(wx.EVT_BUTTON, self.settings)
        self.levelEditorBtn.Bind(wx.EVT_BUTTON, self.levelEditor)
        self.quitBtn.Bind(wx.EVT_BUTTON, self.onQuit)
        self.Layout()

    def OnPlayerCombo(self, e):
        self.playerLabel.SetLabel(
            "Selected Player: "+self.playerCombo.GetValue())

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
            self.GetParent().SetSize(wx.Size(300, 200))
            self.GetParent().settings.Show()

    def levelEditor(self, e):
        main.levelEditorRun = True
        self.GetParent().Destroy()


class Settings(wx.Panel):

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        # Create button column
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        # Create window elements
        self.playerInputLabel = wx.StaticText(self, label="New Player", style=wx.ALIGN_CENTRE)
        self.playerInputLabel.SetFont(wx.Font(wx.FontInfo(15).Bold()))
        self.playerInput = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)

        self.backBtn = wx.Button(self, label="Back", size=(50, 0))

        # Add things to button column
        # Adds padding to the top to push it to the bottom
        self.sizer.AddSpacer(20)

        # Horizontal center and 20 padding on all sides so buttons arent bunched together
        self.sizer.Add(self.playerInputLabel, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 20)
        self.sizer.AddSpacer(10)
        self.sizer.Add(self.playerInput, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 20)
        self.sizer.AddSpacer(10)
        self.sizer.Add(self.backBtn, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 20)

        # Adds padding to the bottom to push it to the top so it ends up in the center
        self.sizer.AddSpacer(20)

        # Tells panel to add a sizer child and uses the one we just made
        self.SetSizer(self.sizer)
        # Bind events to the buttons to allow them to be clicked like an event listener really
        self.playerInput.Bind(wx.EVT_TEXT_ENTER, self.addPlayer)
        self.backBtn.Bind(wx.EVT_BUTTON, self.back)
        self.Layout() 

    def addPlayer(self, e):
        players = ast.literal_eval(self.GetParent().config['general']['players'])
        players.append(self.playerInput.GetLineText(0))

        self.GetParent().config['general']['players'] = f'{players}'
        with open('config.ini', 'w') as configfile:
            self.GetParent().config.write(configfile)
        self.GetParent().config.read('config.ini') # TODO: This line doesnt work probably put in function on the parent



    def back(self, e):
        if self.IsShown():
            self.GetParent().SetTitle("Main Menu")
            self.Hide()
            self.GetParent().SetSize(wx.Size(300, 400))
            self.GetParent().main.Show()
