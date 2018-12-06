import main
from PyQt5.Qt import QApplication
import sys
from config import *

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = main.Main(HOST, USERNAME, PASSWORD, PORT, REMOTE_HOME_DIRECTORY, PARAMIKO_LOG, EXECUTABLE_FILE_NAME)
    sys.exit(app.exec_())
