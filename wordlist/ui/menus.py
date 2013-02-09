import wx
import strings


class FileMenu(wx.Menu):
    def __init__(self, *args, **kwargs):
        super(FileMenu, self).__init__(*args, **kwargs)
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


class EditMenu(wx.Menu):
    def __init__(self, *args, **kwargs):
        super(EditMenu, self).__init__(*args, **kwargs)
        self.find = self.Append(id=wx.ID_FIND,
                                text=strings.menu_find,
                                help=strings.menu_find_help)
        self.findnext = self.Append(id=wx.ID_ANY,
                                    text=strings.menu_findnext,
                                    help=strings.menu_findnext_help)
        self.AppendSeparator()
        self.stop = self.Append(id=wx.ID_ANY,
                                text=strings.menu_stop,
                                help=strings.menu_stop_help)

class ViewMenu(wx.Menu):
    def __init__(self, *args, **kwargs):
        super(ViewMenu, self).__init__(*args, **kwargs)
        self.bywords = self.AppendRadioItem(id=wx.ID_ANY,
                                            text=strings.menu_bywords,
                                            help=strings.menu_bywords_help)
        self.byends = self.AppendRadioItem(id=wx.ID_ANY,
                                           text=strings.menu_byends,
                                           help=strings.menu_byends_help)
        self.byfreq = self.AppendRadioItem(id=wx.ID_ANY,
                                           text=strings.menu_byfreq,
                                           help=strings.menu_byfreq_help)
