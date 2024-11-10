import wx
import os
import json
from .custom.utils.dip import dip

from src.custom.CustomStaticText import CustomStaticText
from src.custom.CustomScrolledWindow import CustomScrolledWindow
from src.gui.chatAssistant import FrameChatAssistant
from src.custom.CustomButton import CustomButton
from src.custom.CustomPanel import CustomPanel
from src.custom.CustomConfig import CustomConfig
from src.custom.CustomRadioButton import CustomRadioButton
import ollama


class FrameQuiz(wx.Frame):
    def __init__(self, parent, course, lesson, lang, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.course = course
        self.lesson = lesson
        self.lang = lang

        self.SetTitle(f"{self.lang["frame_quiz_title"]} - {self.lesson}")
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


        # ---------------------- lesson content ------------------------ #

        panelConfig = CustomConfig(corner_radius_default=dip(5),
                                   border_width_default=1,
                                   border_colour_default=(150, 150, 150))

        for element in self.lesson_data["questions"]:



            panel = CustomPanel(self.panel, config=panelConfig)
            S_panel = wx.GridBagSizer()
            panel.SetSizer(S_panel)

            # ---------------------- question  ------------------------ #

            text = CustomStaticText(panel, label=element["question"], parentWordWrap=True, fontSize=11)

            # ----------------------  answer box  ------------------------ #

            if ("type" in element) and (element["type"] == "open"): # open question

                answer_box = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
            
            else:

                answer_box = wx.Panel(panel)
                answer_box.SetBackgroundColour(wx.WHITE)
                S_answer_box = wx.BoxSizer(wx.VERTICAL)
                radio_buttons = []
                for option in element["options"]:
                    rb = CustomRadioButton(answer_box, label=option, background_colour_default=(255, 255, 255))
                    radio_buttons.append(rb)
                    S_answer_box.Add(rb, 0, wx.ALIGN_LEFT)
                answer_box.SetSizer(S_answer_box)
                    
            # ---------------------- buttons ------------------------ #

            button_panel = wx.Panel(panel)
            button_panel.SetBackgroundColour(wx.WHITE)
            S_button_panel = wx.BoxSizer()
            button_panel.SetSizer(S_button_panel)

            button1 = CustomButton(button_panel, label=self.lang["button_check"])
            button2 = CustomButton(button_panel, label=self.lang["button_assistant"])
            status = wx.StaticText(button_panel, label="")

            S_button_panel.Add(button1, 0, flag=0)
            S_button_panel.Add(button2, 0, flag=0)
            S_button_panel.Add(status, 0, flag=wx.ALIGN_CENTER)

            S_button_panel.Layout()

            # ---------------------- logic ------------------------ #
            def make_check_function(element, answer_box, status, radio_buttons=None):
                def check(event):
                    question = element["question"]
                    if ("type" in element) and (element["type"] == "open"):  # open question
                        answer = answer_box.GetValue()
                        answer_status = self._check_open(question, answer)
                    else:  # multiple choice question
                        selected_option = next((rb.GetLabel() for rb in radio_buttons if rb.GetValue()), None)
                        answer_status = "Correct" if selected_option == element["correct_answer"] else "Incorrect"

                    if answer_status.lower().startswith("correct"):
                        status.SetLabel("Correct")
                        status.SetForegroundColour(wx.Colour(0, 180, 0))
                    else:
                        status.SetLabel("Incorrect")
                        status.SetForegroundColour(wx.Colour(180, 0, 0))
                    button_panel.Layout()
                    S_button_panel.Layout()
                    S_panel.Layout()

                    print(question)
                    print(answer if ("type" in element) and (element["type"] == "open") else selected_option)
                    print(answer_status)

                return check

            self.Bind(wx.EVT_BUTTON, make_check_function(element, answer_box, status, radio_buttons if not ("type" in element) or element["type"] != "open" else None), id=button1.GetId())




            S_panel.Add(text, pos=(0, 0), flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=dip(8))
            S_panel.Add(answer_box, pos=(1, 0), flag=wx.EXPAND|wx.ALL, border=dip(8))
            S_panel.Add(button_panel, pos=(2, 0), flag=wx.EXPAND|wx.ALL, border=dip(8))
            S_panel.AddGrowableCol(0, 0)

            S_panel.Layout()

            self.S_panel.Add(panel, pos=(vertical_counter, 0), flag=wx.EXPAND|wx.BOTTOM, border=dip(8))
            vertical_counter += 1




        end_button = CustomButton(self.panel, label=self.lang["buttons_end"])
        end_button.Bind(wx.EVT_BUTTON, self._on_end)

        self.S_panel.Add(end_button, pos=(vertical_counter, 0), flag=wx.EXPAND)
    
        self.S_panel.Layout()


        # ---------------------- sizer setup ------------------------ #

        self.S_panel.AddGrowableCol(0, 1)
        self.S_mainPanel.Add(csw, flag=wx.EXPAND, proportion=1)
        self.S_mainPanel.Layout()
        self.Layout()

    

    def _check_open(self, question, answer):

        if answer.strip() == "":
            return "incorrect"

        message_history = []

        message_history.append({'role': 'user', 'content': "i am going to give you a question and my answer. if you think that the answer is correct (dont be so strict) for the question, answer with one lowercase word: 'correct'. otherwise, answer 'incorrect'. then, explain why it is right or wrong in one concise sentence."})

        message_history.append({"role": "user", "content": f"the question is: {question}. the answer is {answer}"})

        response = ollama.chat(model="llama3.2",
                    messages=message_history)
        
        return response["message"]["content"]




    def _get_lesson_data(self):

        # get current script directory
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # go to lessons dir
        lessons_dir = os.path.join(script_dir, "..", "courses", self.course, self.lesson, "quiz.json")
        
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


    def _on_end(self, event):
        
        self.Destroy()


    