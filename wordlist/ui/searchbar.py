import wx


class SearchBar(wx.SearchCtrl):
    def __init__(self, *args, **kwargs):
        super(SearchBar, self).__init__(*args, **kwargs)
        self.ShowSearchButton(True)
        self.ShowCancelButton(True)
        self.Bind(event=wx.EVT_SEARCHCTRL_CANCEL_BTN, handler=self.on_cancel)

    def on_cancel(self, event):
        self.Show(False)
        self.GetParent().GetSizer().Layout()
