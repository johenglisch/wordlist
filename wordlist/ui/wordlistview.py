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

    def get_data(self):
        if self.sortbyfreq:
            return self.wordlist.items_by_frequency()
        if self.sortbyend:
            return self.wordlist.items_by_wordend()
        return self.wordlist.items_by_wordbeginning()

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
        data = self.get_data()
        for index, (word, frequency) in enumerate(data):
            self.InsertStringItem(index=index, label=word)
            self.SetStringItem(index=index, col=1, label=str(frequency))
        self.resizeColumn(20)
