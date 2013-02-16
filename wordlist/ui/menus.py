import wx
import wordlist.ui.strings as strings


class FileMenu(wx.Menu):
    def __init__(self, *args, **kwargs):
        super(FileMenu, self).__init__(*args, **kwargs)
        self.openf = self.Append(id=wx.ID_OPEN,
                                 text=strings.menu_open,
                                 help=strings.help_open)
        self.savef = self.Append(id=wx.ID_SAVE,
                                 text=strings.menu_save,
                                 help=strings.help_save)
        self.closef = self.Append(id=wx.ID_CLOSE,
                                  text=strings.menu_close,
                                  help=strings.help_close)
        self.AppendSeparator()
        self.quit = self.Append(id=wx.ID_EXIT,
                                text=strings.menu_quit,
                                help=strings.help_quit)

    def enable_items(self, enable=True):
        self.savef.Enable(enable)
        self.closef.Enable(enable)

    def disable_items(self):
        self.enable_items(False)


class EditMenu(wx.Menu):
    def __init__(self, *args, **kwargs):
        super(EditMenu, self).__init__(*args, **kwargs)
        self.find = self.Append(id=wx.ID_FIND,
                                text=strings.menu_find,
                                help=strings.help_find)
        self.findnext = self.Append(id=wx.ID_ANY,
                                    text=strings.menu_findnext,
                                    help=strings.help_findnext)
        self.AppendSeparator()
        self.stop = self.Append(id=wx.ID_ANY,
                                text=strings.menu_stop,
                                help=strings.help_stop)

    def enable_items(self, enable=True):
        self.find.Enable(enable)
        self.findnext.Enable(enable)
        self.stop.Enable(enable)

    def disable_items(self):
        self.enable_items(False)


class ViewMenu(wx.Menu):
    def __init__(self, *args, **kwargs):
        super(ViewMenu, self).__init__(*args, **kwargs)
        self.bywords = self.AppendRadioItem(id=wx.ID_ANY,
                                            text=strings.menu_bywords,
                                            help=strings.help_bywords)
        self.byends = self.AppendRadioItem(id=wx.ID_ANY,
                                           text=strings.menu_byends,
                                           help=strings.help_byends)
        self.byfreq = self.AppendRadioItem(id=wx.ID_ANY,
                                           text=strings.menu_byfreq,
                                           help=strings.help_byfreq)

    def enable_items(self, enable=True):
        self.bywords.Enable(enable)
        self.byends.Enable(enable)
        self.byfreq.Enable(enable)

    def disable_items(self):
        self.enable_items(False)

    def reset(self):
        self.bywords.Check()
