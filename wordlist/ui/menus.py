import wx
import strings


class FileMenu(wx.Menu):
    def __init__(self, *args, **kwargs):
        super(FileMenu, self).__init__(*args, **kwargs)
        self.init_ui()

    def init_ui(self):
        self.openf = self.Append(id=wx.ID_OPEN,
                                 text=strings.menu_open,
                                 help=strings.menu_open_help)
        self.savef = self.Append(id=wx.ID_SAVE,
                                 text=strings.menu_save,
                                 help=strings.menu_save_help)
        self.AppendSeparator()
        self.quit = self.Append(id=wx.ID_EXIT,
                                text=strings.menu_quit,
                                help=strings.menu_quit_help)
