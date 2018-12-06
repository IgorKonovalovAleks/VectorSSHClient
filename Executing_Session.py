import time


class Session:
    __slots__ = ["_stdin", "_stdout", "_stderr"]

    def __init__(self, stdin, stdout, stderr):
        self._stdin = stdin
        self._stdout = stdout
        self._stderr = stderr

    def check(self):
        return bool(self._stdout.channel.eof_received)

    def __call__(self, command):
        print("session called\ncommand: " + command)
        if command:
            print("writing: " + command)
            self._stdin.write(command + "\n")

        print(len(self._stdout.channel.in_buffer))
        c = 0
        while len(self._stdout.channel.in_buffer) == 0 and c < 10:
            c += 1
            time.sleep(0.1)
            continue
        print("wait: " + c)

        n = len(self._stdout.channel.in_buffer)
        print("reply length: " + str(n))
        repl = self._stdout.read(n).decode("utf-8")
        print("server reply: " + repl)
        return repl

    def read_err(self):
        print("stderr read")
        return self._stderr.read().decode("utf-8")

    def read(self):
        print("stdout read")
        if self.check():
            return self._stdout.read().decode("utf-8")
        else:
            return ""

    def close(self):
        self._stdin.close()
        self._stdout.close()
