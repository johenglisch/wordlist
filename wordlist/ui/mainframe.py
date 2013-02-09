import wx
from .searchbar import SearchBar


class MainFrame(wx.Frame):
    def __init__(self, filename, parent):
        super(MainFrame, self).__init__(parent)
        self.init_ui()
        self.SetSize((400, 400))
        self.SetTitle('Wordlist')
        self.Show()

    def init_ui(self):
        self.searchbar = SearchBar(parent=self)
        self.wordlist = wx.ListCtrl(parent=self, style=wx.LC_REPORT)
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(item=self.searchbar, proportion=0, flag=wx.EXPAND)
        vbox.Add(item=self.wordlist, proportion=1, flag=wx.EXPAND)
        self.SetSizer(vbox)
