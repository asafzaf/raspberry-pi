import time

import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
import configYarinShopBot
# import sys
# print(sys.path)

# import os

# with open('/home/asafz/tasks/output_file.txt', 'w') as f:
#     for key, value in os.environ.items():
#         f.write(f'{key}={value}\n')

# with open('/home/asafz/tasks/output_file123.txt', 'w') as f:
#     for path in sys.path:
#         f.write(f"{path}\n")
        
import psycopg2

import dbconf

def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']
    bot_id = '32'
    
    conn = psycopg2.connect(database=dbconf.name,
                        host=dbconf.host,
                        user=dbconf.user,
                        password=dbconf.dbpass,
                        port=dbconf.port)

    cursor = conn.cursor()
    
    print('Got command: %s' % command)
    if command == '/start':
        start_command(chat_id)
    elif command.split(" ",1)[0] == 'קניתי':
        item = command.split(" ",1)[1]
        cursor.execute(f"SELECT cart_items.id, items.name, departments.name FROM cart_items LEFT JOIN items on cart_items.item_id = items.id LEFT JOIN departments on items.department_id = departments.id WHERE cart_items.is_bought is False and bot_id = '{bot_id}' and items.name LIKE '{item}%';")
        res = cursor.fetchall()
        new_msg = ''
        if (len(res) == 1):
            for line in res:
                (id, item_name, department_name) = line
                cursor.execute(f"UPDATE cart_items SET is_bought = True,  time_bought = CURRENT_TIMESTAMP WHERE cart_items.id = '{id}'")   
                conn.commit()
                new_msg = f'*{item_name}* - נקנה'
        elif (len(res) >= 2):
            new_msg = 'ישנם מספר פריטים דומים:'
            for line in res:
                (id, item_name, department_name) = line
                new_msg = new_msg + '\n' + ' - *' + item_name + '*' + f'  - ({department_name})'
        else:
            new_msg = f"לא נמצא פריט בשם '{item}' ברשימה שלך"
        bot.sendMessage(chat_id, new_msg, parse_mode= 'Markdown')
    elif command == '/shoplist':
        cursor.execute(f"SELECT cart_items.id, items.name, departments.name FROM cart_items LEFT JOIN items on cart_items.item_id = items.id LEFT JOIN departments on items.department_id = departments.id WHERE cart_items.is_bought is False and bot_id = '{bot_id}' order by departments.id asc;")
        new_msg = ''
        res = cursor.fetchall()
        if (len(res) != 0):
            new_msg = 'רשימת קניות:'
            for line in res:
                (id, item_name, department_name) = line
                new_msg = new_msg + '\n' + '*' + item_name + '*' + f'  - ({department_name})'
        else:
            new_msg = new_msg.join("רשימת הקניות ריקה...")
        bot.sendMessage(chat_id, new_msg, parse_mode= 'Markdown')
    elif command == '/myhistory':
        cursor.execute(f"select distinct items.name, departments.name from cart_items left join items on cart_items.item_id = items.id left join departments on items.department_id = departments.id where cart_items.bot_id = '{bot_id}' order by departments.name asc;")
        new_msg = ''
        res = cursor.fetchall()
        if (len(res) != 0):
            new_msg = 'היסטורית פריטים שהוספת:'
            for line in res:
                (item_name, department_name) = line
                new_msg = new_msg + '\n' + '*' + item_name + '*' + f'  - ({department_name})'
        else:
            new_msg = new_msg.join("מעולם לא הוספת פריטים...")
        bot.sendMessage(chat_id, new_msg, parse_mode= 'Markdown')
    elif command == '/allitems':
        cursor.execute(f"select items.name, departments.name from items left join departments on items.department_id = departments.id order by departments.name asc;")
        new_msg = ''
        res = cursor.fetchall()
        if (len(res) != 0):
            new_msg = 'רשימת כל המוצרים שאני מכיר:'
            for line in res:
                (item_name, department_name) = line
                new_msg = new_msg + '\n' + '*' + item_name + '*' + f'  - ({department_name})'
        else:
            new_msg = new_msg.join("מעולם לא הוספת פריטים...")
        bot.sendMessage(chat_id, new_msg, parse_mode= 'Markdown')
    elif command == '/buyall':
        bot.sendMessage(chat_id, 'האם למחוק את הרשימה? (רשום - "קניתי הכל")')
    elif command == 'קניתי הכל':
        cursor.execute(f"UPDATE cart_items SET is_bought = True, time_bought = CURRENT_TIMESTAMP WHERE bot_id = '{bot_id}';")        
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
        bot.sendMessage(chat_id, f'נוסף: *{command}*', parse_mode= 'Markdown')
    conn.close()
    
def start_command(chat_id):
    bot.sendMessage(chat_id, 'שלום! נא לרשום מוצרים לרשימת קניות..')

bot = telepot.Bot(configYarinShopBot.token)
if __name__ == "__main__":
    MessageLoop(bot, handle).run_as_thread()
    print('I am listening ...')

while 1:
    time.sleep(10)




