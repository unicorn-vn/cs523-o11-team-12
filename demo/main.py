import sys
from PyQt5.QtWidgets import QApplication
from classes.GUI import ExternalSortApp
from PyQt5.QtGui import QFont, QIcon

def main():
    app = QApplication(sys.argv)

    text_font = QFont(QFont('Arial', 14))
    button_font = QFont(QFont('Arial', 14, QFont.Bold))

    QApplication.setFont(text_font, "QLabel")
    QApplication.setFont(text_font, "QComboBox")
    QApplication.setFont(text_font, "QLineEdit")
    QApplication.setFont(button_font, "QPushButton")
    
    window = ExternalSortApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
