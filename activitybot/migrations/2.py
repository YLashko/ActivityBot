from activitybot.database import Database

def update_sql():
    return """
        ALTER TABLE users ADD COLUMN sent_message_date date
    """

def update():
    db = Database('activitybot/database.db')
    db.connect()
    db.execute_sql(update_sql())

if __name__ == "__main__":
    update()
