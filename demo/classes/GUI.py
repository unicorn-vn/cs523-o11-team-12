import os
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QPushButton, QFileDialog, QLabel, QProgressBar, QLineEdit, QComboBox
from PyQt5.QtGui import QFont, QIcon
from classes.SortThread import SortThread

class ExternalSortApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # ICONS
        self.icon_asc = QIcon('assets/icons/asc.png')
        self.icon_desc = QIcon('assets/icons/desc.png')


        # =================================================================================================
        # MAIN TITLE
        self.title = QLabel('Chọn tệp CSV để sắp xếp:')
        self.title.setFont(QFont('Arial', 22, QFont.Bold ))


        # =================================================================================================
        # SELECT FILE
        self.select_file_button = QPushButton('Chọn tệp')
        self.select_file_button.clicked.connect(self.selectFile)


        # =================================================================================================
        # SORT OPTIONS
        self.rv = QComboBox()
        self.rv.addItem(self.icon_asc, 'Tăng dần', "0")
        self.rv.addItem(self.icon_desc, 'Giảm dần', "1")
        
        self.chunk_txt = QLineEdit()
        self.chunk_txt.setFixedHeight(60)
        self.chunk_txt.setText('128')

        self.sort_options_layout = QHBoxLayout()
        self.sort_options_layout.addWidget(QLabel("Xếp theo thứ tự:"))
        self.sort_options_layout.addWidget(self.rv, 1)
        self.sort_options_layout.addWidget(QLabel('Chunk size:'))
        self.sort_options_layout.addWidget(self.chunk_txt, 1)
        
        self.sort_options_widget = QWidget(self) 
        self.sort_options_widget.setLayout(self.sort_options_layout)


        # =================================================================================================
        # BUTTON BOTTOM LAYOUT
        self.sort_button = QPushButton('Sắp xếp')
        self.sort_button.clicked.connect(self.startSorting)

        self.clear_temp = QPushButton('Xóa folder temp')
        self.clear_temp.clicked.connect(self.clearTemp)

        self.button_bottom_layout = QHBoxLayout()
        self.button_bottom_layout.addWidget(self.sort_button, 1)
        self.button_bottom_layout.addWidget(self.clear_temp, 1)

        self.button_bottom_widget = QWidget(self) 
        self.button_bottom_widget.setLayout(self.button_bottom_layout)


        # =================================================================================================
        # PROGRESS SECTION
        self.progress_label = QLabel('')

        self.progress_bar = QProgressBar()

        # =================================================================================================
        # SET LAYOUT
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.select_file_button)
        self.layout.addWidget(self.sort_options_widget)
        self.layout.addWidget(self.button_bottom_widget)
        self.layout.addWidget(self.progress_label)
        self.layout.addWidget(self.progress_bar)

        # =================================================================================================
        # WINDOW SETUP
        self.setWindowTitle('Grade Sort App')
        self.setMinimumSize(1200, 800)
        self.central_widget = QWidget(self)
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

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
            self.sorting_column = QComboBox()

            with open(file_path, "r") as f:
                for i, val in enumerate(f.readline().split(",")):
                    self.sorting_column.addItem(val, i)

            onlyFn = self.csv_file.split('/')[-1]
            self.title.setText(f'Tệp CSV đã chọn: {onlyFn}')
            self.layout.insertWidget(len(self.layout) - 5, QLabel('Sắp xếp theo cột:'))
            self.layout.insertWidget(len(self.layout) - 5, self.sorting_column)

    def startSorting(self):
        if hasattr(self, 'csv_file'):
            self.sort_button.setDisabled(True)
            self.progress_label.setText('Đang sắp xếp...')
            
            self.sort_thread = SortThread(self, self.csv_file, 'sorted_output.csv', int(self.chunk_txt.text()), bool(int(self.rv.currentData())), int(self.sorting_column.currentData()))
            self.sort_thread.done_signal.connect(self.sortDone)
            self.sort_thread.start()
        else:
            self.progress_label.setText('Vui lòng chọn tệp CSV trước.')

    def sortDone(self):
        self.progress_label.setText('Đã sắp xếp và lưu tại: sorted_output.csv')
        self.sort_button.setDisabled(False)
