import wx
import wordlist.ui.strings as strings


class ErrorDialog(wx.MessageDialog):
    def __init__(self, parent, message):
        super(ErrorDialog, self).__init__(parent=parent,
                                          message=message,
                                          caption=strings.error_caption,
                                          style=wx.OK | wx.ICON_ERROR)
