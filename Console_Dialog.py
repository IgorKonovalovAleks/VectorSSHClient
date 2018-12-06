from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, pyqtSignal


class ConsoleDialog(QWidget):

    keyPressSignal = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent, Qt.Window)
        uic.loadUi('console_dialog.ui', self)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setParent(parent)
        self.textEdit.keyPressEvent = self._get_console_handler(self.textEdit.keyPressEvent)

    def start(self):
        print("Console init: " + self.textEdit.toPlainText())
        self.setWindowTitle("Interactive Mode")
        self.show()

    def _get_console_handler(self, old_handler):
        def key_press_handler(event):
            old_handler(event)
            print("key press event")
            if event.key() == Qt.Key_Return:
                print("enter key detected")
                self.text = self.textEdit.toPlainText()
                print(self.text)
                self.keyPressSignal.emit()
        return key_press_handler

    def keyPressEvent(self, QKeyEvent):
        super(ConsoleDialog, self).keyPressEvent(QKeyEvent)
        print("key press event")
        if QKeyEvent.key() == Qt.Key_Return:
            print("Enter Key Detected")
            self.keyPressSignal.emit()
