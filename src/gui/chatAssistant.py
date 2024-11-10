import wx
import ollama
import threading
from src.custom.utils.dip import dip


role = """
You are an asistant bot from now on. You will give short, brief and concise answers to the user from now on. The user will most likely ask you finance questions.
"""

class FrameChatAssistant(wx.Frame):

    def __init__(self, questionDataDict=None, problemDataDict=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.questionDataDict = questionDataDict
        self.problemDataDict = problemDataDict

        self.message_history = []

    
        self.init_ui()

        self.message_history.append({"role":"user", "content": role})
        self.message_history.append({"role":"assistant", "content": "How can I help you?"})

        self.chatBotReply("How can I help you?")

        self.userInputTextCtrl.SetFocus()


    def init_ui(self):
        
        self.SetTitle("Chat Assistant")

        self.mainPanel = wx.Panel(self)
        #self.mainPanel.SetBackgroundColour(wx.GREEN)
        self.mainPanel.sizer = wx.GridBagSizer()

        self.chatTextCtrl = wx.TextCtrl(self.mainPanel, style=wx.TE_READONLY|wx.TE_MULTILINE)
        #self.chatTextCtrl.Disable()
        self.userInputTextCtrl = wx.TextCtrl(self.mainPanel, style=wx.TE_PROCESS_ENTER)

        self.userInputTextCtrl.Bind(wx.EVT_TEXT_ENTER, self.OnUserEnter)

        self.mainPanel.sizer.Add(self.chatTextCtrl, pos=(0, 0), flag=wx.EXPAND|wx.ALL, border=dip(10))
        self.mainPanel.sizer.Add(self.userInputTextCtrl, pos=(1, 0), flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, border=dip(10))

        self.mainPanel.sizer.AddGrowableCol(0, 1)
        self.mainPanel.sizer.AddGrowableRow(0, 1)

        self.mainPanel.SetSizer(self.mainPanel.sizer)


    def OnUserEnter(self, event):

        userInputValue = self.userInputTextCtrl.GetValue()

        if (userInputValue.strip() != ""):

            userInputMessage = f"User: {userInputValue}\n\n"

            self.chatTextCtrl.AppendText(userInputMessage)

            self.userInputTextCtrl.SetValue("") # clear value

            self.response_thread = threading.Thread(target=self.getResponse, args=(userInputValue,))
            self.response_thread.start()


    def getResponse(self, prompt):

        self.message_history.append({'role': 'user', 'content': prompt})

        # stream = ollama.chat(
        #     model="llama3.2:1b",
        #     messages=self.message_history,
        #     stream=True,
        # )
        # for chunk in stream:
        #     print(chunk['message']['content'], end='', flush=True)

        response = ollama.chat(model="llama3.2:1b",
                    messages=self.message_history)
        
        self.message_history.append(response["message"])

        self.chatBotReply(response["message"]["content"])
        
        
         
    def chatBotReply(self, message):

        chatBoxMessage = f"Assistant: {message}\n\n"

        self.chatTextCtrl.AppendText(chatBoxMessage)

