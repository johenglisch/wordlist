import wx
import wordlist.ui.strings as strings


class ToolBar(wx.ToolBar):
    def __init__(self, *args, **kwargs):
        super(ToolBar, self).__init__(*args, **kwargs)
        icon_open = wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_TOOLBAR)
        icon_save = wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE, wx.ART_TOOLBAR)
        icon_file = wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE,
                                             wx.ART_TOOLBAR)
        self.openf = self.AddLabelTool(id=wx.ID_OPEN,
                                       label=strings.tb_open,
                                       shortHelp=strings.tb_open_tooltip,
                                       longHelp=strings.help_open,
                                       bitmap=icon_open)
        self.savef = self.AddLabelTool(id=wx.ID_SAVE,
                                       label=strings.tb_save,
                                       shortHelp=strings.tb_open_tooltip,
                                       longHelp=strings.help_save,
                                       bitmap=icon_save)
        self.AddSeparator()
        self.stopf = self.AddLabelTool(id=wx.ID_ANY,
                                       label=strings.tb_stop,
                                       shortHelp=strings.tb_stop_tooltip,
                                       longHelp=strings.help_stop,
                                       bitmap=icon_file)

    def enable_tools(self, enable=True):
        self.EnableTool(wx.ID_SAVE, enable)
        self.EnableTool(self.stopf.GetId(), enable)

    def disable_tools(self):
        self.enable_tools(False)
