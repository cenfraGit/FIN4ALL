import wx
from wx.lib import sized_controls

class DialogBase(sized_controls.SizedDialog):

    """
    Base Dialog class for creating sized dialogs.
    The main panel is self.panel and its sizer is in self.panel.sizer.
    self.panel.sizer is a BoxSizer oriented vertically.
    """

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent=parent, style=wx.RESIZE_BORDER|wx.CAPTION|wx.CLOSE_BOX, *args, **kwargs)

        self._originalPanel = self.GetContentsPane()
        self._originalPanel.SetSizerType("grid", {"rows":1,"cols":1, "growable_col":(0,1), "growable_row":(0,1)})

        self.panel = wx.Panel(self._originalPanel)
        self.panel.sizer = wx.BoxSizer(wx.VERTICAL)

        self.panel.SetSizer(self.panel.sizer)
        self.panel.SetSizerProps(expand=True)


# EXAMPLE
""" 
class DialogTestResults(DialogBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        
        self.mainPanel = wx.Panel(self.panel)
        self.mainPanel.SetBackgroundColour(wx.CYAN)

        self.mainPanel.sizer = wx.GridBagSizer()
        self.mainPanel.SetSizer(self.mainPanel.sizer)

        self.panel.sizer.Add(window=self.mainPanel, proportion=1, flag=wx.EXPAND) 
"""