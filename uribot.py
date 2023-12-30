import time
import os
import datetime
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
import configUriBot

def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']
    sender = msg['from']['first_name']
    
    print('Got command: %s' % command)
    if command == '/start':
        start_command(chat_id)
    elif command == '/shoplist':
        f = open('urilist.txt', 'r')
        obj = f.read()
        f.close()
        log = open('/home/asafz/tasks/urilog.txt', 'a+')
        log.write(f'{str(datetime.datetime.now())} | chat id: {chat_id} - {sender} | ask for list \n')
        log.close()
        bot.sendMessage(chat_id, obj)
    elif command == '/buyall':
        bot.sendMessage(chat_id, 'האם למחוק את הרשימה? (רשום - "קניתי הכל")')
    elif command == 'קניתי הכל':
        f = open('urilist.txt', 'w')
        f.write('רשימת קניות:')
        f.close()
        log = open('/home/asafz/tasks/urilog.txt', 'a+')
        log.write(f'{str(datetime.datetime.now())} | chat id: {chat_id} - {sender} | deleted list \n')
        log.close()
        bot.sendMessage(chat_id, 'עבודה טובה, הרשימה נמחקה...')
    else:
        f = open('urilist.txt', 'a+')
        f.write(f'\n{command} - {sender}')
        f.close()
        log = open('/home/asafz/tasks/urilog.txt', 'a+')
        log.write(f'{str(datetime.datetime.now())} | chat id: {chat_id} - {sender} | added {command}\n')
        log.close()
        bot.sendMessage(chat_id, f'נוסף: {command}')

def start_command(chat_id):
    bot.sendMessage(chat_id, 'שלום! נא לרשום מוצרים לרשימת קניות..')

bot = telepot.Bot(configUriBot.token)
if __name__ == "__main__":
    MessageLoop(bot, handle).run_as_thread()
    print('I am listening ...')

while 1:
    time.sleep(10)



