import sys
from datetime import datetime


def get_settings() -> dict:
    settings: dict = {}
    try:
        with open('settings.env', 'r') as file:
            for line in file:
                key, value = line.split('=')
                settings[key] = value
    except FileNotFoundError as err:
        raise SystemExit(err)
    settings['INTERVAL_IN_SECONDS'] = time_to_seconds(settings['INTERVAL'])
    return settings


def time_to_seconds(time: str) -> int:
    str_value = ''
    measure = ''
    if len(time) == 0:
        incorrect_interval()
    for el in time:
        if not el.isdigit():
            if time.find(el) == 0:
                incorrect_interval()
            measure += el
        else:
            str_value += el

    if len(measure) != 1:
        incorrect_interval()

    if measure == 's':
        return int(str_value)
    elif measure == 'm':
        return int(str_value) * 60
    elif measure == 'h':
        return int(str_value) * 3600
    elif measure == 'd':
        return int(str_value) * 86400
    else:
        incorrect_interval()


def get_process_name(file: str) -> str:
    return file.split('/')[-1].rstrip()


def format_date(date: float, fmt: str) -> str:
    return datetime.fromtimestamp(date).strftime(fmt)


def incorrect_interval():
    sys.exit('[ERROR] Set the correct integer interval in format s, m, h, d\nExample: 3s or 4h')
