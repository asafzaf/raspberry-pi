import time
import random
import datetime
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton


def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']

    print('Got command: %s' % command)
    if command == '/start':
        start_command(chat_id)
    elif command == '/question':
        send_question(chat_id)
    else:
        bot.sendMessage(chat_id, 'What?..')

def start_command(chat_id):
    bot.sendMessage(chat_id, 'Welcome! How can i help you?')
    print(chat_id)



def send_question(chat_id):
    options = ['Option 1', 'Option 2', 'Option 3']
    keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=option)] for option in options], one_time_keyboard=True)
    bot.sendMessage(chat_id, 'Choose an option:', reply_markup=keyboard)

bot = telepot.Bot('6356050984:AAHTm7LtD2HDq2AsjbLxa9NsAcXsbfUFMpk')
if __name__ == "__main__":
    MessageLoop(bot, handle).run_as_thread()
    print('I am listening ...')

while 1:
    time.sleep(10)
