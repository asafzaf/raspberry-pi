import time
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
import configMetrosBot

from apscheduler.schedulers.blocking import BlockingScheduler


import psycopg2

import dbconf

def handle(msg):
    
    conn = psycopg2.connect(database=dbconf.name,
                        host=dbconf.host,
                        user=dbconf.user,
                        password=dbconf.dbpass,
                        port=dbconf.port)

    cursor = conn.cursor()
    chat_id = msg['chat']['id']
    sender = msg['from']['first_name']
    command = msg['text']

    print('Got command: %s' % command)
    sign_num = 0
    title = ''
    text = ''
    if command == '/start':
        start_command(chat_id)
    else:
        if command.split(" ",2)[0] == 'אני' and command.split(" ",2)[1] == 'גר' and command.split(" ",2)[2][0] == 'ב':
            city = command.split(" ", 2)[2].split("", 1)[1]
            cursor.execute(f"SELECT cities_weather.id, cities_weather.hebrew FROM cities_weather WHERE cities_weather.name_hebrew LIKE '%{city}%'")
            res = cursor.fetchone()
            if(res):
                (city_id, name) = res
                cursor.execute(f"INSERT INTO weather_users (telegram_name, chat_id, city_id) VALUES ('{sender}', '{chat_id}', '{city_id}');")
                conn.commit()
                mes = f'הרשמתך לתחזית לעיר {name} בוצעה בהצלחה!'
            else:
                mes = 'אני לא מכיר את העיר שרשמת.. אנא רשום שוב או פנה לאסף'
            bot.sendMessage(chat_id, mes, parse_mode='Markdown')
        elif command.split(" ",1)[0] == 'תחזית':
            city = command.split(" ", 1)[1]
            cursor.execute(f"SELECT cities_weather.name_hebrew, weather.date, weather.min_temp, weather.max_temp, weather.avg_temp, weather.max_wind_kph, weather.will_it_rain, weather.daily_rain_chance, weather.sun_rise, weather.sun_set, weather.moon_rise, weather.moon_set FROM weather INNER JOIN cities_weather ON cities_weather.id = weather.city_id WHERE cities_weather.name_hebrew LIKE '%{city}%' ORDER BY weather.date asc LIMIT 1;")
            # distract the result
            res = cursor.fetchone()
            if(res):
                (city_name, date, min_temp, max_temp, avg_temp, max_wind_kph, will_it_rain, daily_chance_of_rain, sunrise, sunset, moonrise, moonset) = res
                if(will_it_rain):
                    rain = 'ירד גשם'
                else:
                    rain = 'לא ירד גשם'
                mes = f'תחזית יומית!\nעיר: {city_name}\nתאריך: {date}\nטמפרטורה: {min_temp}°c - {max_temp}°c ({avg_temp}°c)\nרוח: {max_wind_kph}/קמ"ש\nירד גשם? {rain} ({daily_chance_of_rain}%)\nשמש:\nזריחה: {sunrise}\nשקיעה: {sunset}\nירח:\nזריחה: {moonrise}\nשקיעה: {moonset}'
            else:
                mes = 'אני לא מכיר את העיר שרשמת.. אנא רשום שוב או פנה לאסף'
            bot.sendMessage(chat_id, mes, parse_mode='Markdown')
        elif command.split(" ",2)[0] == 'אני' and command.split(" ",2)[1] == 'מזל':
            sign_num = sign_translate(command.split(" ",2)[2])
            if (sign_num != 0):
                print("rgister user")
                cursor.execute(f"INSERT INTO met_users (telegram_name, chat_id, sign) VALUES ('{sender}', '{chat_id}', '{sign_num}')")
                conn.commit()
                cursor.execute(f"SELECT met_users.id, met_signs.name FROM met_users INNER JOIN met_signs ON met_users.sign = met_signs.id WHERE chat_id = '{chat_id}';")
                res = cursor.fetchone()
                if (res):
                    (id, sign_name) = res
                    title = "*ההרשמה בוצעה בהצלחה!*"
                    text = f"המזל הנבחר הוא - *{sign_name}*"
            else:
                title = '*אני לא יודע מה רשמת...*'
                text = 'אנא רשום מזל או רשום "אני מזל *_שם המזל_*"' 
            # title = '*בקרוב!*'
            # text = 'אופציה להרשמה לקבלת הודעה יומית'
            print("בחירת מזלללל")
            mes = title + '\n' + text
            bot.sendMessage(chat_id, mes, parse_mode='Markdown')
        elif command == 'הסר':
            title = '*בקרוב!*'
            text = 'אופציה להסרה מהודעה יומית'
        else:
            sign_num = sign_translate(command)
            if (sign_num != 0):
                cursor.execute(f"SELECT metros.title, metros.text FROM metros WHERE metros.met = {sign_num} order by metros.id desc limit 1;")  
                res = cursor.fetchone()
                if (res):
                    (title, text) = res
                    title = '*' + title + '*'
                else:
                    mes = "Error!"  
            else:
                title = '*אני לא יודע מה רשמת...*'
                text = 'אנא רשום מזל או רשום "אני מזל *_שם המזל_*"' 
            mes = title + '\n' + text
            bot.sendMessage(chat_id, mes, parse_mode='Markdown')
    conn.close()

