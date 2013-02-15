import wx
from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin
import wordlist.ui.strings as strings


class WordlistView(wx.ListView, ListCtrlAutoWidthMixin):
    def __init__(self, parent):
        wx.ListView.__init__(self, parent=parent)
        ListCtrlAutoWidthMixin.__init__(self)
        self.setResizeColumn(0)
        self.wordlist = None
        self.sortbyfreq = False
        self.sortbyend= False
        self.reset()

    def reset(self):
        self.ClearAll()
        self.InsertColumn(0, heading=strings.col_word)
        self.InsertColumn(1, heading=strings.col_freq)

    def set_wordlist(self, wordlist):
        self.wordlist = wordlist
        self.update()

    def set_sortbyword(self):
        self.sortbyfreq = False
        self.sortbyend = False
        self.update()

    def set_sortbyfreq(self):
        self.sortbyfreq = True
        self.sortbyend = False
        self.update()

    def set_sortbyend(self):
        self.sortbyfreq = False
        self.sortbyend = True
        self.update()

    def update(self):
        self.reset()
        if self.sortbyfreq:
            data = self.wordlist.items_by_frequency()
        elif self.sortbyend:
            data = self.wordlist.items_by_wordend()
        else:
            data = self.wordlist.items_by_wordbeginning()
        for index, (word, frequency) in enumerate(data):
            self.InsertStringItem(index=index, label=word)
            self.SetStringItem(index=index, col=1, label=str(frequency))
        self.resizeColumn(20)
