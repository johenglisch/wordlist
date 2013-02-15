import wx
import wordlist.ui.strings as strings


class ErrorDialog(wx.MessageDialog):
    def __init__(self, parent, message):
        super(ErrorDialog, self).__init__(parent=parent,
                                          message=message,
                                          caption=strings.dlg_error,
                                          style=wx.OK | wx.ICON_ERROR)
        self.ShowModal()
        self.Destroy()


class MessageDialog(wx.MessageDialog):
    def __init__(self, parent, message):
        super(MessageDialog, self).__init__(parent=parent,
                                            message=message,
                                            caption=strings.dlg_info,
                                            style=wx.OK | wx.ICON_INFORMATION)
        self.ShowModal()
        self.Destroy()


class OpenDialog(wx.FileDialog):
    def __init__(self, parent):
        super(OpenDialog, self).__init__(parent=parent,
                                         message=strings.dlg_open,
                                         style=wx.FD_OPEN | wx.FD_CHANGE_DIR)


class SaveDialog(wx.FileDialog):
    def __init__(self, parent):
        super(SaveDialog, self).__init__(parent=parent,
                                         message=strings.dlg_save,
                                         style=wx.FD_SAVE |
                                               wx.FD_OVERWRITE_PROMPT)
