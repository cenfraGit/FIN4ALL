import wx
import os
import json
from .custom.utils.dip import dip

from src.custom.CustomStaticText import CustomStaticText
from src.custom.CustomScrolledWindow import CustomScrolledWindow
from src.gui.chatAssistant import FrameChatAssistant
from src.custom.CustomButton import CustomButton

from src.FrameQuiz import FrameQuiz


class FrameLesson(wx.Frame):
    def __init__(self, parent, course, lesson, lang, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.course = course
        self.lesson = lesson
        self.lang = lang

        self.SetTitle(f"{self.lang["frame_lesson_title"]} - {self.lesson}")
        self.SetInitialSize(dip(500, 500))

        self._init_menubar()

        self.lesson_data = self._get_lesson_data()


        self.mainPanel = wx.Panel(self)
        self.S_mainPanel = wx.BoxSizer()
        self.mainPanel.SetSizer(self.S_mainPanel)


        csw = CustomScrolledWindow(self.mainPanel)
        self.panel = csw.GetPanel()
        self.S_panel = wx.GridBagSizer()
        self.panel.SetSizer(self.S_panel)

        vertical_counter = 1


        # ---------------------- heading ------------------------ #

        header = wx.Panel(self.panel)
        S_header = wx.BoxSizer(wx.VERTICAL)
        header.SetSizer(S_header)

        title = wx.StaticText(header, label=self.lesson_data["title"])
        font_title = wx.Font(21, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        title.SetFont(font_title)

        subtitle = wx.StaticText(header, label=self.lesson_data["subtitle"])
        font_subtitle = wx.Font(18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        subtitle.SetFont(font_subtitle)
        subtitle.SetForegroundColour(wx.Colour(150, 150, 150))
    
        S_header.Add(title, 0, flag=wx.ALIGN_CENTER)
        S_header.Add(subtitle, 0, flag=wx.ALIGN_CENTER)

        self.S_panel.Add(header, pos=(0, 0), flag=wx.EXPAND)
        self.S_panel.AddGrowableCol(0, 1)


        # ---------------------- lesson content ------------------------ #

        for element in self.lesson_data["content"]:
            if element.startswith("text"):
                
                self.S_panel.Add(CustomStaticText(self.panel, label=self.lesson_data["content"][element], parentWordWrap=True, fontSize=11),
                                 pos=(vertical_counter, 0), flag=wx.EXPAND|wx.BOTTOM, border=dip(10))
                vertical_counter += 1


        quiz_button = CustomButton(self.panel, label=self.lang["buttons_quiz"])
        quiz_button.Bind(wx.EVT_BUTTON, self._on_quiz)

        self.S_panel.Add(quiz_button, pos=(vertical_counter, 0), flag=wx.EXPAND)
    

        # for i in range(40):
        #     self.S_panel.Add(wx.Button(self.panel, label="test"), pos=(i+2, 0))
        self.S_panel.Layout()

        

        # ---------------------- sizer setup ------------------------ #

        
        self.S_mainPanel.Add(csw, flag=wx.EXPAND, proportion=1)
        self.S_mainPanel.Layout()
        self.Layout()

    




    def _get_lesson_data(self):

        # get current script directory
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # go to lessons dir
        lessons_dir = os.path.join(script_dir, "..", "courses", self.course, self.lesson, "lesson.json")
        
        with open(lessons_dir, 'r', encoding='utf-8') as file:
            data_lesson = json.load(file)

        return data_lesson
    

    def _init_menubar(self):
        
        self.menubar = wx.MenuBar()

        fileMenu = wx.Menu()
        fileMenu.Append(102, self.lang["menubar_file_exit"], "")

        helpMenu = wx.Menu()
        helpMenu.Append(301, self.lang["menubar_help_assistant"])

        # add menus
        self.menubar.Append(fileMenu, self.lang["menubar_file"])
        self.menubar.Append(helpMenu, self.lang["menubar_help"])

        self.SetMenuBar(self.menubar)

        #self.Bind(wx.EVT_MENU, self.on_exit, id=101)

        self.Bind(wx.EVT_MENU, self._on_assistant, id=301)
        self.Bind(wx.EVT_MENU, self._on_exit, id=102)

    def _on_assistant(self, event):
        frame = FrameChatAssistant(parent=self)
        frame.Show()

    def _on_exit(self, event):
        self.Destroy()


    def _on_quiz(self, event):
        
        frame = FrameQuiz(self, self.course, self.lesson, self.lang)
        frame.Show()

        


        