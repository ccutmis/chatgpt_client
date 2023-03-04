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
        quiz = self.input_msg.toPlainText()
        if quiz.strip() == "": return 
        self.show_msg.append("我 : \n\n"+quiz+'\n\n')
        completion = openai.ChatCompletion.create(
            model=model,
            messages=[
            {"role": "user", "content": quiz}
            ]
        )
        #return completion.choices[0].message['content']
        self.input_msg.setPlainText('')
        self.show_msg.append("GPT : \n"+completion.choices[0].message['content']+'\n\n')
    def save_chat_record(self):
        try:
            ans = self.show_dialog('另存文檔確認','確定要 將聊天內容另存為文字檔嗎? 按下確定後會開始另存...　過程中請勿操作滑鼠鍵盤。','Information',(QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No))
            if ans == 65536:
                return
            now = datetime.now()
            date_time = now.strftime("%Y%m%d_%H%M%S")
            with open(date_time+'.md','w+',encoding='utf-8') as f:
                f.write(self.show_msg.toPlainText())
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
    w.send_btn.clicked.connect(lambda:w.talk_to_chatGPT())
    w.save_btn.clicked.connect(lambda:w.save_chat_record())
    w.show()
    w.setWindowTitle("ChatGPT-MSN")
    app.exec()

if __name__ == "__main__" : main()