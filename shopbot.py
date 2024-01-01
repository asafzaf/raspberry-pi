import time

import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
import configShopBot
import sys
print(sys.path)

import os

with open('/home/asafz/tasks/output_file.txt', 'w') as f:
    for key, value in os.environ.items():
        f.write(f'{key}={value}\n')

with open('/home/asafz/tasks/output_file123.txt', 'w') as f:
    for path in sys.path:
        f.write(f"{path}\n")
        
import psycopg2

import dbconf

def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']
    sender = msg['from']['first_name']
    bot_id = '94'
    
    conn = psycopg2.connect(database=dbconf.name,
                        host=dbconf.host,
                        user=dbconf.user,
                        password=dbconf.dbpass,
                        port=dbconf.port)

    cursor = conn.cursor()
    
    print('Got command: %s' % command)
    if command == '/start':
        start_command(chat_id)
    elif command == '/shoplist':
        cursor.execute(f"SELECT cart_items.id, items.name FROM cart_items LEFT JOIN items on cart_items.item_id = items.id WHERE bot_id = {bot_id} and is_bought = False")
        new_msg = ''
        list_items = []
        res = cursor.fetchall()
        if (len(res) != 0):
            for line in res:
                (id, item_name) = line
                list_items.append(item_name)
            for item in list_items:
                new_msg = new_msg + '\n' + item
        else:
            new_msg = new_msg.join("empty list...")
        bot.sendMessage(chat_id, new_msg)
    elif command == '/buyall':
        bot.sendMessage(chat_id, 'האם למחוק את הרשימה? (רשום - "קניתי הכל")')
    elif command == 'קניתי הכל':
        cursor.execute(f"UPDATE cart_items SET is_bought = True, time_bought = CURRENT_TIMESTAMP WHERE bot_id = {bot_id};")        
        conn.commit()
        bot.sendMessage(chat_id, 'עבודה טובה, הרשימה נמחקה...')
    else:
        cursor.execute(f"SELECT * FROM items WHERE name = '{command}'")
        res = cursor.fetchone()
        
        if(res == None):
            cursor.execute(f"INSERT INTO items (name) values ('{command}')")  
            conn.commit()
            cursor.execute(f"SELECT * FROM items WHERE name = '{command}'")
            res = cursor.fetchone()

        (id, name, class_id) = res
        cursor.execute(f"INSERT INTO cart_items (item_id, bot_id, chat_id) values ('{id}', '{bot_id}', '{chat_id}')")  
        conn.commit()
        
        bot.sendMessage(chat_id, f'נוסף: {command}')
    
    conn.close()
    
def start_command(chat_id):
    bot.sendMessage(chat_id, 'שלום! נא לרשום מוצרים לרשימת קניות..')

bot = telepot.Bot(configShopBot.token)
if __name__ == "__main__":
    MessageLoop(bot, handle).run_as_thread()
    print('I am listening ...')

while 1:
    time.sleep(10)




