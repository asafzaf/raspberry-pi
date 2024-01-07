import time
import random
import datetime
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
import sqlite3


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    #chat_id = msg['chat']['id']
    #command = msg['text']
    if content_type == 'text':
        handle_text(msg)

def handle_text(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    command = msg['text']
    print('Got command: %s' % command)
    if command == '/start':
        start_command(chat_id)
    elif command == '/swift':
        send_question(chat_id)
    else:
        bot.sendMessage(chat_id, 'What?..')

def start_command(chat_id):
    sqlite_user_Query = f'select * from employee where chat_id = {chat_id}'
    cursor.execute(sqlite_user_Query)
    res = cursor.fetchone()
    if len(res) == 0:
        bot.sendMessage(chat_id, 'Welcome! How can i help you?')
    else:
        bot.sendMessage(chat_id, f'Welcome {res.first_name}, welcome back!')
    print(chat_id)


def send_question(chat_id):
    options = ['Add swift', 'Change swift', 'Delete swift', 'Make file']
    keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=option)] for option in options], one_time_keyboard=True)
    bot.sendMessage(chat_id, 'Choose an option:', reply_markup=keyboard)

bot = telepot.Bot('6356050984:AAHTm7LtD2HDq2AsjbLxa9NsAcXsbfUFMpk')

try:
    sqliteConnection = sqlite3.connect('swifts.db')
    cursor = sqliteConnection.cursor()
    print("Database created and Successfully Connected to SQLite")
    sqlite_select_Query = "select sqlite_version();"
    cursor.execute(sqlite_select_Query)
    record = cursor.fetchall()
    print("SQLite Database Version is: ", record)
    cursor.close()
    
except sqlite3.Error as error:
    print("Error while connecting to sqlite", error)
    
#finally:
#    if sqliteConnection:
#        sqliteConnection.close()
#        print("The SQLite connection is closed")


if __name__ == "__main__":
    MessageLoop(bot, handle).run_as_thread()
    print('I am listening ...')

while 1:
    time.sleep(10)

