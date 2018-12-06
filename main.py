import User_Interface
import VectorClient
import os
import sys
import Console_Dialog


class Main:

    def __init__(self, host, login, password, port, home_remote, log_file, filename):
        self.Window = User_Interface.MainWindow()
        self.Client = VectorClient.SSH_Client(host, login, password, port, home_remote, log_file)
        self.Console = Console_Dialog.ConsoleDialog(self.Window)
        self.Window.textBrowser.setText("start")
        self._tmp = "cache/tmp.cpp"
        self._name = filename
        self._saved = True
        self._compiled = True
        self._session_able = False
        self.Window.textBrowser.setText(os.path.dirname(sys.argv[0]) + "/" + self._tmp)
        self.Window.connectButton.clicked.connect(self._on_connect_button_clicked)
        self.Window.saveButton.clicked.connect(self._on_save_button_pressed)
        self.Window.compileButton.clicked.connect(self._on_compile_button_pressed)
        self.Window.executeButton.clicked.connect(self._on_execute_button_pressed)
        self.Window.textEdit.textChanged.connect(self._on_text_changed)
        self.Console.pushButton.clicked.connect(self._return_from_interactive)
        self.Console.keyPressSignal.connect(self._session_handle)

    def _on_text_changed(self):
        self._compiled = False
        self._saved = False

    def _update_session(self, com=""):
        print("try to update session")
        if self.session.check():
            self.Console.textEdit.setText(self.Console.textEdit.toPlainText() + "\n" + self.session.read() + "\n***Session closed***")
            print("session already closed: " + self.session.read())
            return False
        if self._session_able:
            print("updating session")
            try:
                repl = self.session(com)
            except OSError:
                self.Console.textEdit.setText(self.Console.textEdit.toPlainText() + "\n***Session closed due to OSError***")
                return False
            print("updated: " + repl)
            self.Console.textEdit.setText(self.Console.textEdit.toPlainText() + "\n" + repl + "\n" + ">>> ")
            return True
        else:
            return False

    def _on_execute_button_pressed(self):
        if self._compiled:
            self.session = self.Client.start_session(self._name)
            self._session_able = True
            self.Window.disable()
            self.Console.start()
            self._update_session()

    def _session_handle(self):
        print("got keyPressSignal")
        text = self.Console.textEdit.toPlainText()
        text = text.split("\n")[-1]
        print("text" + text)
        command = text[text.find(">>> ") + 4:]
        print(command)
        if self._update_session(command):
            print("session updated")
        else:
            print("session stopping...")
            self._on_session_executed()
        if self.session.check():
            print("session finished")
            self._update_session()
            self._on_session_executed()

    def _on_session_executed(self):
        self.Window.textBrowser.setText(self.Console.textEdit.toPlainText())
        self.Client.stop_session()
        self._session_able = False
        self.session.close()

    def _return_from_interactive(self):
        if not self._session_able:
            self.Console.close()
            self.Window.enable()

    def _on_save_button_pressed(self):
        print("saved")
        self._saved = True
        self._built_file(self._tmp)

    def _on_compile_button_pressed(self):
        print("compiling...")
        if not self._saved:
            self.Window.textBrowser.setText("Cannot compile before saving")
            return
        self._compiled = True
        self.Client.transfer_put(os.path.dirname(sys.argv[0]) + "/" + self._tmp, self._name + ".cpp")
        repl = self.Client.compile(self._name)
        if repl:
            self.Window.textBrowser.setText("Compilation failed:\n" + repl)
        else:
            self.Window.textBrowser.setText("Compilation succeeded:\n" + repl)

    def _built_file(self, name):
        text = self.Window.textEdit.toPlainText()
        with open(name, "w") as file:
            file.write(text)
            file.flush()

    def _on_connect_button_clicked(self):
        repl = self.Client.ls_home()
        self.Window.textBrowser.setText("connected: " + str(repl))
