def reset_tables():
    return [
    '''
    drop table if exists users
    ''',
    '''
    drop table if exists records
    ''',
    '''
    create table if not exists users (
        id integer primary key autoincrement,
        telegram_id text unique not null,
        telegram_nickname unique not null 
    )
    ''',
    '''
    create table if not exists records (
        id integer primary key autoincrement,
        user_telegram_id text not null,
        activity_mark_absolute integer not null,
        activity_mark_relative integer not null,
        mood_mark_absolute integer not null,
        mood_mark_relative integer not null,
        record_date date default current_timestamp not null,
        foreign key (user_telegram_id)
            references users (telegram_id)
                on update cascade
                on delete cascade
    )    
    ''']

def create_user(telegram_id: str, telegram_nickname: str):
    return f'''
        insert into users (telegram_id, telegram_nickname)
        values
        ('{telegram_id}', '{telegram_nickname}');
    '''

def set_users_default_date():
    return f'''
        update users
        set sent_message_date = date('now', '-1 day')
        where sent_message_date is null
    '''

def update_users_date_to_today():
    return f"""
        update users
        set sent_message_date = date('now')
        where sent_message_date < date('now')
    """

def get_user(telegram_id: str):
    return f'''
        select * from users
        where users.telegram_id = {telegram_id}
    '''

def delete_user_by_telegram_name(name):
    return f'''
        DELETE from users
        where users.telegram_nickname = {name}
    '''

def get_all_users():
    return '''
        select users.telegram_id, users.telegram_nickname, users.sent_message_date
        from users
    '''

def create_activity_record(user_telegram_id: str, activity_mark_absolute: int, activity_mark_relative: int, mood_mark_absolute: int, mood_mark_relative: int):
    return f'''
        insert into records (user_telegram_id, activity_mark_absolute, activity_mark_relative, mood_mark_absolute, mood_mark_relative)
        values 
        ('{user_telegram_id}', {activity_mark_absolute}, {activity_mark_relative}, {mood_mark_absolute}, {mood_mark_relative})
    '''

def get_user_activities(user_telegram_id: str):
    return f'''
        select * from records
        where records.user_telegram_id = {user_telegram_id}
    '''
