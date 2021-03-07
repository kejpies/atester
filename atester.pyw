#!/usr/bin/env python

#    Copyright (C) 2021 Konrad Sekuła
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

# atester.pyw

import wx

class Atester(wx.Frame):
    req="GET / HTTP/1.1\r\nHost: example.com\r\n"
    host="example.com | 80"

    conf=[]
    def __init__(self, *args, **kwargs):
        super(Atester, self).__init__(*args, **kwargs)

        self.InitUI()
        self.Centre()

    def InitUI(self):
        # Menubar
        menubar = wx.MenuBar()
        menu = wx.Menu()
        menubar.Append(menu, '&Atester')

        _open=menu.Append(wx.ID_OPEN, '&Open configuration file')
        _save=menu.Append(wx.ID_SAVE, '&Save configuration file')

        menu.AppendSeparator()

        _quit = menu.Append(wx.ID_EXIT, 'Quit', 'Quit application')
        
        self.SetMenuBar(menubar)

        # Main UI
        panel=wx.Panel(self)
        font=wx.SystemSettings.GetFont(wx.SYS_ANSI_VAR_FONT)
        font.SetPointSize(10)
        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        st1 = wx.StaticText(panel, label='Host | Port')
        st1.SetFont(font)
        hbox1.Add(st1,flag=wx.RIGHT,border=8)
        self.tc = wx.TextCtrl(panel)
        self.tc.write('example.com | 80')
        hbox1.Add(self.tc, proportion=1)
        vbox.Add(hbox1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

        st2 = wx.StaticText(panel, label='Request')
        st2.SetFont(font)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.tc2 = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        hbox2.Add(st2,flag=wx.RIGHT|wx.TOP|wx.BOTTOM,border=8)
        self.tc2.write('GET / HTTP/1.1\r\nHost: example.com\r\n\r\n')
        vbox.Add((-1, 10))
        hbox2.Add(self.tc2, proportion=1, flag=wx.EXPAND)
        vbox.Add(hbox2, proportion=1, flag=wx.LEFT|wx.RIGHT|wx.EXPAND,
            border=15)

        
        
        vbox.Add((-1, 25))

        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        btn1 = wx.Button(panel, label='Send', size=(70, 30))
        self.cbssl = wx.CheckBox(panel, label = 'SSL?')
        hbox3.Add(self.cbssl)
        hbox3.Add(btn1)
        vbox.Add(hbox3, flag=wx.ALIGN_RIGHT|wx.RIGHT|wx.BOTTOM, border=10)

        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        self.tc3 = wx.TextCtrl(panel, style=wx.TE_MULTILINE|wx.TE_READONLY)
        hbox4.Add(self.tc3, proportion=1, flag=wx.EXPAND)
        vbox.Add(hbox4, proportion=1, flag=wx.LEFT|wx.RIGHT|wx.EXPAND,
            border=15)


        panel.SetSizer(vbox)

        # Binds
        
        self.Bind(wx.EVT_MENU, self.OnQuit, _quit)
        self.Bind(wx.EVT_MENU, self.OpenFile, _open)
        self.Bind(wx.EVT_MENU, self.SaveFile, _save)

        self.Bind(wx.EVT_BUTTON,self.SendPressed,btn1)

        self.Bind(wx.EVT_TEXT, self.OnEditH,self.tc)
        self.Bind(wx.EVT_TEXT, self.OnEditR,self.tc2)

        # Ending

        self.SetSize((750, 500))
        self.SetTitle('Atester')

    def OnEditH(self,e):
        self.host=self.tc.GetValue()
    def OnEditR(self,e):
        self.req=self.tc2.GetValue()

    def OnQuit(self, e):
        self.Close()

    def SendPressed(self, e):
        from sender import Sender
        self.host=self.host.strip()
        self.req=self.req.strip()
        print(self.host)
        print(self.req)
        __port=int(self.host.split("|")[1].strip())
        __host=self.host.split("|")[0].strip()
        self.tc3.SetValue(Sender.Send(__host,__port,self.req+"\r\n\r\n",self.cbssl.GetValue()).decode("utf-8"))

    def OpenFile(self,e):
        with wx.FileDialog(self, "Open configuration file", wildcard="Atester files (*.at)|*.at",style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            pathname = fileDialog.GetPath()
            try:
                with open(pathname, 'r') as file:
                    conf=file.readlines()
                    self.host=conf[0].strip()
                    self.req="".join(conf[1:-1])
                    self.req=self.req.lstrip()
                    self.tc.write(self.host)
                    self.tc2.write(self.req)
            except IOError:
                wx.MessageBox("An error occured during reading a file", 'Error', wx.OK | wx.ICON_ERROR)
    def SaveFile(self,e):
        with wx.FileDialog(self, "Save configuration file", wildcard="AT files (*.at)|*.at",style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            pathname = fileDialog.GetPath()
            try:
                with open(pathname, 'w') as file:
                    file.write(self.host+"\r\n"+self.req+"\r\n")
                    file.close()
            except IOError:
                wx.MessageBox("An error occured during saving a file", 'Error', wx.OK | wx.ICON_ERROR)


def main():

    app = wx.App()
    at = Atester(None,style=wx.MINIMIZE_BOX | wx.RESIZE_BORDER | 
                            wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX)
    at.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()
    