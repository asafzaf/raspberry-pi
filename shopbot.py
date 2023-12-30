import time
import os
import datetime
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
import configShopBot
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
        # f = open('shoplist.txt', 'r')
        # obj = f.read()
        # f.close()
        # log = open('/home/asafz/tasks/shoplog.txt', 'a+')
        # log.write(f'{str(datetime.datetime.now())} | chat id: {chat_id} - {sender} | ask for list \n')
        # log.close()
        
        cursor.execute(f"SELECT * FROM cart_items WHERE bot_id = {bot_id} and is_bought = False")
        new_msg = ''
        res = cursor.fetchall()
        print(res)
        print("\n")
        print(len(res))
        if (len(res) != 0):
            for line in res:
                (id, class_name, num_of_objects, date) = line
                new_msg.join(f"{class_name}\n")
        else:
            new_msg.join("empty list...")
        bot.sendMessage(chat_id, new_msg)
    elif command == '/buyall':
        bot.sendMessage(chat_id, 'האם למחוק את הרשימה? (רשום - "קניתי הכל")')
    elif command == 'קניתי הכל':
        # f = open('shoplist.txt', 'w')
        # f.write('רשימת קניות:')
        # f.close()
        # log = open('/home/asafz/tasks/shoplog.txt', 'a+')
        # log.write(f'{str(datetime.datetime.now())} | chat id: {chat_id} - {sender} | deleted list \n')
        # log.close()
        
        
        bot.sendMessage(chat_id, 'עבודה טובה, הרשימה נמחקה...')
    else:
        # f = open('shoplist.txt', 'a+')
        # f.write(f'\n{command}')
        # f.close()
        # log = open('/home/asafz/tasks/shoplog.txt', 'a+')
        # log.write(f'{str(datetime.datetime.now())} | chat id: {chat_id} - {sender} | added {command}\n')
        # log.close()
        
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




