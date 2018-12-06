from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt, pyqtSignal


class MainWindow(QMainWindow):

    keyPressSignal = pyqtSignal(int)

    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('user_interface.ui', self)
        self.setWindowTitle("Vector++ IDE (nioh)")
        self.show()

    # self.seyDisabled(True) makes child window disable
    def disable(self):
        self.connectButton.setDisabled(True)
        self.saveButton.setDisabled(True)
        self.executeButton.setDisabled(True)
        self.compileButton.setDisabled(True)
        self.textEdit.setDisabled(True)
        self.textBrowser.setDisabled(True)

    def enable(self):
        self.connectButton.setDisabled(False)
        self.saveButton.setDisabled(False)
        self.executeButton.setDisabled(False)
        self.compileButton.setDisabled(False)
        self.textEdit.setDisabled(False)
        self.textBrowser.setDisabled(False)

    def keyPressEvent(self, event):
        super(MainWindow, self).keyPressEvent(event)
        self.keyPressSignal.emit(event.key)
