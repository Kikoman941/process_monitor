from internal.config.config import get_settings, get_process_name
from internal.logger.logger import Logger
from internal.worker.worker import Worker, IntervalWorker
from internal.process.process import Process
import signal


class App(object):
    CONSOLE_MONITORING_INTERVAL = 2

    def __init__(self):
        self._file = ''
        self._interval = ''
        self._worker = None
        self._service_console = None
        self._service_report = None
        self._app_logger = Logger()
        self._process = Process()

        self._set_settings()

    def _set_settings(self):
        settings = get_settings()

        self._file = settings['FILE']
        self._interval = settings['INTERVAL_IN_SECONDS']
        self._worker = Worker(
            lambda: self._process.start_process(self._file),
        )
        self._service_console = IntervalWorker(self.CONSOLE_MONITORING_INTERVAL, self._process.console_monitoring)
        self._service_report = IntervalWorker(self._interval, self._process.report_monitoring)
        self._worker.connect(self._service_console, self._service_report)

        report = self._process.create_report_file(get_process_name(self._file))
        self._app_logger.write_console_message(
            'Work with a file:\n--- {0}'
            'With an reporting interval of:\n--- {1}\n'
            'Write report in file:\n --- {2}\n'
            '============================================'.format(
                self._file,
                settings['INTERVAL'],
                report,
            )
        )

        signal.signal(signal.SIGINT, self._gracefully_exit)

    def _gracefully_exit(self, *args):
        self._process.stop()
        self._worker.stop()

    def run(self):
        self._worker.start()
