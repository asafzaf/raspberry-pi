import time
import os
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
import configShopBot

def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']
    
    print('Got command: %s' % command)
    if command == '/start':
        start_command(chat_id)
    elif command == '/shoplist':
        f = open('shoplist.txt', 'r')
        obj = f.read()
        bot.sendMessage(chat_id, obj)
        f.close()
    elif command == '/buyall':
        bot.sendMessage(chat_id, 'האם למחוק את הרשימה? (רשום - "קניתי הכל")')
    elif command == 'קניתי הכל':
        f = open('shoplist.txt', 'w')
        f.write('רשימת קניות:')
        f.close()
        bot.sendMessage(chat_id, 'עבודה טובה, הרשימה נמחקה...')
    else:
        f = open('shoplist.txt', 'a+')
        f.write(f'\n{command}')
        f.close()
        bot.sendMessage(chat_id, f'נוסף: {command}')

def start_command(chat_id):
    bot.sendMessage(chat_id, 'שלום! נא לרשום מוצרים לרשימת קניות..')

bot = telepot.Bot(configShopBot.token)
if __name__ == "__main__":
    MessageLoop(bot, handle).run_as_thread()
    print('I am listening ...')

while 1:
    time.sleep(10)




