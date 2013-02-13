import wx
import wordlist.ui.strings as strings
import wordlist.ui.menus as menus
import wordlist.ui.searchbar as searchbar
import wordlist.ui.toolbar as toolbar
import wordlist.ui.dialogs as dialogs
import wordlist.wl as wl


class MainFrame(wx.Frame):
    def __init__(self, filename, *args, **kwargs):
        super(MainFrame, self).__init__(*args, **kwargs)
        self.filename = ''
        self.stoplist = list()
        self.wordlist = None
        self.init_ui()
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
        self.wordlist = wx.ListCtrl(parent=self, style=wx.LC_REPORT)
        self.searchbar = searchbar.SearchBar(parent=self)

        # layout
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(item=self.wordlist, proportion=1, flag=wx.EXPAND)
        vbox.Add(item=self.searchbar, proportion=0, flag=wx.EXPAND)
        self.SetSizer(vbox)
        self.searchbar.hide()

        # status bar
        self.statusbar = self.CreateStatusBar()

        # events
        self.Bind(event=wx.EVT_MENU, handler=self.on_quit, id=wx.ID_EXIT)
        self.Bind(event=wx.EVT_MENU, handler=self.searchbar.on_find,
                  id=wx.ID_FIND)

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
