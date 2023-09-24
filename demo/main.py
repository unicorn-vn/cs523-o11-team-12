import os
import sys
import tempfile
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QPushButton, QFileDialog, QLabel, QProgressBar, QCheckBox, QLineEdit, QComboBox, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QFont, QFontDatabase, QIcon

# Hàm để chia tệp thành các phần nhỏ
def split_file(input_file, chunk_size):
    chunks = []
    with open(input_file, 'r') as f:
        f.readline()
        chunk = f.readlines(chunk_size)
        while chunk:
            chunks.append(chunk)
            chunk = f.readlines(chunk_size)
    return chunks

# Hàm để ghi dữ liệu vào tệp tạm thời
def write_temp_file(sf, data, temp_dir):
    temp_file = tempfile.mktemp(dir=temp_dir)
    sf.progress_label.setText(f'Đang ghi file {temp_file}...')
    with open(temp_file, 'w') as f:
        f.writelines(data)
    return temp_file

# Hàm để sắp xếp và trộn các tệp tạm thời
def merge_sorted_files(sf, sorted_files, output_file, rv, k):
    sf.progress_label.setText('Đang trộn file...')
    with open(output_file, 'a') as out:
        # Mở các tệp tạm thời và đọc dữ liệu ban đầu
        temp_files = [open(file, 'r') for file in sorted_files]
        data = [file.readline() for file in temp_files]
        
        while data:
            # Tìm phần tử nhỏ nhất
            if (rv):
                min_val = max(data, key=lambda x: x.split(',')[k])
            else:
                min_val = min(data, key=lambda x: x.split(',')[k])
            min_idx = data.index(min_val)
            
            # Ghi phần tử nhỏ nhất vào tệp kết quả
            out.write(min_val)
            
            # Đọc tiếp dữ liệu từ tệp đó
            data[min_idx] = temp_files[min_idx].readline()
            
            # Kiểm tra xem tệp đó còn dữ liệu không
            if not data[min_idx]:
                temp_files[min_idx].close()
                del temp_files[min_idx]
                del data[min_idx]

# Hàm sắp xếp ngoại bộ
def external_sort(sf, input_file, output_file, chunk_size=1024, rv=False, col=0):
    temp_dir = './temp_files/'
    chunks = split_file(input_file, chunk_size)
    sorted_files = []

    # Sắp xếp từng phần nhỏ và lưu vào các tệp tạm thời
    for i, chunk in enumerate(chunks):
        chunk.sort(key=lambda x: x.split(',')[col], reverse=rv)
        temp_file = write_temp_file(sf, chunk, temp_dir)
        sorted_files.append(temp_file)

    with open(input_file, 'r') as inp:
        first_line = inp.readline()
        with open(output_file, 'w') as out:
            out.write(first_line)

    # Trộn các tệp tạm thời để có kết quả cuối cùng
    merge_sorted_files(sf, sorted_files, output_file, rv, col)

    # Xóa tệp tạm thời và thư mục tạm thời
    for temp_file in sorted_files:
        os.remove(temp_file)
    # os.rmdir(temp_dir)

from PyQt5.QtCore import Qt, QThread, pyqtSignal

class SortThread(QThread):
    done_signal = pyqtSignal()

    def __init__(self, sf, input_file, output_file, chunk, rv, col):
        super().__init__()
        self.input_file = input_file
        self.output_file = output_file
        self.rv = rv
        self.chunk = chunk
        self.col = col
        self.sf = sf

    def run(self):
        external_sort(self.sf, self.input_file, self.output_file, self.chunk, self.rv, self.col)
        self.done_signal.emit()

class ExternalSortApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Grade Sort App')
        self.setMinimumSize(1200, 800)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.label = QLabel('Chọn tệp CSV để sắp xếp:')
        self.label.setFont(QFont('Arial', 22, QFont.Bold ))
        self.layout.addWidget(self.label)

        self.select_button = QPushButton('Chọn tệp')
        self.select_button.setFont(QFont('Arial', 14, QFont.Bold ))
        self.select_button.clicked.connect(self.selectFile)
        self.layout.addWidget(self.select_button)

        # verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        # self.layout.addItem(verticalSpacer)

        self.param_layout = QHBoxLayout()

        self.label_rv = QLabel("Xếp theo thứ tự:")
        self.label_rv.setFont(QFont('Arial', 14))
        self.param_layout.addWidget(self.label_rv)
        self.rv = QComboBox()
        icon_asc = QIcon('asc.png')
        icon_desc = QIcon('desc.png')
        self.rv.addItem(icon_asc, 'Tăng dần', "1")
        self.rv.addItem(icon_desc, 'Giảm dần', "0")
        self.rv.setFont(QFont('Arial', 14))
        self.param_layout.addWidget(self.rv, 1)
        
        self.label_chunk = QLabel('Chunk size:')
        self.label_chunk.setFont(QFont('Arial', 14))
        self.param_layout.addWidget(self.label_chunk)
        self.chunk_txt = QLineEdit()
        self.chunk_txt.setFixedHeight(60)
        self.chunk_txt.setFont(QFont('Arial', 14))
        self.chunk_txt.setText('128')
        self.param_layout.addWidget(self.chunk_txt, 1)
        
        self.param_element = QWidget(self) 
        self.param_element.setLayout(self.param_layout)
        self.layout.addWidget(self.param_element)

        self.button_layout = QHBoxLayout()

        self.sort_button = QPushButton('Sắp xếp')
        self.sort_button.setFont(QFont('Arial', 14, QFont.Bold ))
        self.sort_button.clicked.connect(self.startSorting)
        self.button_layout.addWidget(self.sort_button, 1)

        self.clear_temp = QPushButton('Xóa folder temp')
        self.clear_temp.setFont(QFont('Arial', 14, QFont.Bold ))
        self.clear_temp.clicked.connect(self.clearTemp)
        self.button_layout.addWidget(self.clear_temp, 1)

        self.button_element = QWidget(self) 
        self.button_element.setLayout(self.button_layout)
        self.layout.addWidget(self.button_element)

        self.progress_label = QLabel('')
        self.progress_label.setFont(QFont('Arial', 14, QFont.Bold ))
        self.layout.addWidget(self.progress_label)

        self.progress_bar = QProgressBar()
        self.layout.addWidget(self.progress_bar)

        self.central_widget.setLayout(self.layout)

    def clearTemp(self):
        os.system('rm -rf temp_files')
        os.system('mkdir temp_files')
        self.progress_label.setText('Đã xóa folder temp')

    def selectFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(self, 'Chọn tệp CSV', '', 'CSV Files (*.csv);;All Files (*)', options=options)
        

        if file_path:
            self.csv_file = file_path
            onlyFn = self.csv_file.split('/')[-1]
            self.label.setText(f'Tệp CSV đã chọn: {onlyFn}')
            self.label_col = QLabel('Sắp xếp theo cột:')
            self.label_col.setFont(QFont('Arial', 14))
            self.layout.insertWidget(len(self.layout) - 5, self.label_col)
            self.col_txt = QComboBox()
            with open(file_path) as f:
                first_line = f.readline()
            for i, val in enumerate(first_line.split(",")):
                self.col_txt.addItem(val, i)
            self.col_txt.setFont(QFont('Arial', 14))
            self.layout.insertWidget(len(self.layout) - 5, self.col_txt)

    def startSorting(self):
        if hasattr(self, 'csv_file'):
            self.sort_button.setDisabled(True)
            self.progress_label.setText('Đang sắp xếp...')
            self.sort_thread = SortThread(self, self.csv_file, 'sorted_output.csv', int(self.chunk_txt.text()), bool(int(self.rv.currentData())), int(self.col_txt.currentData()))
            self.sort_thread.done_signal.connect(self.sortDone)
            self.sort_thread.start()
        else:
            self.progress_label.setText('Vui lòng chọn tệp CSV trước.')

    def sortDone(self):
        self.progress_label.setText('Đã sắp xếp và lưu tại: sorted_output.csv')
        self.sort_button.setDisabled(False)

def main():
    app = QApplication(sys.argv)
    window = ExternalSortApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
