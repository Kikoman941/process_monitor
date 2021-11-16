import psutil
from ..logger.logger import Logger
from time import time
from ..config.config import format_date
from platform import system


class PsutilProcess(object):
    CONSOLE_TEMPLATE = {
        'Linux': 'Started: {start} | CPU_PERCENT: {cpu_perc}% | MEM_RS: {mem_rs} MB | '
                 'MEM_VIRTUAL: {mem_virt} MB | OPEN_FILES: {open_fs}',
        'Windows': 'Started: {start} | CPU_PERCENT: {cpu_perc}% | WORK_SET: {work_set} MB | '
                   'PRIVATE_B: {private_b} MB | OPEN_FILES: {open_fs}',
    }

    REPORT_TEMPLATE = {
        'Linux': [['TIME_UNIX', 'CPU_PERCENT', 'MEM_RS', 'MEM_VIRTUAL', 'OPEN_FILES']],
        'Windows': [['TIME_UNIX', 'CPU_PERCENT', 'WORK_SET', 'PRIVATE_B', 'OPEN_FILES']],
    }

    def __init__(self):
        self.process_info = None
        self._process_logger = Logger()
        self._os = system()
        self._cpu_count = psutil.cpu_count()

    def set_process_info(self, pid):
        self.process_info = psutil.Process(pid)

    def create_report_file(self, name: str) -> str:
        return self._process_logger.create_report_file(
            name,
            self.REPORT_TEMPLATE[self._os]
        )

    def console_monitoring(self):
        if self.process_info is not None:
            data = self._fetch_data()
            self._process_logger.replace_last_line(
                self.CONSOLE_TEMPLATE[self._os].format(
                    start=format_date(
                        self.process_info.create_time(),
                        self._process_logger.CONSOLE_DATE_FORMAT,
                    ),
                    cpu_perc=data['cpu_percent'],
                    mem_rs=format(data['resident_set'] / 1000000, '.2f'),
                    mem_virt=format(data['virtual_memory'] / 1000000, '.2f'),
                    work_set=format(data['work_set'] / 1000000, '.2f'),
                    private_b=format(data['private_b'] / 1000000, '.2f'),
                    open_fs=data['open_files'],
                )
            )

    def report_monitoring(self):
        if self.process_info is not None:
            data_for_report = []
            data = self._fetch_data()
            time_now = int(time())

            if self._os == 'Linux':
                data_for_report.append(
                    [
                        time_now,
                        data['cpu_percent'],
                        data['resident_set'],
                        data['virtual_memory'],
                        data['open_files'],
                    ]
                )
            elif self._os == 'Windows':
                data_for_report.append(
                    [
                        time_now,
                        data['cpu_percent'],
                        data['work_set'],
                        data['private_b'],
                        data['open_files'],
                    ]
                )

            self._process_logger.write_to_csv_file(data_for_report)

    def _fetch_data(self) -> dict:
        cpu_percent = 0
        resident_set = 0
        virtual_memory = 0
        work_set = 0
        private_b = 0
        open_files = 0

        try:
            child_processes = self.process_info.children(recursive=True)
            for process in child_processes:
                memory_info = process.memory_info()
                open_files += len(process.open_files())
                if self._os == 'Linux':
                    cpu_percent += process.cpu_percent(interval=0.5)
                    resident_set += memory_info.rss
                    virtual_memory += memory_info.vms
                elif self._os == 'Windows':
                    cpu_percent += process.cpu_percent(interval=0.5) / self._cpu_count
                    work_set += memory_info.wset
                    private_b += memory_info.private
        except psutil.NoSuchProcess as err:
            raise SystemExit(err)

        return {
            'cpu_percent': cpu_percent,
            'resident_set': resident_set,
            'virtual_memory': virtual_memory,
            'open_files': open_files,
            'work_set': work_set,
            'private_b': private_b,
        }
