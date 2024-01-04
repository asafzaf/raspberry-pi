import time
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
import configMetrosBot

import psycopg2

import dbconf

conn = psycopg2.connect(database=dbconf.name,
                        host=dbconf.host,
                        user=dbconf.user,
                        password=dbconf.dbpass,
                        port=dbconf.port)

cursor = conn.cursor()

def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']

    print('Got comma    nd: %s' % command)
    sign_num = 0
    title = ''
    text = ''
    if command == '/start':
        sign_num = 77
        start_command(chat_id)
    elif command.split(" ",2)[0] == 'אני' and command.split(" ",2)[1] == 'מזל':
        #add to list
        x = 5
        print("בחירת מזלללל")
    elif command == 'גדי':
        sign_num = 1
    elif command == 'דלי':
        sign_num = 2
    elif command == 'דגים':
        sign_num = 3
    elif command == 'טלה':
        sign_num = 4
    elif command == 'שור':
        sign_num = 5
    elif command == 'תאומים':
        sign_num = 6
    elif command == 'סרטן':
        sign_num = 7
    elif command == 'אריה':
        sign_num = 8
    elif command == 'בתולה':
        sign_num = 9
    elif command == 'מאזניים':
        sign_num = 10
    elif command == 'עקרב':
        sign_num = 11
    elif command == 'קשת':
        sign_num = 12
    elif command == 'הסר':
        x = 9
        print("הסרהההה")
    else:
        sign_num = 0
        title = 'אני לא יודע מה רשמת...'
        text = 'אנא רשום מזל או רשום "אני מזל _____"'
    if sign_num != 0:
        cursor.execute(f"SELECT metros.title, metros.text FROM metros WHERE metros.met = {sign_num} order by metros.id desc limit 1;")  
        res = cursor.fetchone()
        (title, text) = res
    bot.sendMessage(chat_id, "*" + title + "*\n" + text)

def start_command(chat_id):
    bot.sendMessage(chat_id, 'היי ברוך הבא להורוסקופ!\nאנא רשום מזל:')

bot = telepot.Bot(configMetrosBot.token)
if __name__ == "__main__":
    MessageLoop(bot, handle).run_as_thread()
    print('I am listening ...')

while 1:
    time.sleep(10)
