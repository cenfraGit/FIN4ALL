# finance forward

__version__ = "1.0"

import wx
import json
import os
from src.custom import CustomConfig
from src.custom import CustomPanel
from src.custom.utils.dip import dip


class MainFrame(wx.Frame):
    def __init__(self, parent):

        super().__init__(parent)

        self._get_lang()
        self._init_ui()


    def _init_ui(self):

        self.SetTitle(f"Finance Forward v{__version__}")
        self.SetMinClientSize(dip(700, 400))

        self._init_menubar()

        # create main panel
        self.P_main = wx.Panel(self)
        self.P_main.SetBackgroundColour(wx.GREEN)
        self.S_main = wx.BoxSizer(wx.VERTICAL)
        self.P_main.SetSizer(self.S_main)


    def _init_menubar(self):
        
        self.menubar = wx.MenuBar()

        fileMenu = wx.Menu()
        fileMenu.Append(101, self.lang["menubar_file_preferences"], "")
        fileMenu.AppendSeparator()
        fileMenu.Append(102, self.lang["menubar_file_exit"], "")

        learnMenu = wx.Menu()
        learnMenu.Append(201, self.lang["menubar_learn_your_courses"], "")
        learnMenu.Append(201, self.lang["menubar_learn_explore_courses"], "")

        helpMenu = wx.Menu()
        helpMenu.Append(301, self.lang["menubar_help_about"])

        # add menus
        self.menubar.Append(fileMenu, self.lang["menubar_file"])
        self.menubar.Append(learnMenu, self.lang["menubar_learn"])
        self.menubar.Append(helpMenu, self.lang["menubar_help"])

        self.SetMenuBar(self.menubar)

        #self.Bind(wx.EVT_MENU, self.on_exit, id=101)


    def _get_lang(self):

        # get current script directory
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # open config
        config_path = os.path.join(script_dir, "..", "config.json")
        with open(config_path, 'r', encoding='utf-8') as file:
            data_config = json.load(file)

        # read language 
        languages_path = os.path.join(script_dir, "lang")
        language_json_path = os.path.join(languages_path, f"{data_config["language"]}.json")

        # save language as attributes
        with open(language_json_path, 'r', encoding='utf-8') as file:
            self.lang = json.load(file)

