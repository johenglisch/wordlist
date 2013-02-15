import wx
import wordlist.ui.strings as strings


class ErrorDialog(wx.MessageDialog):
    def __init__(self, parent, message):
        super(ErrorDialog, self).__init__(parent=parent,
                                          message=message,
                                          caption=strings.dlg_error,
                                          style=wx.OK | wx.ICON_ERROR)


class OpenDialog(wx.FileDialog):
    def __init__(self, parent):
        super(OpenDialog, self).__init__(parent=parent,
                                         message=strings.dlg_open,
                                         style=wx.FD_OPEN)
