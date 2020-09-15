from bs4 import BeautifulSoup
import requests
import telepot
import datetime
from time import sleep
from emoji import emojize

token = '1389229800:AAG_wo7KQX-Qn-wV4nVK2ufOqZ9sO7yOM48'
bot = telepot.Bot(token)

headers = requests.utils.default_headers()
headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'})
emoji_perigo = emojize(":warning:", use_aliases=True)
exclamacao = emojize(":exclamation:", use_aliases=True)

while True:
    data = requests.get('http://br.investing.com/economic-calendar/', headers=headers)

    resultados = []

    if data.status_code == requests.codes.ok:
        info = BeautifulSoup(data.text, 'html.parser')
        blocos = ((info.find('table', {'id': 'economicCalendarData'})).find('tbody')).findAll('tr', {'class': 'js-event-item'})

        for blocos2 in blocos:
            impacto = str((blocos2.find('td', {'class': 'sentiment'})).get('data-img_key')).replace('bull1', f'{emoji_perigo}').replace('bull2', f'{emoji_perigo}{emoji_perigo}').replace('bull3',f'{emoji_perigo}{emoji_perigo}{emoji_perigo}')
            horario = str(blocos2.get('data-event-datetime')).replace('/', '-')
            horario2 = float(str(blocos2.get('data-event-datetime'))[11:16].replace(':', '.'))
            moeda = (blocos2.find('td', {'class': 'left flagCur noWrap'})).text.strip()
            noticia = blocos2.find('td', {'class': 'left event'}).find('a').text.strip()
            resultados.append({'PAR': moeda, 'HORÁRIO': horario, 'IMPACTO': impacto, 'HORARIO2': horario2, 'NOTÍCIA': noticia})

    while True:
        horario_agora = float(str(datetime.datetime.now())[11:16].replace(':', '.'))
        if horario_agora <= 23.59 or horario_agora >= 00.01: 
            for info in resultados:
                if round(float(info['HORARIO2'] - 1), 2) == horario_agora:
                    print(f'''{exclamacao}ATENÇÃO, ÁGUIAS! NOTÍCIA {exclamacao}\nPARIDADE: {info["PAR"]}\nHORÁRIO: {info["HORÁRIO"]}\nNOTÍCIA: {info["NOTÍCIA"]}\nIMPACTO: {info["IMPACTO"]}\n-----------------------------''')
                    bot.sendMessage(-481423284, f'''{exclamacao}ATENÇÃO, ÁGUIAS! NOTÍCIA {exclamacao}\nPARIDADE: {info["PAR"]}\nHORÁRIO: {info["HORÁRIO"]}\nNOTÍCIA: {info["NOTÍCIA"]}\nIMPACTO: {info["IMPACTO"]}\n-----------------------------''')
                sleep(0.5)
                horario_agora = float(str(datetime.datetime.now())[11:16].replace(':', '.'))


        else:
            break

#versao 1.0.8.4 - 15/09/2020
