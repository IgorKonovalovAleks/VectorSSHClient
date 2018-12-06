import paramiko
import Executing_Session


class SSH_Client:
    __slots__ = ["_clientSSH", "_host", "_user", "_password", "_port", "_home"]

    def __init__(self, host, login, password, port, home, log_file):
        paramiko.util.log_to_file(log_file)
        self._clientSSH = paramiko.SSHClient()
        self._clientSSH.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self._host = host
        self._user = login
        self._password = password
        self._port = port
        self._home = home

    def _execute_command(self, command):
        print("executed: " + command)
        self._clientSSH.connect(self._host, self._port, self._user, self._password)
        stdin, stdout, stderr = self._clientSSH.exec_command(command)
        self._clientSSH.close()
        return stdout.read()

    def ls_home(self):
        repl = self._execute_command("ls " + self._home + "\n").decode('utf-8')
        print("ls " + self._home + ": " + repl)
        buffer = ""
        ret = []
        for ch in repl:
            if ch == '\n':
                ret.append(buffer)
                buffer = ""
            else:
                buffer += ch
        print("home directory: " + str(ret))
        return ret

    def compile(self, name):
        print("compiled")
        repl = self._execute_command("g++ -o {} {}.cpp".format(self._home + "/" + name, self._home + "/" + name)).decode('utf-8')
        return repl

    def start_session(self, name):
        print("session started")
        self._clientSSH.connect(self._host, self._port, self._user, self._password)
        stdin, stdout, stderr = self._clientSSH.exec_command("/home/{}/{}/{}".format(self._user, self._home, name), get_pty=True)
        return Executing_Session.Session(stdin, stdout, stderr)

    def stop_session(self):
        print("session stoped")
        self._clientSSH.close()

    def transfer_get(self, name, path):
        try:
            transport = paramiko.Transport((self._host, self._port))
            transport.connect(self._user, self._password)
            _client_sftp = paramiko.SFTPClient.from_transport(transport)
            _client_sftp.get(self._home + "/" + name, path)
        except Exception:
            f = open(path, "w")
            f.flush()
            f.close()
        finally:
            transport.close()

    def transfer_put(self, path, name):
        if name not in self.ls_home():
            self._execute_command("touch {}".format(self._home + "/" + name))
        try:
            transport = paramiko.Transport((self._host, self._port))
            transport.connect(username=self._user, password=self._password)
            _client_sftp = paramiko.SFTPClient.from_transport(transport)
            print("/home/{}/{}/{}".format(self._user, self._home, name))
            _client_sftp.put(path, "/home/{}/{}/{}".format(self._user, self._home, name))
        finally:
            transport.close()
        self._execute_command("chmod 777 {}".format(self._home + "/" + name))
        print("transfered")
