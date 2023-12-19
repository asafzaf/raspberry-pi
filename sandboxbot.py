import time
import os
import datetime
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
import configSandboxBot

def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']
    
    print('Got command: %s' % command)
    if command == '/start':
        start_command(chat_id)
    print(msg)

def start_command(chat_id):
    bot.sendMessage(chat_id, 'Hello!')

bot = telepot.Bot(configSandboxBot.token)
if __name__ == "__main__":
    MessageLoop(bot, handle).run_as_thread()
    print('I am listening ...')

while 1:
    time.sleep(10)




