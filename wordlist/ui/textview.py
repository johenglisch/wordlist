#!/usr/bin/env python2

'''textview.py - a simple text viewer window'''


import wx


class TextView(wx.Frame):
    '''simple text viewer window

    attributes:
        filename    the name of the text file
        text        the text to be displayed
        textctrl    the control displaying the text
    '''

    def __init__(self, text, filename, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)
        self.text = text
        self.filename = filename
        self.init_ui()
        self.Show()
        self.update_text()

    def init_ui(self):
        '''initialise user interface'''
        self.SetTitle("View '{0}'".format(self.filename))
        self.SetSize((300, 300))
        # text view
        self.textctrl = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.textctrl.SetEditable(False)

    def update_text(self):
        '''update text field'''
        self.textctrl.SetValue(self.text)
