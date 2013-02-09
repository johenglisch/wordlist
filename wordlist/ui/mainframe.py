import wx
import strings
import menus
import searchbar


class MainFrame(wx.Frame):
    def __init__(self, filename, parent):
        super(MainFrame, self).__init__(parent)
        self.init_ui()
        self.SetSize((400, 400))
        self.SetTitle(strings.programme_name)
        self.Show()

    def init_ui(self):
        # menu
        menubar = wx.MenuBar()
        self.filemenu = menus.FileMenu()
        menubar.Append(self.filemenu, strings.menu_file)
        self.SetMenuBar(menubar)

        # widgets
        self.searchbar = searchbar.SearchBar(parent=self)
        # TODO hide searchbar by default
        self.wordlist = wx.ListCtrl(parent=self, style=wx.LC_REPORT)

        # layout
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(item=self.searchbar, proportion=0, flag=wx.EXPAND)
        vbox.Add(item=self.wordlist, proportion=1, flag=wx.EXPAND)
        self.SetSizer(vbox)

        # status bar
        self.statusbar = self.CreateStatusBar()
