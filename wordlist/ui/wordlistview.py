import wx
from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin
import wordlist.ui.strings as strings


class WordlistView(wx.ListView):
    def __init__(self, parent):
        super(WordlistView, self).__init__(parent=parent)
        self.wordlist = None
        self.sortbyfreq = False
        self.sortbyends= False
        self.reset()

    def get_data(self):
        if self.sortbyfreq:
            return self.wordlist.items_by_frequency()
        if self.sortbyends:
            return self.wordlist.items_by_wordend()
        return self.wordlist.items_by_wordbeginning()

    def reset(self):
        self.ClearAll()
        if self.sortbyends:
            align = wx.LIST_FORMAT_RIGHT
        else:
            align = wx.LIST_FORMAT_LEFT
        self.InsertColumn(0, heading=strings.col_word, format=align, width=150)
        self.InsertColumn(1, heading=strings.col_freq, width=100)

    def set_wordlist(self, wordlist):
        self.wordlist = wordlist
        self.update()

    def set_sortbywords(self):
        self.sortbyfreq = False
        self.sortbyends = False
        self.update()

    def set_sortbyfreq(self):
        self.sortbyfreq = True
        self.sortbyends = False
        self.update()

    def set_sortbyends(self):
        self.sortbyfreq = False
        self.sortbyends = True
        self.update()

    def update(self):
        self.reset()
        data = self.get_data()
        for index, (word, frequency) in enumerate(data):
            self.InsertStringItem(index=index, label=word.encode('utf8'))
            self.SetStringItem(index=index, col=1, label=str(frequency))
