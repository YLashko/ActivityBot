import datetime
import os

DB_PATH = 'activitybot/db/database.db' if os.getenv('DB_PATH') is None else os.getenv('DB_PATH')
TOKEN = os.getenv('TOKEN')
ADMINS = [os.getenv("ADMINS")]
MESSAGE_TIME = '20:00'
RECORD_TIME_RANGE = [datetime.time(hour=20, minute=0, second=0), datetime.time(hour=23, minute=59, second=59)]
HELP_MESSAGE = 'Привет! Запись активности - /activity, доступна с {} до {}'.format(RECORD_TIME_RANGE[0].strftime("%H:%M:%S"), RECORD_TIME_RANGE[1].strftime("%H:%M:%S"))
