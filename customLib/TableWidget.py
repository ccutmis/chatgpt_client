from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from PySide6.QtGui import QKeySequence

class TableWidget(QTableWidget):
    def __init__(self, rows, columns, parent=None):
        super().__init__(rows, columns)
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_V and (event.modifiers() & Qt.KeyboardModifier.ControlModifier):
            selection = self.selectedIndexes()

            if selection:
                row_anchor = selection[0].row()
                column_anchor = selection[0].column()
                clipboard = QApplication.clipboard()
                rows = clipboard.text().split('\n')
                for indx_row, row in enumerate(rows):
                    values = row.split('\t')
                    for indx_col, value in enumerate(values):
                        item = QTableWidgetItem(value)
                        self.setItem(row_anchor + indx_row, column_anchor + indx_col, item)
            super().keyPressEvent(event)
        elif event.key() in [ Qt.Key.Key_Left ,Qt.Key.Key_Right, Qt.Key.Key_Up, Qt.Key.Key_Down]:
            # press arrow key to move cursor on cells
            row_max = self.rowCount()
            col_max = self.columnCount()
            selection = self.selectedIndexes()
            row_anchor = selection[0].row()
            column_anchor = selection[0].column()
            if event.key() == Qt.Key.Key_Left: 
                if column_anchor > 0:
                    column_anchor -= 1
                else:
                    column_anchor = 0
            elif event.key() == Qt.Key.Key_Right: 
                if column_anchor < col_max-1:
                    column_anchor += 1
                else:
                    col_max = col_max-1
            elif event.key() == Qt.Key.Key_Up:
                if row_anchor > 0:
                    row_anchor -= 1
                else:
                    row_anchor = 0
            else:
                if row_anchor < row_max-1 :
                    row_anchor += 1
                else:
                    row_anchor = row_max-1
            # move to right cell
            self.setCurrentCell(row_anchor,column_anchor)
        elif event.key() == Qt.Key.Key_Delete :
            selection = self.selectedIndexes()
            #print(selection[0].row(),selection[0].column())
            if selection:
                #print(selection)
                for i in selection:
                    item = QTableWidgetItem(str('')) 
                    self.setItem(i.row(),i.column(),item)




    def clearTableData(self):
        try:
            for row in range(self.rowCount()):
                tmp_col_txt=''
                for col in range(self.columnCount()):
                    self.setItem(row,col, QTableWidgetItem(''))
            return True
        except:
            return False

    def readTableData(self):
        tmp_all_txt=''
        try:
            for row in range(self.rowCount()):
                tmp_col_txt=''
                for col in range(self.columnCount()):
                    tmp_col_txt+=(self.item(row,col).text())+'\t'
                tmp_col_txt+='\n'
                #print(tmp_col_txt)
                if tmp_col_txt.replace('\t','').replace('\n','').strip()!='':
                    tmp_all_txt+=tmp_col_txt
        except:
            print("READ TABLE DATA FAIL!")
        print(tmp_all_txt)
        if tmp_all_txt!="":
            return tmp_all_txt
        else:
            return None