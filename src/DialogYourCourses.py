import wx
import os
from src.gui.dialogBase import DialogBase

from src.custom import CustomPanel
from src.custom import CustomButton
from src.custom import CustomStaticBox
from src.custom import CustomScrolledWindow
from src.custom.utils.dip import dip

from src.DialogYourCoursesLessons import DialogYourCoursesLessons


class DialogYourCourses(DialogBase):
    def __init__(self, parent, lang, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.lang = lang

        self.SetTitle(self.lang["dialog_your_courses_title"])
        self.SetInitialSize(dip(500, 600))
        
        self.mainPanel = CustomPanel(self.panel)
        #self.mainPanel.SetBackgroundColour(wx.CYAN)
        self.mainPanel.SetBackgroundColour(self.panel.GetBackgroundColour())
        self.mainPanel.sizer = wx.GridBagSizer()
        self.mainPanel.SetSizer(self.mainPanel.sizer)


        # staticbox
        staticbox = CustomStaticBox(self.mainPanel, label=self.lang["dialog_your_courses_staticbox_label"])
        staticbox.SetBackgroundColour(self.panel.GetBackgroundColour())
        staticbox_panel = staticbox.GetPanel()
        staticbox_panel.SetBackgroundColour(self.panel.GetBackgroundColour())
        S_staticbox = wx.BoxSizer(wx.VERTICAL)
        staticbox_panel.SetSizer(S_staticbox)
        csw = CustomScrolledWindow(staticbox_panel)
        self.scrolledWindowButtons = csw.GetPanel()
        self.S_scrolledWindowButtons = wx.GridBagSizer()
        self.scrolledWindowButtons.SetSizer(self.S_scrolledWindowButtons)
        self.courses_display_buttons()

        self.S_scrolledWindowButtons.AddGrowableCol(0, 1)
        self.S_scrolledWindowButtons.Layout()

        S_staticbox.Add(csw, proportion=1, flag=wx.EXPAND)


        self.mainPanel.sizer.Add(staticbox, pos=(0, 0), flag=wx.EXPAND)


        self.mainPanel.sizer.AddGrowableRow(0, 1)
        self.mainPanel.sizer.AddGrowableCol(0, 1)

        self.mainPanel.sizer.Layout()
        

        self.panel.sizer.Add(window=self.mainPanel, proportion=1, flag=wx.EXPAND) 


    def courses_display_buttons(self):

        # get current script directory
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # go to courses dir
        courses_dir = os.path.join(script_dir, "..", "courses")

        courses_list = os.listdir(courses_dir)

        for index, course in enumerate(courses_list):
            button = CustomButton(self.scrolledWindowButtons, label=course)
            self.S_scrolledWindowButtons.Add(button, pos=(index, 0), flag=wx.EXPAND)
            button.Bind(wx.EVT_BUTTON, self._on_button)

    def _on_button(self, event:wx.Event):

        button:CustomButton = event.GetEventObject()

        buttonLabel = button.GetLabel() # course

        dlg = DialogYourCoursesLessons(self, self.lang, buttonLabel)
        dlg.ShowModal()
