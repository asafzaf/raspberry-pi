import time
import os
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
#import config

def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']
    
    print('Got command: %s' % command)
    if command == '/start':
        start_command(chat_id)
    elif command == '/shoplist':
        f = open('shoplist.txt', 'r')
        listobj = f.readline()
        bot.sendMessage(chat_id, listobj)
        f.close()
    elif command == '/buyall':
        f = open('shoplist.txt', 'w').close()
        bot.sendMessage(chat_id, 'עבודה טובה, הרשימה נמחקה...')
    else:
        f = open('shoplist.txt', 'w+')
        f.write(command)
        f.close()
        bot.sendMessage(chat_id, f'נוסף: {command}')

def start_command(chat_id):
    bot.sendMessage(chat_id, 'שלום! נא לרשום מוצרים לרשימת קניות..')

bot = telepot.Bot('6880455155:AAFjQrDZ3PCwkayPIEVi0kfK050pHOLe59U')
if __name__ == "__main__":
    MessageLoop(bot, handle).run_as_thread()
    print('I am listening ...')

while 1:
    time.sleep(10)




