from datetime import datetime
import os
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")
import tkinter as tk
import tkinter.messagebox as mbox
from tkinter.ttk import *

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.conversation_history = []
        self.pack()
        self.create_widgets()
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def create_widgets(self):
        #建立唯讀的文字方塊
        self.output_box = tk.Text(self,font=("Helvetica", 16), height=10)
        self.output_box.config(state="disabled")
        self.output_box.grid(row=0, column=0, sticky='nsew')
        #self.entry = tk.Entry(self)
        #self.entry.grid(row=1, column=0, sticky='nsew')
        #建立可以輸入多行文字的 Text 方塊
        self.input_box = tk.Text(self,font=("Helvetica", 16), height=5)
        self.input_box.grid(row=1, column=0, sticky='nsew')
        self.button = tk.Button(self, text="送出問題",font=("Helvetica", 24),command=lambda: self.submit(), height=1)
        self.button.grid(row=2, column=0, sticky='nsew')
        self.button_save = tk.Button(self, text="另存對話",font=("Helvetica", 24),command=lambda: self.save_chat_record(), height=1)
        self.button_save.grid(row=3, column=0, sticky='nsew')

    def save_chat_record(self):
        answer = mbox.askyesno("另存對話確認", "確定要 將聊天內容另存為文字檔嗎? 按下確定後會開始另存...　過程中請勿操作滑鼠鍵盤。")
        if answer:
            now = datetime.now()
            date_time = now.strftime("%Y%m%d_%H%M%S")
            with open(date_time+'.md','w+',encoding='utf-8') as f:
                f.write(self.output_box.get("1.0",tk.END))
            #mbox.showinfo("提示", "您選擇了繼續！")
        else:
            return


    def submit(self):
        #取得輸入的文字
        quiz = self.input_box.get("1.0", tk.END)

        #quiz = input_msg.toPlainText()
        if quiz.strip() == "": return
        self.conversation_history.append({"role": "user", "content": quiz})
        now = datetime.now()
        date_time = now.strftime("%Y-%m-%d %H:%M:%S")

        #將文字添加至唯讀方塊
        self.output_box.config(state="normal")
        self.output_box.insert(tk.END, "### "+date_time+' 我說 : \n'+quiz+'\n')
        #output_box.see(tk.END)
        #output_box.config(state="disabled")
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role":x['role'],"content":x['content']} for x in self.conversation_history]
        )
        return_msg = completion.choices[0].message['content']
        self.conversation_history.append({"role": "assistant", "content": return_msg})
        #清空輸入方塊
        self.input_box.delete("1.0", tk.END)
        now = datetime.now()
        date_time = now.strftime("%Y-%m-%d %H:%M:%S")
        self.output_box.insert(tk.END, "### "+date_time+" ChatGPT說 : \n"+return_msg+'\n\n-----\n')
        self.output_box.see("end")

root = tk.Tk()
app = Application(master=root)
app.mainloop()