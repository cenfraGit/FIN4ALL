import wx
import os
from src.gui.dialogBase import DialogBase

from src.custom import CustomPanel
from src.custom import CustomButton
from src.custom import CustomStaticBox
from src.custom import CustomScrolledWindow
from src.custom.utils.dip import dip
import json

from src.FrameLesson import FrameLesson


class DialogYourCoursesLessons(DialogBase):
    def __init__(self, parent, lang, course, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.lang = lang
        self.course = course

        self.SetTitle(f"{self.lang["dialog_your_courses_lessons_title"]} - {course}")
        self.SetInitialSize(dip(500, 600))
        
        self.mainPanel = CustomPanel(self.panel)
        #self.mainPanel.SetBackgroundColour(wx.CYAN)
        self.mainPanel.SetBackgroundColour(self.panel.GetBackgroundColour())
        self.mainPanel.sizer = wx.GridBagSizer()
        self.mainPanel.SetSizer(self.mainPanel.sizer)


        # staticbox
        staticbox = CustomStaticBox(self.mainPanel, label=self.lang["dialog_your_courses_lessons_staticbox_label"])
        staticbox.SetBackgroundColour(self.panel.GetBackgroundColour())
        staticbox_panel = staticbox.GetPanel()
        staticbox_panel.SetBackgroundColour(self.panel.GetBackgroundColour())
        S_staticbox = wx.BoxSizer(wx.VERTICAL)
        staticbox_panel.SetSizer(S_staticbox)
        csw = CustomScrolledWindow(staticbox_panel)
        self.scrolledWindowButtons = csw.GetPanel()
        self.S_scrolledWindowButtons = wx.GridBagSizer()
        self.scrolledWindowButtons.SetSizer(self.S_scrolledWindowButtons)
        self.lessons_display_buttons()

        self.S_scrolledWindowButtons.AddGrowableCol(0, 1)
        self.S_scrolledWindowButtons.Layout()

        S_staticbox.Add(csw, proportion=1, flag=wx.EXPAND)


        self.mainPanel.sizer.Add(staticbox, pos=(0, 0), flag=wx.EXPAND)


        self.mainPanel.sizer.AddGrowableRow(0, 1)
        self.mainPanel.sizer.AddGrowableCol(0, 1)

        self.mainPanel.sizer.Layout()
        

        self.panel.sizer.Add(window=self.mainPanel, proportion=1, flag=wx.EXPAND) 


    def lessons_display_buttons(self):

        # get current script directory
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # go to lessons dir
        lessons_dir = os.path.join(script_dir, "..", "courses", self.course)

        lessons_list = os.listdir(lessons_dir)

        # get progress
        progress_path = os.path.join(script_dir, "..", "progress.json")
        with open(progress_path, 'r', encoding='utf-8') as file:
            data_progress = json.load(file)


        color_completed = (0, 200, 0)
        color_incompleted = (200, 0, 0)

        for index,lesson in enumerate(lessons_list):

            color = color_completed if (lesson in data_progress["course_lessons_completed"][self.course]) else color_incompleted
            
            button = CustomButton(self.scrolledWindowButtons, label=lesson, text_foreground_colour_default=color)
            self.S_scrolledWindowButtons.Add(button, pos=(index, 0), flag=wx.EXPAND)
            button.Bind(wx.EVT_BUTTON, self._on_button)


    def _on_button(self, event:wx.Event):

        button:CustomButton = event.GetEventObject()

        buttonLabel = button.GetLabel() # lesson

        lesson = FrameLesson(self, self.course, buttonLabel, self.lang)
        lesson.Show()