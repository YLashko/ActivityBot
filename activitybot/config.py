import datetime

TOKEN = '5916985356:AAGZfgdD_55JIZhPxCkFv4XkgKUIdCQZa3I'
ADMINS = ['532842840']
MESSAGE_TIME = '20:36'
RECORD_TIME_RANGE = [datetime.time(hour=20, minute=0, second=0), datetime.time(hour=23, minute=59, second=59)]
HELP_MESSAGE = 'Привет! Запись активности - /activity, доступна с {} до {}'.format(RECORD_TIME_RANGE[0].strftime("%H:%M:%S"), RECORD_TIME_RANGE[1].strftime("%H:%M:%S"))
