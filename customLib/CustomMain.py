from PySide6.QtWidgets import *
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import *
from PySide6.QtGui import *
import sys, os, re, codecs, ctypes, platform

class CustomUi(QMainWindow):
    def __init__(self,ui_path,window_title='title name'):
        super(CustomUi,self).__init__()
        # Required to change taskbar icon
        if platform.system() == "Windows":
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
                "com.random.appID")
        self.setting_file_path = "resource/setting.txt"
        self.setting = {}
        self.read_setting()
        ui_file = QFile(ui_path)
        if not ui_file.open(QIODevice.ReadOnly):
            print(f"Cannot open {ui_path}: {ui_file.errorString()}")
            return

        loader = QUiLoader()
        ui = loader.load(ui_file)
        ui_file.close()
        if not ui:
            print(loader.errorString())
            return
        tmp_dict = self.declare_variables_by_ui(ui_path)
        content = ""
        for i in tmp_dict.keys(): content += tmp_dict[i]+'\n'
        #print(content)
        #with open('loadUi_test_content.txt','w+',encoding='utf-8') as f:
        #    f.write(content)
        exec(content)
        self.setCentralWidget(ui)

    def declare_variables_by_ui(self,ui_loc):
        with open(ui_loc,'r',encoding='utf-8') as f:
            ui_source = f.read()
        tmp_dict = {}
        tmp_tuple = ()
        ls = re.findall('<(widget|layout) class="([^"]*)" name="([^"]*)"',ui_source,re.DOTALL)
        for i in ls:
            obj_type,obj_name = i[1],i[2]
            if obj_name in tmp_tuple: continue
            tmp_tuple += (obj_name,)
            # fix class issue
            if obj_type == 'Line': obj_type = 'QLine'
            if obj_name in ('MainWindow','centralwidget'): continue
            tmp_dict[obj_name] = "self."+obj_name+" = ui.findChild("+obj_type+", '"+obj_name+"')"
        # process QAction items
        ls = re.findall('<widget class="QMenu" name="[^"]*">.*?</widget>',ui_source,re.DOTALL)
        for i in ls:
            qaction_ls = re.findall('<addaction name="([^"]*)"/>',i,re.DOTALL)
            for j in qaction_ls:
                obj_type,obj_name = 'QAction',j
                if obj_name in tmp_tuple: continue
                tmp_tuple += (obj_name,)
                tmp_dict[obj_name] = "self."+obj_name+" = ui.findChild("+obj_type+", '"+obj_name+"')"
        # process QToolBar items
        ls = re.findall('<widget class="QToolBar" name="[^"]*">.*?</widget>',ui_source,re.DOTALL)
        for i in ls:
            qaction_ls = re.findall('<addaction name="([^"]*)"/>',i,re.DOTALL)
            for j in qaction_ls:
                obj_type,obj_name = 'QAction',j
                if obj_name in tmp_tuple: continue
                tmp_tuple += (obj_name,)
                tmp_dict[obj_name] = "self."+obj_name+" = ui.findChild("+obj_type+", '"+obj_name+"')"
        return tmp_dict

    def open_file(self):
        path = QFileDialog.getOpenFileName(self, "Open")[0]
        if path:
            if self.detect_by_bom(path) == 'utf-8':
                with open(path, 'r', encoding='utf-8') as f:
                    tmp = f.read()
            else: #utf-16
                with open(path,'rb') as f:
                    tmp = f.read()
                tmp = str(tmp, 'utf-16')
            self.file_path = path
            print(tmp)
            return ( tmp )
        else:
            return None

    def close_app(self): sys.exit()

    def detect_by_bom(self,path, default='utf-8'):
        with open(path, 'rb') as f:
            raw = f.read(4)  # will read less if the file is smaller
        for enc, boms in \
                ('utf-8-sig', (codecs.BOM_UTF8,)),\
                ('utf-16', (codecs.BOM_UTF16_LE, codecs.BOM_UTF16_BE)),\
                ('utf-32', (codecs.BOM_UTF32_LE, codecs.BOM_UTF32_BE)):
            if any(raw.startswith(bom) for bom in boms):
                return enc
        return default 

    def read_setting(self):
        app_current_path = os.getcwd()+'\\'
        if os.path.exists(self.setting_file_path)==False: # 找不到設定檔
            # 用 resource\\setting_template 重建
            with open(app_current_path+'resource/setting_template','r',encoding='utf-8') as f:
                template_txt = f.read()
            value_ls=re.findall(r"^([^\t]+)\t([^\n]*)",template_txt,re.M)
            out_txt=""
            for i in value_ls:
                if i[0].find('DIR')!=-1:
                    self.setting[i[0].strip()]=app_current_path+i[1].strip()
                    out_txt += i[0].strip()+"\t"+app_current_path+i[1].strip()+"\n"
                else:
                    self.setting[i[0].strip()]=i[1].strip()
                    out_txt += i[0].strip()+"\t"+i[1].strip()+"\n"
            with open(self.setting_file_path,'w+',encoding='utf-8') as f:
                f.write(out_txt)
        else:
            if self.detect_by_bom(self.setting_file_path) == 'utf-8':
                with open(self.setting_file_path, 'r', encoding='utf-8') as f:
                    tmp = f.read()
            else: #utf-16
                with open(self.setting_file_path,'rb') as f:
                    tmp = f.read()
                tmp = str(tmp, 'utf-16')
            value_ls=re.findall(r"^([^\t]+)\t([^\n]*)",tmp,re.M)
            for i in value_ls:
                self.setting[i[0].strip()]=i[1].strip()
    # Reference => https://doc.qt.io/qt-6/qfiledialog.html#static-public-members
    def select_dir(self):
        selected_folder = QFileDialog.getExistingDirectory(None,"Select Directory...")
        #print(selected_folder)
        return selected_folder

    def select_file(self):
        selected_file = QFileDialog.getOpenFileName(None,"Select File...")
        #print(selected_folder)
        return selected_file

    def show_dialog(self,dialog_title,dialog_body,iconType='Information',buttonType=QMessageBox.StandardButton.Ok):
        dialog = QMessageBox(parent=self, text=dialog_body)
        dialog.setWindowTitle(dialog_title)
        if iconType == 'Question':
            dialog.setIcon(QMessageBox.Icon.Question)
        elif iconType == 'Information':
            dialog.setIcon(QMessageBox.Icon.Information)
        elif iconType == 'Warning':
            dialog.setIcon(QMessageBox.Icon.Warning)
        elif iconType == 'Critical':
            dialog.setIcon(QMessageBox.Icon.Critical)
        # more StandardButton options --> https://coderslegacy.com/python/pyqt6-qmessagebox/
        dialog.setStandardButtons(buttonType)
        return dialog.exec()

    # 開啟新QWidget 以匯入ui處理版面問題
    def open_error_msg_win(self,error_title,error_msg): # 槽的連結寫在 ui 裡
        self.error_msg_win = QWidget(self)
        ui_path = "resource/error_msg_win.ui"
        ui_file = QFile(ui_path)
        if not ui_file.open(QIODevice.ReadOnly):
            print(f"Cannot open {ui_path}: {ui_file.errorString()}")
            sys.exit(-1)
        loader = QUiLoader()
        self.error_msg_win = loader.load(ui_file)
        ui_file.close()
        if not self.error_msg_win:
            print(loader.errorString())
            sys.exit(-1)
        self.error_msg_win.setWindowTitle(error_title)
        self.error_msg_win.setWindowFlags(Qt.WindowType.WindowCloseButtonHint)
        self.error_msg_win.error_msg_detail.setPlainText(error_msg)
        self.error_msg_win.error_msg_win_close_btn.clicked.connect(lambda: self.error_msg_win.close()) 
        self.error_msg_win.show()

    def show_about_dialog(self,title_txt,body_txt):
        text = body_txt
        QMessageBox.about(self,'關於 '+title_txt , text)