#!/usr/bin/env python3
import wx
class Example(wx.Frame):
    def __init__(self, parent, title):
        super(Example, self).__init__(parent, title=title, size=(640,480))
        self.InitUI()
        self.opts = [ ]
        self.URL = "http://example.com"
    def InitUI(self):
        panel = wx.Panel(self)

        self.cb1 = wx.CheckBox(panel, label='Random Agent', pos=(10,  80))
        self.cb2 = wx.CheckBox(panel, label='Dump all', pos=(140, 80))

        self.cmd_input_lable = wx.StaticText(panel, label = "URL", pos = (10,15))
        self.url = wx.TextCtrl(panel, value="https://exmaple.com", pos = (50, 10), size=(580, 24))
        self.cmd_input_lable = wx.StaticText(panel, label = "CMD", pos = (10,45))
        self.cmd_inp = wx.TextCtrl(panel, value="sqlmap -u https://example.com", pos = (50, 40), style = wx.TE_READONLY, size=(580, 24))
        
        self.Bind(wx.EVT_CHECKBOX,self.onChecked)
        self.Centre()
        self.Show(True)

    def onChecked(self, e):
        vopt = {
            'Random Agent':'--random-agnet ',
            'Dump all': '--dump-all '
        }
        cb = e.GetEventObject()
        opt = vopt[ cb.GetLabel() ]
        if cb.GetValue():
            self.opts.append( opt )
        else:
            self.opts.remove( opt ) 
        self.cmd_inp.ChangeValue( self.gen( URL=self.URL, opts=self.opts ) )
        # print( self.cmd_inp. )
        # self.cmd_inp

    @staticmethod
    def gen( URL="", opts=[] ):
        cmd_txt = "sqlmap "
        cmd_txt += "-u '" + URL + "' "
        for opt in opts:
            cmd_txt += opt
        print( cmd_txt )
        return cmd_txt

ex = wx.App()
Example(None, 'CheckBox')
ex.MainLoop()
