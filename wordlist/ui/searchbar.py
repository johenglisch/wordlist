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


#class SearchBar(wx.BoxSizer):
#    def __init__(self, parent):
#        super(SearchBar, self).__init__(orient=wx.HORIZONTAL)
#        self.parent = parent
#        self.init_ui()
#
#    def init_ui(self):
#        self.find_but = wx.Button(parent=self.parent, label='&Find',
#                                  style=wx.BU_EXACTFIT)
#        self.find_field = wx.TextCtrl(parent=self.parent)
#        self.find_close = wx.Button(parent=self.parent, label='X',
#                                    style=wx.BU_EXACTFIT)
#        self.Add(item=self.find_but)# proportion=0,
#                 #flag=wx.TOP | wx.BOTTOM)#, border=5)
#        self.Add(item=self.find_field, proportion=1)
#                 #flag=wx.TOP | wx.BOTTOM | wx.EXPAND)#, border=5)
#        self.Add(item=self.find_close)# proportion=0,
#                 #flag=wx.TOP | wx.BOTTOM)#, border=5)
#        # events
#        self.find_close.Bind(event=wx.EVT_BUTTON, handler=self.on_hide)
#
#
#    def on_show(self, event):
#        self.ShowItems(True)
#        self.parent.GetSizer().Layout()
#        self.find_field.SetFocus()
#
#    def on_hide(self, event):
#        self.ShowItems(False)
#        self.parent.GetSizer().Layout()
