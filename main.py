import wx
from src.MainFrame import MainFrame
from src.custom.utils.dpiAwareness import setDpiAwareness

setDpiAwareness()


if __name__ == "__main__":
    app = wx.App()
    frame = MainFrame(None)
    frame.Show()
    app.MainLoop()