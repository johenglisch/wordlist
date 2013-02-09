import wx
import strings
import menus
import searchbar


class MainFrame(wx.Frame):
    def __init__(self, filename, parent):
        super(MainFrame, self).__init__(parent)
        self.init_ui()
        self.SetSize((400, 400))
        self.SetTitle(strings.programme_name)
        self.Show()

    def init_ui(self):
        # menu
        menubar = wx.MenuBar()
        self.filemenu = menus.FileMenu()
        self.editmenu = menus.EditMenu()
        self.viewmenu = menus.ViewMenu()
        menubar.Append(self.filemenu, strings.menu_file)
        menubar.Append(self.editmenu, strings.menu_edit)
        menubar.Append(self.viewmenu, strings.menu_view)
        self.SetMenuBar(menubar)

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
