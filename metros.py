import requests
import bs4
import re
import time

import psycopg2

import dbconf

conn = psycopg2.connect(database=dbconf.name,
                        host=dbconf.host,
                        user=dbconf.user,
                        password=dbconf.dbpass,
                        port=dbconf.port)

cursor = conn.cursor()

def attach(base, array):
    new_array = []
    for obj in array:
        new_array.append(f'{base}{obj}')
    return new_array

# class scope():
#     def __init__(self,name,num,title,text):
#         self.name = name
#         self.num = num
#         self.title = title
#         self.text = text

urls = []
scopes = {}

result = requests.get('https://www.israelhayom.co.il/horoscopes')
soup = bs4.BeautifulSoup(result.text, "lxml")

posts = soup.select('.post')

for post in posts:
    link = post.find('a', attrs={'href': re.compile("^/")})
    urls.append(link.get('href'))
    
new_urls = attach('https://www.israelhayom.co.il', urls)

for x in range(8):
    new_urls.pop()

print(len(new_urls))

for url in new_urls:
    temp_res = requests.get(url)
    temp_soup = bs4.BeautifulSoup(temp_res.text, 'lxml')
    temp_title = temp_soup.select('.titleText')
    temp_content = temp_soup.select('.text-content')
    delimiter = "<p>"
    delimiter2 = ">"
    trimmed_string = str(temp_content[0]).split(delimiter)[0]
    trimmed_string2 = trimmed_string.split(delimiter2)[1]
    
    if temp_title[0].text.find('יומית') != -1:
        scope_name = ''
        scope_num = 0
        if temp_title[0].text.find('גדי') != -1:
            scope_name = 'גדי'
            scope_num = 1
        elif temp_title[0].text.find('דלי') != -1:
            scope_name = 'דלי'
            scope_num = 2
        elif temp_title[0].text.find('דגים') != -1:
            scope_name = 'דגים'
            scope_num = 3
        elif temp_title[0].text.find('טלה') != -1:
            scope_name = 'טלה'
            scope_num = 4
        elif temp_title[0].text.find('שור') != -1:
            scope_name = 'שור'
            scope_num = 5
        elif temp_title[0].text.find('תאומים') != -1:
            scope_name = 'תאומים'
            scope_num = 6
        elif temp_title[0].text.find('סרטן') != -1:
            scope_name = 'סרטן'
            scope_num = 7
        elif temp_title[0].text.find('אריה') != -1:
            scope_name = 'אריה'
            scope_num = 8
        elif temp_title[0].text.find('בתולה') != -1:
            scope_name = 'בתולה'
            scope_num = 9
        elif temp_title[0].text.find('מאזניים') != -1:
            scope_name = 'מאזניים'
            scope_num = 10
        elif temp_title[0].text.find('עקרב') != -1:
            scope_name = 'עקרב'
            scope_num = 11
        elif temp_title[0].text.find('קשת') != -1:
            scope_name = 'קשת'
            scope_num = 12
        else:
            scope_name = 'תקלה'
        # scopes[f'{scope_name}'] = scope(scope_name, scope_num, temp_title[0].text, trimmed_string2 )
        cursor.execute(f"INSERT INTO metros (met, title, text) values ({scope_num}, '{temp_title[0].text}', '{trimmed_string2}')")  
        conn.commit()
    time.sleep(5)
    