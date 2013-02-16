import wx


class SearchBar(wx.SearchCtrl):
    def __init__(self, parent):
        super(SearchBar, self).__init__(parent=parent,
                                        style=wx.TE_PROCESS_ENTER)
        self.ShowSearchButton(True)
        self.ShowCancelButton(True)
        self.Bind(event=wx.EVT_SEARCHCTRL_CANCEL_BTN, handler=self.on_cancel)
        self.Bind(event=wx.EVT_KEY_UP, handler=self.on_key)

    def hide(self):
        self.Show(False)
        self.GetParent().GetSizer().Layout()

    def unhide(self):
        self.Show(True)
        self.GetParent().GetSizer().Layout()
        self.SetFocus()

    def on_key(self, event):
        if event.GetKeyCode() == wx.WXK_ESCAPE:
            self.hide()

    def on_cancel(self, event):
        self.hide()
