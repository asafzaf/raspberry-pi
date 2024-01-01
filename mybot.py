import time
import random
import datetime
# import telepot
# from telepot.loop import MessageLoop
# from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
import configMyBot
# import urllib.request

import sys
print(sys.path)

import os

with open('/home/asafz/tasks/output_file.txt', 'w') as f:
    for key, value in os.environ.items():
        f.write(f'{key}={value}\n')

with open('/home/asafz/tasks/output_file123.txt', 'w') as f:
    for path in sys.path:
        f.write(f"{path}\n")



"""
After **inserting token** in the source code, run it:

```
$ python2.7 diceyclock.py
```

[Here is a tutorial](http://www.instructables.com/id/Set-up-Telegram-Bot-on-Raspberry-Pi/)
teaching you how to setup a bot on Raspberry Pi. This simple bot does nothing
but accepts two commands:

- `/roll` - reply with a random integer between 1 and 6, like rolling a dice.
- `/time` - reply with the current time, like a clock.
"""

array = 'Mercury:\nFrom 29.12.2022 until 18.1.2023\nFrom 21.4.2022 until 15.5.2023\nFrom 23.8.2023 until 15.9.2023\nFrom 13.12.2023 until 2.1.2024'

def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']

    print('Got command: %s' % command)
    if command == '/start':
        start_command(chat_id)
    elif command == '/roll':
        bot.sendMessage(chat_id, random.randint(1,6))
    elif command == '/time':
        bot.sendMessage(chat_id, str(datetime.datetime.now()))
    elif command == '/mercury':
        bot.sendMessage(chat_id, array)
    elif command == '/question':
        send_question(chat_id)
    elif command == '/ip':
        external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')
        bot.sendMessage(chat_id, 'Wait a second...')
        time.sleep(1)
        bot.sendMessage(chat_id, external_ip)
    else:
        bot.sendMessage(chat_id, 'What?..')

def start_command(chat_id):
    bot.sendMessage(chat_id, 'Welcome! How can i help you?')

def send_question(chat_id):
    options = ['Option 1', 'Option 2', 'Option 3']
    keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=option)] for option in options], one_time_keyboard=True)
    bot.sendMessage(chat_id, 'Choose an option:', reply_markup=keyboard)

bot = telepot.Bot(configMyBot.token)
if __name__ == "__main__":
    MessageLoop(bot, handle).run_as_thread()
    print('I am listening ...')

while 1:
    time.sleep(10)

