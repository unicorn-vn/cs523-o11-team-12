import sys
import os
import tempfile
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QFileDialog, QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt
from time import sleep

# Hàm để chia tệp thành các phần nhỏ
def split_file(input_file, chunk_size):
    c1 = []
    c2 = []
    cr = 1
    t = []
    runs = 0
    with open(input_file, 'r') as f:
        ln = f.readline()
        while ln:
            if (ln != '\n'):
                if (len(t) < chunk_size):
                    t.append(int(ln))
                else:
                    if(cr == 1):
                        c1.append(t)
                        cr = 2
                        t = [int(ln)]
                        runs += 1
                    else:
                        c2.append(t)
                        cr = 1
                        t = [int(ln)]
                        runs += 1
            ln = f.readline()
        if (cr == 1 and len(t)>0):
            c1.append(t)
            runs += 1
        elif len(t)>0:
            c2.append(t)
            runs += 1
    # print(c1);
    # print(c2);
    return [c1, c2]

def sort_chunk(run, rv=False):
    run.sort(reverse=rv)
    return run

def merge(list1, list2):
    result = []
    i = j = 0
    while i < len(list1) and j < len(list2):
        if list1[i] < list2[j]:
            result.append(list1[i])
            i += 1
        else:
            result.append(list2[j])
            j += 1
    result += list1[i:]
    result += list2[j:]
    return result

class ExternalSortApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.tp=[]

    def initUI(self):
        self.setGeometry(100, 100, 400, 300)
        self.setWindowTitle('External Sort Demo')

        self.text_edit = QTextEdit()
        self.text_edit_2 = QTextEdit()

        self.temp1 = QHBoxLayout()
        self.temp1.addWidget(QLabel("Chunk 1"), 1)
        self.temp1.addWidget(self.text_edit, 1)
        self.temp1.addWidget(self.text_edit_2, 1)

        self.temp1_wid = QWidget(self) 
        self.temp1_wid.setLayout(self.temp1)

        self.text_edit_3 = QTextEdit()
        self.text_edit_4 = QTextEdit()
        self.text_edit_5 = QTextEdit()

        self.temp2 = QHBoxLayout()
        self.temp2.addWidget(QLabel("Chunk 2"), 1)
        self.temp2.addWidget(self.text_edit_3, 1)
        self.temp2.addWidget(self.text_edit_4, 1)

        self.temp2_wid = QWidget(self) 
        self.temp2_wid.setLayout(self.temp2)

        self.select_button = QPushButton('Load file')
        self.select_button.setGeometry(150, 220, 100, 30)
        self.select_button.clicked.connect(self.choose_files)

        self.sort_button = QPushButton('Sort')
        self.sort_button.setGeometry(150, 220, 100, 30)
        self.sort_button.clicked.connect(self.sort)

        self.merge_button = QPushButton('Merge')
        self.merge_button.setGeometry(150, 220, 100, 30)
        self.merge_button.clicked.connect(self.merge)

        self.export_button = QPushButton('Export')
        self.export_button.setGeometry(150, 220, 100, 30)
        self.export_button.clicked.connect(self.export)

        self.layout = QVBoxLayout()
        self.layout.addWidget(QLabel("External Sort Demo"), 1)
        self.layout.addWidget(self.temp1_wid)
        self.layout.addWidget(self.temp2_wid)
        self.layout.addWidget(QLabel("Result"), 1)
        self.layout.addWidget(self.text_edit_5)
        self.layout.addWidget(QLabel("Actions"), 1)
        self.layout.addWidget(self.select_button)
        self.layout.addWidget(self.sort_button)
        self.layout.addWidget(self.merge_button)
        self.layout.addWidget(self.export_button)
        self.central_widget = QWidget(self)
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        

    def choose_files(self):
        options = QFileDialog.Options()
        input_file, _ = QFileDialog.getOpenFileName(self, "Chọn tệp đầu vào", "", "Text Files (*.txt);;All Files (*)", options=options)
        # output_file, _ = QFileDialog.getSaveFileName(self, "Chọn tệp xuất", "", "Text Files (*.txt);;All Files (*)", options=options)

        if input_file:
            temp_file1 = "temp1.txt"
            temp_file2 = "temp2.txt"
            self.tt = split_file("text.txt", 2)
            self.text_edit.setText(str(self.tt[0]))
            self.text_edit_3.setText(str(self.tt[1]))
            # external_sort(input_file, output_file, temp_file1, temp_file2)
            # self.text_edit.setPlainText("Sắp xếp thành công và lưu vào tệp: " + output_file)
            # Xóa các tệp tạm
            # os.remove(temp_file1)
            # os.remove(temp_file2)
    
    def sort(self):
        for i in range(0, max(len(self.tt[0]), len(self.tt[1]))):
            if (i < len(self.tt[0])):
                self.tt[0][i] = sort_chunk(self.tt[0][i])
                self.text_edit.setText(str(self.tt[0]))
            if (i < len(self.tt[1])):
                self.tt[1][i] = sort_chunk(self.tt[1][i])
                self.text_edit_3.setText(str(self.tt[1]))

    def merge(self):
        while (len(self.tt[0]) > 1):
            for i in range(0, len(self.tt[0]), 2):
                if (i+1 >= len(self.tt[0])):
                    self.tp.append(self.tt[0][i])
                else:
                    self.tp.append(merge(self.tt[0][i], self.tt[0][i+1]))
            self.tt[0] = self.tp
            self.tp = []
            print(self.tt)
        while (len(self.tt[1]) > 1):
            for i in range(0, len(self.tt[1]), 2):
                if (i+1 >= len(self.tt[1])):
                    self.tp.append(self.tt[1][i])
                else:
                    self.tp.append(merge(self.tt[1][i], self.tt[1][i+1]))
            self.tt[1] = self.tp
            self.tp = []
            print(self.tt)
        self.text_edit_2.setText(str(self.tt[0][0]))
        self.text_edit_4.setText(str(self.tt[1][0]))
    
    def export(self):
        self.tt = merge(self.tt[0][0], self.tt[1][0])
        self.text_edit_5.setText(str(self.tt))

        

def main():
    app = QApplication(sys.argv)
    ex = ExternalSortApp()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
