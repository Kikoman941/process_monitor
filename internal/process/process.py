from .psutill_process import PsutilProcess
from subprocess import Popen, PIPE
from psutil import NoSuchProcess


class Process(PsutilProcess):
    def __init__(self):
        PsutilProcess.__init__(self)
        self._process = None
        self._return_code = None

    def start_process(self, cmd: str) -> int:
        self._process = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
        self.set_process_info(self._process.pid)
        try:
            self._return_code = self._process.wait()
        except KeyboardInterrupt:
            self._process_logger.write_console_message('Exit')
            return self._return_code

        if self._return_code != 0:
            err = self._process.stderr.read().decode('utf-8')
            if err != '':
                self._process_logger.write_console_inner_process_message(err)
        return self._return_code

    def stop(self):
        try:
            for child in self.process_info.children(recursive=True):
                child.kill()
            self._process.kill()
        except NoSuchProcess:
            self._process_logger.write_console_message('Exit')
