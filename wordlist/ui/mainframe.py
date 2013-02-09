import wx


class MainFrame(wx.Frame):
    def __init__(self, filename, parent):
        super(MainFrame, self).__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.SetSize((400, 400))
        self.SetTitle('Wordlist')
        self.Show()
