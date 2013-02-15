import wx
import wordlist.ui.strings as strings
import wordlist.ui.menus as menus
import wordlist.ui.searchbar as searchbar
import wordlist.ui.toolbar as toolbar
import wordlist.ui.dialogs as dialogs
import wordlist.ui.wordlistview as wordlistview
import wordlist.wl as wl


class MainFrame(wx.Frame):
    def __init__(self, filename, *args, **kwargs):
        super(MainFrame, self).__init__(*args, **kwargs)
        self.filename = ''
        self.stoplist = list()
        self.wordlist = None
        self.init_ui()
        self.reset()
        self.Show()
        if filename:
            self.open_file(filename)

    def init_ui(self):
        # window properties
        self.SetTitle(strings.programme_name)
        self.SetSize((400, 400))

        # menu
        menubar = wx.MenuBar()
        self.filemenu = menus.FileMenu()
        self.editmenu = menus.EditMenu()
        self.viewmenu = menus.ViewMenu()
        menubar.Append(self.filemenu, strings.menu_file)
        menubar.Append(self.editmenu, strings.menu_edit)
        menubar.Append(self.viewmenu, strings.menu_view)
        self.SetMenuBar(menubar)

        # toolbar
        self.toolbar = toolbar.ToolBar(self)
        self.SetToolBar(self.toolbar)
        self.toolbar.Realize()

        # widgets
        self.wordlistview = wordlistview.WordlistView(parent=self)
        self.searchbar = searchbar.SearchBar(parent=self)

        # layout
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(item=self.wordlistview, proportion=1, flag=wx.EXPAND)
        vbox.Add(item=self.searchbar, proportion=0, flag=wx.EXPAND)
        self.SetSizer(vbox)
        self.searchbar.hide()

        # status bar
        self.statusbar = self.CreateStatusBar()

        # events
        self.Bind(event=wx.EVT_MENU, handler=self.on_open, id=wx.ID_OPEN)
        self.Bind(event=wx.EVT_MENU, handler=self.on_save, id=wx.ID_SAVE)
        self.Bind(event=wx.EVT_MENU, handler=self.on_close, id=wx.ID_CLOSE)
        self.Bind(event=wx.EVT_MENU, handler=self.on_quit, id=wx.ID_EXIT)
        self.Bind(event=wx.EVT_MENU, handler=self.searchbar.on_find,
                  id=wx.ID_FIND)
        self.Bind(event=wx.EVT_TOOL, handler=self.on_open, id=wx.ID_OPEN)
        self.Bind(event=wx.EVT_TOOL, handler=self.on_save, id=wx.ID_SAVE)

    def enable_controls(self, enable=True):
        self.filemenu.enable_items(enable)
        self.editmenu.enable_items(enable)
        self.viewmenu.enable_items(enable)
        self.toolbar.enable_tools(enable)

    def disable_controls(self):
        self.enable_controls(False)

    def on_open(self, event):
        dlg = dialogs.OpenDialog(parent=self)
        dlg.ShowModal()
        filename = dlg.GetPath()
        dlg.Destroy()
        if filename:
            self.open_file(filename)

    def on_close(self, event):
        self.reset()

    def on_save(self, event):
        dlg = dialogs.SaveDialog(parent=self)
        dlg.ShowModal()
        filename = dlg.GetPath()
        dlg.Destroy()
        if filename:
            self.save_file(filename)

    def on_quit(self, event):
        self.Close()

    def open_file(self, filename):
        try:
            with open(filename) as inputfile:
                new_text = inputfile.read()
        except IOError as error:
            msg = dialogs.ErrorDialog(self, str(error))
            msg.ShowModal()
        else:
            self.wordlist = wl.Wordlist(text=new_text, stoplist=self.stoplist)
            self.filename = filename
            self.wordlistview.set_wordlist(self.wordlist)
            self.enable_controls()

    def reset(self):
        self.wordlist = None
        self.stoplist = list()
        self.disable_controls()
        self.wordlistview.reset()
        self.searchbar.hide()

    def save_file(self, filename):
        lines = ['{word}\t{freq}'.format(word=word, freq=freq)
                 for word, freq in self.wordlistview.get_data()]
        try:
            with open(filename) as outputfile:
                new_text = inputfile.writelines(lines)
        except IOError as error:
            msg = dialogs.ErrorDialog(self, str(error))
            msg.ShowModal()
        else:
            filename = os.basename(filename)
            msg = dialogs.MessageDialog(self,
                                        strings.dlg_filesaved.format(filename))