def start_command(chat_id):
    bot.sendMessage(chat_id, 'היי ברוך הבא להורוסקופ!\nאנא רשום מזל:')
    
def sign_translate(command):
    if command == 'גדי':
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
    else:
        sign_num = 0
    print(f"sign num: {sign_num}")
    return sign_num
    
def my_interval_job():
    conn = psycopg2.connect(database=dbconf.name,
                        host=dbconf.host,
                        user=dbconf.user,
                        password=dbconf.dbpass,
                        port=dbconf.port)

    cursor = conn.cursor()
    
    cursor.execute("SELECT met_users.chat_id, met_users.sign FROM met_users WHERE met_users.is_active = True;")
    users = cursor.fetchall()
    
    for user in users:
        (chat_id, sign) = user
        cursor.execute(f"SELECT metros.title, metros.text FROM metros WHERE metros.met = {sign} order by metros.id desc limit 1;") 
        res = cursor.fetchone() 
        (met_title, met_text) = res
        if (res):
            (title, text) = res
            title = '*' + title + '*'
        else:
            mes = "Error!"   
        mes = title + '\n' + text
        bot.sendMessage(chat_id, mes, parse_mode='Markdown')
        
    
    cursor.execute("SELECT chat_id, city_id FROM weather_users WHERE met_users.is_active = True;")
    users = cursor.fetchall()
    
    for user in users:
        (chat_id, city_id) = user
        cursor.execute(f"SELECT cities_weather.name_hebrew, weather.date, weather.min_temp, weather.max_temp, weather.avg_temp, weather.max_wind_kph, weather.will_it_rain, weather.daily_rain_chance, weather.sun_rise, weather.sun_set, weather.moon_rise, weather.moon_set FROM weather INNER JOIN cities_weather ON cities_weather.id = weather.city_id WHERE cities_weather.name_hebrew LIKE '%{city}%' ORDER BY weather.date asc LIMIT 1;")
            # distract the result
        res = cursor.fetchone()
        if(res):
            (city_name, date, min_temp, max_temp, avg_temp, max_wind_kph, will_it_rain, daily_chance_of_rain, sunrise, sunset, moonrise, moonset) = res
            if(will_it_rain):
                rain = 'ירד גשם'
            else:
                rain = 'לא ירד גשם'
            mes = f'תחזית יומית!\nעיר: {city_name}\nתאריך: {date}\nטמפרטורה: {min_temp}°c - {max_temp}°c ({avg_temp}°c)\nרוח: {max_wind_kph}/קמ"ש\nירד גשם? {rain} ({daily_chance_of_rain}%)\nשמש:\nזריחה: {sunrise}\nשקיעה: {sunset}\nירח:\nזריחה: {moonrise}\nשקיעה: {moonset}'
        bot.sendMessage(chat_id, mes, parse_mode='Markdown')
    
    conn.close()
    

sched = BlockingScheduler()

bot = telepot.Bot(configMetrosBot.token)
if __name__ == "__main__":
    MessageLoop(bot, handle).run_as_thread()
    print('I am listening ...')
    
    sched.add_job(my_interval_job, trigger="cron", hour=8)
    sched.start()
    print('Schedule is ready ...')

while 1:
    time.sleep(10)
