from PySide6.QtWidgets import QApplication,QMessageBox,QGraphicsOpacityEffect
from PySide6.QtGui import QKeySequence,QIcon
from PySide6.QtCore import QSize,QPropertyAnimation,QRect
from customLib.CustomMain import CustomUi
from customLib.TableWidget import TableWidget
from PySide6.QtCore import Qt,QCoreApplication


from datetime import datetime
import os
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")
conversation_history = []
used_tokens = 0

class Ui2(CustomUi):
    def set_folder_path(self):
        tmp = self.select_dir()
        if tmp != '':
            self.label_folder.setText(tmp)
    def set_file_path(self):
        tmp = self.select_file()
        if tmp[0] != '':
            self.label_file.setText(tmp[0])

    def talk_to_chatGPT(self,model="gpt-3.5-turbo"):
        global conversation_history,used_tokens
        quiz = self.input_msg.toPlainText()
        if quiz.strip() == "": return
        conversation_history.append({"role": "user", "content": quiz})
        now = datetime.now()
        date_time = now.strftime("%Y-%m-%d %H:%M:%S")
        self.show_msg.append("### "+date_time+' 我說 : \n'+quiz+'\n')
        completion = openai.ChatCompletion.create(
            model=model,
            messages=[{"role":x['role'],"content":x['content']} for x in conversation_history]
        )
        return_msg = completion.choices[0].message['content']
        conversation_history.append({"role": "assistant", "content": return_msg})
        self.input_msg.setPlainText('')
        now = datetime.now()
        date_time = now.strftime("%Y-%m-%d %H:%M:%S")
        self.show_msg.append("### "+date_time+" ChatGPT說 : \n"+return_msg+'\n\n-----\n')
        used_tokens = int(completion["usage"]["prompt_tokens"])
        self.label_token_count.setText('目前已使用Tokens: '+str(used_tokens))

    def save_chat_record(self):
        global conversation_history
        try:
            ans = self.show_dialog('另存文檔確認','確定要 將聊天內容另存為文字檔嗎? 按下確定後會開始另存...　過程中請勿操作滑鼠鍵盤。','Information',(QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No))
            if ans == 65536:
                return
            now = datetime.now()
            date_time = now.strftime("%Y%m%d_%H%M%S")
            with open(date_time+'.md','w+',encoding='utf-8') as f:
                f.write(self.show_msg.toPlainText()+"\n ## conversation_history: \n"+str(conversation_history).replace('},',',\n')+'\n\n已使用Tokens: '+str(used_tokens))
            self.show_dialog('另存文檔完成', '另存文檔完成，檔名為:'+date_time+'.md')
        except:
            pass


def main():
    import sys
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    app = QApplication(sys.argv)
    with open("resource/styles.qss") as f: 
        app.setStyleSheet(f.read())
    w = Ui2("resource/main.ui")
    w.setWindowIcon(QIcon('resource/images/chatgpt-icon.svg'))
    w.send_btn.clicked.connect(lambda:w.talk_to_chatGPT())
    w.save_btn.clicked.connect(lambda:w.save_chat_record())
    w.setWindowTitle("ChatGPT")
    w.setMinimumSize(800,600)
    w.show()
    app.exec()

if __name__ == "__main__" : main()