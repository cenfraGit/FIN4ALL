import wx
import os
import json
from src.custom.utils.dip import dip
from src.gui.dialogBase import DialogBase

from src.custom import CustomButton, CustomCheckBox, CustomRadioButton, CustomPanel, CustomStaticBox, CustomConfig


class DialogPreferences(DialogBase):
    def __init__(self, parent, lang, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.lang = lang
        self.config = self.get_config()

        self.SetTitle(self.lang["dialog_preferences_title"])
        self.SetInitialSize(dip(500, 500))
        
        self.mainPanel = wx.Panel(self.panel)

        self.mainPanel.sizer = wx.GridBagSizer()
        self.mainPanel.SetSizer(self.mainPanel.sizer)

        panelConfig = CustomConfig(border_colour_default=(150, 150, 150), 
                                   border_width_default=1,
                                   corner_radius_default=dip(5))
        

        p1 = CustomPanel(self.mainPanel, config=panelConfig)
        S_p1 = wx.BoxSizer()
        p1.SetSizer(S_p1)

        st1 = CustomStaticBox(p1, label=self.lang["dialog_preferences_auth"])
        st1_panel = st1.GetPanel()
        S_st1_panel = wx.GridBagSizer()
        st1_panel.SetSizer(S_st1_panel)

        email_textctrl = wx.TextCtrl(st1_panel, value=self.config["email"])
        password_textctrl = wx.TextCtrl(st1_panel, value=self.config["password"], style=wx.TE_PASSWORD)

        S_st1_panel.Add(wx.StaticText(st1_panel, label=f"{self.lang["dialog_preferences_email"]}:"), pos=(0, 0), flag=wx.ALIGN_RIGHT|wx.ALL, border=dip(7))
        S_st1_panel.Add(wx.StaticText(st1_panel, label=f"{self.lang["dialog_preferences_password"]}:"), pos=(1, 0), flag=wx.ALIGN_RIGHT|wx.ALL, border=dip(7))
        S_st1_panel.Add(email_textctrl, pos=(0, 1), flag=wx.EXPAND|wx.ALL, border=dip(7))
        S_st1_panel.Add(password_textctrl, pos=(1, 1), flag=wx.EXPAND|wx.ALL, border=dip(7))
        S_st1_panel.AddGrowableCol(1, 1)

        S_p1.Add(st1, 1, wx.EXPAND|wx.ALL, border=dip(10))







        p2 = CustomPanel(self.mainPanel, config=panelConfig)
        S_p2 = wx.BoxSizer()
        p2.SetSizer(S_p2)

        st2 = CustomStaticBox(p2, label=self.lang["dialog_preferences_language"])
        st2_panel = st2.GetPanel()
        S_st2_panel = wx.GridBagSizer()
        st2_panel.SetSizer(S_st2_panel)


        languages = {
            "English": "en_US",
            "Spanish": "es_MX",
            "Korean": "ko_KR",
            "Russian": "ru_RU",
            "Chinese": "zh_CN",
            "Japanese": "ja_JP"
        }

        for index, language in enumerate(languages.keys()):
            S_st2_panel.Add(CustomRadioButton(st2_panel, label=language), pos=(index, 0), flag=wx.ALIGN_LEFT|wx.ALL, border=dip(7))



        S_p2.Add(st2, 1, wx.EXPAND|wx.ALL, border=dip(10))







        self.mainPanel.sizer.Add(p1, pos=(0, 0), flag=wx.EXPAND)
        self.mainPanel.sizer.Add(p2, pos=(1, 0), flag=wx.EXPAND)



        self.mainPanel.sizer.AddGrowableCol(0, 1)
        self.panel.sizer.Add(window=self.mainPanel, proportion=1, flag=wx.EXPAND)


    def get_config(self):

        # get current script directory
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # go to lessons dir
        configdir = os.path.join(script_dir, "..", "config.json")
        
        with open(configdir, 'r', encoding='utf-8') as file:
            data = json.load(file)

        return data