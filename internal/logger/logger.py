import csv
from time import strftime


class Logger(object):
    CONSOLE_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
    FILENAME_DATE_FORMAT = '%Y-%m-%d_%H-%M-%S'
    FILE_PATH_TEMPLATE = './reports/{name}_{date}.csv'
    report_file_path = ''

    def create_report_file(self, name: str, headers: str):
        self.report_file_path = self.FILE_PATH_TEMPLATE.format(
            name=name,
            date=strftime(self.FILENAME_DATE_FORMAT),
        )
        with open(self.report_file_path, 'w') as file:
            writer = csv.writer(file)
            writer.writerows(headers)
        return self.report_file_path

    def write_to_csv_file(self, data: list):
        with open(self.report_file_path, 'a') as file:
            writer = csv.writer(file)
            writer.writerows(data)

    @staticmethod
    def write_console_message(message: str):
        print(message)

    @staticmethod
    def write_console_inner_process_message(message: str):
        print(
            '\nINNER PROCESS MESSAGE\n'
            '============================================\n'
            '{0}\n'
            '============================================\n'.format(message)
        )

    @staticmethod
    def replace_last_line(message: str):
        print(message, end='\r')
