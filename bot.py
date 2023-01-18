from telebot.async_telebot import AsyncTeleBot
from telebot.handler_backends import State, StatesGroup
from telebot.asyncio_storage import StateMemoryStorage
from telebot import asyncio_filters
from collections import defaultdict
from activities import Activity
import io
import csv
import asyncio
import datetime
from config import TOKEN, HELP_MESSAGE, MESSAGE_TIME, RECORD_TIME_RANGE
from database import Database
from filters import is_number
from queries import *

bot = AsyncTeleBot(token=TOKEN, state_storage=StateMemoryStorage())

class ABotStates(StatesGroup):
    recording_activity = 4
    deleting_user = 3

@bot.message_handler(commands=['start', 'help'])
async def help(message):
    user = message.from_user
    if not database.user_exists(user.id):
        database.execute_sql(create_user(user.id, user.username))
    await send_message_to_user(user.id, HELP_MESSAGE)

@bot.message_handler(commands=['reset'])
async def reset_tables_message(message):
    user = message.from_user
    if not database.is_admin(user.id):
        return
    database.execute_list(reset_tables())
    await send_message_to_user(user.id, 'База данных очищена')

@bot.message_handler(commands=['deleteuser'])
async def delete_user(message):
    user = message.from_user
    if not database.is_admin(user.id):
        return
    await bot.set_state(user.id, ABotStates.deleting_user)
    await send_message_to_user(user.id, "Выберите пользователя. Отмена - /cancel")

@bot.message_handler(commands=['activity'])
async def activity_message(message):
    user = message.from_user

    try:
        user_can_record_activity(user.id)
    except PermissionError as e:
        await send_message_to_user(user.id, e)
        return

    await send_message_to_user(user.id, "Отменить запись активности - /cancel")

    activity = Activity()
    await send_message_to_user(user.id, activity.next_title())
    users_activities[user.id] = activity
    await bot.set_state(user.id, ABotStates.recording_activity, message.chat.id)

@bot.message_handler(commands=['cancel'], state=ABotStates.recording_activity)
async def cancel_activity_recording_message(message):
    user = message.from_user
    await cancel_activity_recording(user.id)
    await send_message_to_user(user.id, "Запись отменена")

@bot.message_handler(commands=['cancel'], state=ABotStates.deleting_user)
async def cancel_deleting_user_message(message):
    user = message.from_user
    if not database.is_admin(user.id):
        print(f"Non-admin user @{user.username} somehow did activate the deleting_user state")
        return
    await bot.delete_state(user.id)
    await send_message_to_user(user.id, "Удаление отменено")

@bot.message_handler(state=ABotStates.deleting_user)
async def delete_user_message(message):
    user = message.from_user
    try:
        deleting_user_name = message.text if message.text[0] != '@' else message.text[1:]
        database.execute_sql(delete_user_by_telegram_name(deleting_user_name))
        await send_message_to_user(user.id, f"Пользователь @{deleting_user_name} удален, если такой существовал")
        await bot.delete_state(user.id)
    except Exception as e:
        await send_message_to_user(user.id, f"Что-то пошло не так. {e}")

@bot.message_handler(state=ABotStates.recording_activity)
async def recording_activity_iteration(message):

    if not is_number(message.text):
        return

    user = message.from_user
    activity: Activity = users_activities[user.id]

    try:
        activity.write_mark(message.text)
    except ValueError as e:
        await send_message_to_user(user.id, e)
        return
    
    if (next_title := activity.next_title()) is None:

        await send_message_to_user(user.id, 'Ваши оценки записаны!')
        save_activity(user.id, activity)
        await cancel_activity_recording(user.id)
        await compile_activities(user.id)
        return

    await send_message_to_user(user.id, next_title)

@bot.message_handler(commands=['users'])
async def get_users_message(message):
    user = message.from_user

    if not database.is_admin(user.id):
        return
    
    users = database.execute_sql(get_all_users())
    await send_message_to_user(user.id, ", ".join(["@" + user[1] for user in users]))
    
async def cancel_activity_recording(user_id):
    users_activities[user_id] = None
    await bot.delete_state(user_id, user_id)

def save_activity(user_id: int, activity: Activity):
    database.execute_sql(create_activity_record(str(user_id), *activity.get_marks()))

async def send_messages_to_users():
    current_datetime = datetime.datetime.now()
    if not in_range(RECORD_TIME_RANGE[0], RECORD_TIME_RANGE[1], current_datetime.time()):
        return

    database.execute_sql(set_users_default_date())
    users = database.execute_sql(get_all_users())
    
    for user in users:
        if datetime.datetime.strptime(user[2], "%Y-%M-%d").date() < datetime.datetime.now().date():
            await send_message_to_user(user[0], "Как прошел твой день? /activity")
    database.execute_sql(update_users_date_to_today())

async def send_message_to_user(user_telegram_id, message):
    try:
        await bot.send_message(user_telegram_id, message)
    except Exception as e:
        print(f"Failed to send message to user {user_telegram_id}: {e}")

async def compile_activities(user_telegram_id: str):
    user_activities = database.execute_sql(get_user_activities(user_telegram_id))
    activities_csv = [[a[2], a[3], a[4], a[5], a[6][:10]] for a in user_activities]
    file = io.StringIO()
    csv.writer(file).writerows(activities_csv)
    file.seek(0)
    buf = io.BytesIO()
    buf.write(file.getvalue().encode())
    buf.seek(0)
    await bot.send_document(user_telegram_id, buf, caption='activities.csv', visible_file_name='activities.csv')

def get_user_recent_activity(user_telegram_id):
    user_activities = database.execute_sql(get_user_activities(user_telegram_id))
    if len(user_activities) == 0:
        return None
    last_activity = user_activities[-1]
    return last_activity

def user_can_record_activity(user_telegram_id):

    current_datetime = datetime.datetime.now()
    if not in_range(RECORD_TIME_RANGE[0], RECORD_TIME_RANGE[1], current_datetime.time()):
        raise PermissionError('В данное вренмя нельзя сделать запись')
    user_activities = database.execute_sql(get_user_activities(user_telegram_id))

    if len(user_activities) == 0:
        return

    last_activity = user_activities[-1]
    if last_activity[6][:10] == datetime.date.today().strftime('%Y-%m-%d'):
        raise PermissionError('Нельзя записать активность дважды в день')

def in_range(start, end, i):
    return i >= start and i <= end

@bot.message_handler(commands=['stop'])
async def stop(message):
    if database.is_admin(message.from_user.id):
        global running
        running = False
        exit()

async def main_loop():
    global running
    while running:
        await send_messages_to_users()
        await asyncio.sleep(1)
    
async def polling():
    await bot.polling()


def run():
    global database
    global users_activities
    global running
    bot.add_custom_filter(asyncio_filters.StateFilter(bot))
    bot.add_custom_filter(asyncio_filters.IsDigitFilter())

    running = True
    users_activities = defaultdict(lambda: None)
    database = Database('database.db')
    database.connect()
    loop = asyncio.get_event_loop()
    loop.create_task(polling())
    loop.create_task(main_loop())
    loop.run_forever()
