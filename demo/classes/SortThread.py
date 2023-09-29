from utils.external_sorting import external_sort
from PyQt5.QtCore import QThread, pyqtSignal

class SortThread(QThread):
    done_signal = pyqtSignal()

    def __init__(self, sf, input_file, output_file, chunk, rv, col, output_buffer):
        super().__init__()
        self.input_file = input_file
        self.output_file = output_file
        self.rv = rv
        self.chunk = chunk
        self.col = col
        self.sf = sf
        self.output_buffer = output_buffer

    def run(self):
        external_sort(self.sf, self.input_file, self.output_file, self.chunk, self.rv, self.col, self.output_buffer)
        self.done_signal.emit()
