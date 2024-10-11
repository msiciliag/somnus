'''scripts for database operations'''
from sqlalchemy import create_engine, Column, Integer, String, Text, MetaData, Table
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import inspect

Base = declarative_base()

class Config(Base):
    __tablename__ = 'config'
    key = Column(String, primary_key=True)
    value = Column(String)

class SleepRecord(Base):
    __tablename__ = 'sleep_record'
    id = Column(Integer, primary_key=True)
    date = Column(String)
    start_time = Column(String)
    end_time = Column(String)
    duration = Column(Integer)

class TimeTable(Base):
    __tablename__ = 'time_table'
    type = Column(String, primary_key=True)
    sleep_hour = Column(String)
    wake_up_hour = Column(String)
    duration = Column(Integer)

class Reminders(Base):
    __tablename__ = 'reminders'
    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)
    time = Column(Integer, nullable=False)
    days = Column(String)
    message = Column(String)
    sound = Column(String)
    active = Column(Integer, default=1)

DATABASE_URL = 'sqlite:///somnus.db'

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def create_db():
    '''create the database and tables'''
    Base.metadata.create_all(engine)
    print("Database created")
    inspector = inspect(engine)
    print("with tables: " + str(inspector.get_table_names()))

def is_db():
    '''check if the database exists'''
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    return len(tables) > 0

def get_user():
    '''get the user name from the database'''
    if not is_db():
        return ""
    user = session.query(Config).filter_by(key='user').first()
    return user.value if user else ""

def set_user(name):
    '''set the user name in the database'''
    insert_config('user', name)

def insert_config(key, value):
    '''insert a configuration value in the database'''
    config = session.query(Config).filter_by(key=key).first()
    if config:
        config.value = value
    else:
        config = Config(key=key, value=value)
        session.add(config)
    session.commit()

def insert_sleep_record(date, start_time, end_time, duration):
    '''insert a sleep record in the database'''
    record = SleepRecord(date=date, start_time=start_time, end_time=end_time, duration=duration)
    session.add(record)
    session.commit()

def insert_time_table(type, sleep_hour, wake_up_hour, duration):
    '''insert a time table in the database'''
    table = TimeTable(type=type, sleep_hour=sleep_hour, wake_up_hour=wake_up_hour, duration=duration)
    session.add(table)
    session.commit()

def insert_reminder(type, time, days, message, sound):
    '''insert a reminder in the database'''
    reminder = Reminders(type=type, time=time, days=days, message=message, sound=sound)
    session.add(reminder)
    session.commit()

def get_time_table(type):
    '''get the time table from the database'''
    table = session.query(TimeTable).filter_by(type=type).first()
    return table

def get_reminders():
    '''get all reminders from the database'''
    reminders = session.query(Reminders).all()
    return reminders

def get_reminder(id):
    '''get a reminder by id from the database'''
    reminder = session.query(Reminders).filter_by(id=id).first()
    return reminder

def delete_reminder(id):
    '''delete a reminder by id from the database'''
    reminder = session.query(Reminders).filter_by(id=id).first()
    session.delete(reminder)
    session.commit()

def update_reminder(id, type, time, days, message, sound, active):
    '''update a reminder by id in the database'''
    reminder = session.query(Reminders).filter_by(id=id).first()
    reminder.type = type
    reminder.time = time
    reminder.days = days
    reminder.message = message
    reminder.sound = sound
    reminder.active = active
    session.commit()

def get_sleep_records():
    '''get all sleep records from the database'''
    records = session.query(SleepRecord).all()
    return records

def get_sleep_record(id):
    '''get a sleep record by id from the database'''
    record = session.query(SleepRecord).filter_by(id=id).first()
    return record

def delete_sleep_record(id):
    '''delete a sleep record by id from the database'''
    record = session.query(SleepRecord).filter_by(id=id).first()
    session.delete(record)
    session.commit()

def update_sleep_record(id, date, start_time, end_time, duration):
    '''update a sleep record by id in the database'''
    record = session.query(SleepRecord).filter_by(id=id).first()
    record.date = date
    record.start_time = start_time
    record.end_time = end_time
    record.duration = duration
    session.commit()

def delete_time_table(type):
    '''delete a time table by type from the database'''
    table = session.query(TimeTable).filter_by(type=type).first()
    session.delete(table)
    session.commit()
    
def update_time_table(type, sleep_hour, wake_up_hour, duration):
    '''update a time table by type in the database'''
    table = session.query(TimeTable).filter_by(type=type).first()
    table.sleep_hour = sleep_hour
    table.wake_up_hour = wake_up_hour
    table.duration = duration
    session.commit()

def delete_all():
    '''delete all records from the database'''
    for table in Base.metadata.tables.keys():
        session.execute(f"DELETE FROM {table}")
    session.commit()

if __name__ == '__main__':
    create_db()
    set_user('Alice')
    print(is_db())
    print(get_user())
