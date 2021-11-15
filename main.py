#!/usr/bin/env python3
import wx
import os
import threading

class Example(wx.Frame):
    def __init__(self, parent, title):
        super(Example, self).__init__(parent, title=title, size=(640,480))
        self.InitUI()
        self.opts = [ ]
        self.URL = "http://example.com"

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update, self.timer)

    def onToggle(self, event):
        btnLabel = self.toggleBtn.GetLabel()
        if btnLabel == "Start":
            print( "starting timer...")
            self.timer.Start(1000)
            self.toggleBtn.SetLabel("Stop")
        else:
            print( "timer stopped!")
            self.timer.Stop()
            self.toggleBtn.SetLabel("Start")
            
    def update(self, event):
        f = open('output.txt', 'r')
        # print( f.read() )
        self.outputbox.ChangeValue( f.read() )
        f.close()
        # print( "\nupdated: ")
        # print( time.ctime())

    def InitUI(self):
        panel = wx.Panel(self)

        self.cb1 = wx.CheckBox(panel, label='Random Agent', pos=(10,  80))
        self.cb2 = wx.CheckBox(panel, label='Dump all', pos=(140, 80))

        self.cmd_input_lable = wx.StaticText(panel, label = "URL", pos = (10,15))
        self.url = wx.TextCtrl(panel, value="https://exmaple.com", pos = (50, 10), size=(580, 24))
        self.url.Bind(wx.EVT_TEXT, self.OnKeyTyped)

        self.cmd_input_lable = wx.StaticText(panel, label = "CMD", pos = (10,45))
        self.cmd_inp = wx.TextCtrl(panel, value="sqlmap -u https://example.com", pos = (50, 40), style = wx.TE_READONLY, size=(480, 24))

        self.exec_btn = wx.Button(panel, label = 'Execute', pos = (540,35))

        self.outputbox = wx.TextCtrl(panel, value="System loading...\nOK\n\n", pos = (10, 120), style = wx.TE_READONLY | wx.TE_MULTILINE, size=(620, 300))


        self.Bind(wx.EVT_BUTTON, self.OnButtonClicked)
        self.Bind(wx.EVT_CHECKBOX,self.onChecked)
        self.Centre()
        self.Show(True)

    def OnButtonClicked(self, e): 
        print('click event received by frame class') 
        cmd = self.gen( URL=self.URL, opts=self.opts ) + '--answers="follow=Y" --batch '
        print( cmd )

        self.timer.Start(1000)
        output = os.system( cmd + " | tee output.txt" )
        # self.outputbox.ChangeValue( output )
        # print(  )
        # print( os.system( cmd + " > output.txt" ) )
        # e.Skip()

    def onChecked(self, e):
        vopt = {
            'Random Agent':'--random-agent ',
            'Dump all': '--dump-all '
        }
        cb = e.GetEventObject()
        opt = vopt[ cb.GetLabel() ]
        if cb.GetValue():
            self.opts.append( opt )
        else:
            self.opts.remove( opt ) 

        self.cmd_inp.ChangeValue( self.gen( URL=self.URL, opts=self.opts ) )
        
    def OnKeyTyped(self, event): 
        print( event.GetString() )
        self.URL = event.GetString()

        self.cmd_inp.ChangeValue( self.gen( URL=self.URL, opts=self.opts ) )

    @staticmethod
    def gen( URL="", opts=[] ):
        cmd_txt = "sqlmap "
        cmd_txt += "-u '" + URL + "' "
        for opt in opts:
            cmd_txt += opt
        print( cmd_txt )
        return cmd_txt

ex = wx.App()
Example(None, 'SQL Injection toolkit')
ex.MainLoop()
