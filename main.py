import wx
from custom import *
from custom.utils.dip import dip
from custom.utils.dpiAwareness import setDpiAwareness

setDpiAwareness()


class Main(wx.Frame):
    def __init__(self, parent):

        super().__init__(parent)

        self.SetTitle("Finance Diagnostics")
        self.SetMinClientSize(dip(300, 300))



if __name__ == "__main__":
    app = wx.App()
    frame = Main(None)
    frame.Show()
    app.MainLoop()
    
