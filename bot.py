"""
Домашнее задание №1

Использование библиотек: ephem

* Установите модуль ephem
* Добавьте в бота команду /planet, которая будет принимать на вход
  название планеты на английском, например /planet Mars
* В функции-обработчике команды из update.message.text получите
  название планеты (подсказка: используйте .split())
* При помощи условного оператора if и ephem.constellation научите
  бота отвечать, в каком созвездии сегодня находится планета.

"""

from datetime import date, datetime, timedelta
import locale
import logging
import random
import ephem
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import settings

logging.basicConfig(filename='bot.log', level=logging.INFO)

PROXY = {'proxy_url': settings.PROXY_URL, 'urllib3_proxy_kwargs': {'username': settings.PROXY_USERNAME,
         'password': settings.PROXY_PASSWORD}}


def greet_user(update, context):
    print('Called /start')
    update.message.reply_text('Приветствую представителя третьего по разумности вида на планете Земля.\nКакой '
                              'вопрос ты хочешь задать Думателю?')


def lets_talk(update, context):
    user_text = update.message.text
    user_text = user_text.lower()
    print(user_text)
    if 'до свидания' in user_text or 'до свиданья' in user_text or 'пока' in user_text or 'прощай' in user_text:
        update.message.reply_text('Прощай. И помни: галактика суровая штука. '
                                  'Чтобы в ней выжить, надо знать, где твое полотенце.')
    elif 'вопрос жизни' in user_text:
        wrong_answer_list = ['главный вопрос жизни, вселенной и всего такого',
                             'основной вопрос жизни, вселенной и всего остального',
                             'главный вопрос жизни, вселенной и всего-всего',
                             'жизни, вселенной и всего на свете',
                             'главный вопрос о жизни, вселенной и всяком таком']
        if 'самый главный вопрос жизни, вселенной и вообще' in user_text:
            update.message.reply_text('42')
        else:
            for line in wrong_answer_list:
                if user_text in line:
                    update.message.reply_text('Возвращайся на это же место через семь с половиной миллионов лет ровно.')

    else:
        update.message.reply_text(f'сам ты {user_text}')


def astrolog(update, context):
    planet_name = update.message.text
    planet_name = planet_name.split()
    planet_name = planet_name[1]
    planet_name = planet_name.capitalize()
    print(planet_name)
    locale.setlocale(locale.LC_ALL, "russian")
    date_now = datetime.now()
    delta_1 = timedelta(days=1)
    tomorrow = date_now + delta_1
    if 'Меркурий' in planet_name:
        planet_name = ephem.Mercury(tomorrow)
        constellation = ephem.constellation(planet_name)
    elif 'Венера' in planet_name:
        planet_name = ephem.Venus(tomorrow)
        constellation = ephem.constellation(planet_name)
    elif 'Земля' in planet_name:
        planet_name = ephem.Earth(tomorrow)
        constellation = ephem.constellation(planet_name)
    elif 'Марс' in planet_name:
        planet_name = ephem.Mars(tomorrow)
        constellation = ephem.constellation(planet_name)
    elif 'Юпитер' in planet_name:
        planet_name = ephem.Jupiter(tomorrow)
        constellation = ephem.constellation(planet_name)
    elif 'Сатурн' in planet_name:
        planet_name = ephem.Saturn(tomorrow)
        constellation = ephem.constellation(planet_name)
    elif 'Уран' in planet_name:
        planet_name = ephem.Uranus(tomorrow)
        constellation = ephem.constellation(planet_name)
    elif 'Нептун' in planet_name:
        planet_name = ephem.Neptune(tomorrow)
        constellation = ephem.constellation(planet_name)
    print(constellation)
    update.message.reply_text(constellation)


def next_full_moon(update, context):
    user_text = update.message.text
    print(user_text)
    locale.setlocale(locale.LC_ALL, "russian")
    date_now = date.today()
    print(date_now)
    if '/next_full_moon' in user_text.lower():
        full_moon = ephem.next_full_moon(date_now)
        print(full_moon)
        update.message.reply_text(full_moon)


def wordcount(update, context):
    user_text = update.message.text
    print(user_text)
    text = user_text.split()
    text_list = text[1:]
    sentence = ''.join(text_list)
    if sentence == '' or set('[~!@#$%^&*,()_+{}":;\']+$').intersection(sentence) or sentence.isdigit():
        update.message.reply_text(f'Фраза состоит из пустой строки, одно из слов '
                                  f'состоит только из чисел или фраза включает спец. символы')
    else:
        update.message.reply_text(f'Количество слов во фразе: {len(text_list)}')


def cities(update, context):
    with open('cities.txt', encoding='utf-8') as f:
        cities_file = f.read()
    cities_list = cities_file.split()
    print(cities_list)
    avaiable_cities = list(cities_list)
    random.shuffle(avaiable_cities)

    game_over = False
    while not game_over:
        user_answer = update.message.text
        print(user_answer)
        user_answer = user_answer.split()
        user_answer = user_answer[1:]
        user_answer = ''.join(user_answer)
        print(user_answer)

        exeption_list = ['й', 'ь', 'ы', 'ъ']
        if user_answer.lower()[-1] in exeption_list:
            last_user_literal = user_answer.lower()[-2]
        else:
            last_user_literal = user_answer.lower()[-1]

        if user_answer not in cities_list:
            update.message.reply_text('похоже что это не город')
        elif user_answer not in avaiable_cities:
            update.message.reply_text('этот город уже называли до этого')
        else:
            last_user_literal = user_answer.lower()[-1]
            avaiable_cities.remove(user_answer)

            for possible_city in avaiable_cities:
                if possible_city[0] == last_user_literal.upper():
                    bot_answer = possible_city
                    avaiable_cities.remove(bot_answer)
                    update.message.reply_text(bot_answer)
                    if bot_answer[-1] in exeption_list:
                        last_bot_literal = bot_answer[-2]
                    else:
                        last_bot_literal = bot_answer[-1]
                    break
            else:
                game_over = True
                update.message.reply_text('я не знаю больше городов на ' + last_user_literal)


def calculator(update, context):
    user_text = update.message.text
    print(user_text)
    text = user_text.split()
    text_list = text[1:]
    expression = ''.join(text_list)
    print(expression)
    try:
        expression = expression.lower().replace(' ', '')
        parts = expression.split('+')
        for plus in range(len(parts)):
            if '-' in parts[plus]:
                parts[plus] = parts[plus].split('-')
        for plus in range(len(parts)):
            parts[plus] = precalculator(parts[plus])
        result = sum(parts)
    except ValueError:
        result = 'Введен не верный тип данных'
    except ZeroDivisionError:
        result = 'Попытка разделить на ноль'
    update.message.reply_text(result)
    print(result)


def precalculator(part):
    if type(part) is str:
        if '*' in part:
            result = 1
            for subpart in part.split('*'):
                result *= precalculator(subpart)
            return result
        elif '/' in part:
            parts = list(map(precalculator, part.split('/')))
            result = parts[0]
            for subpart in parts[1:]:
                result /= subpart
            return result
        else:
            return float(part)
    elif type(part) is list:
        for i in range(len(part)):
            part[i] = precalculator(part[i])
        return part[0] - sum(part[1:])
    return part


def main():
    mybot = Updater(settings.API_KEY, use_context=True, request_kwargs=PROXY)
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler("planet", astrolog))
    dp.add_handler(CommandHandler("wordcount", wordcount))
    dp.add_handler(CommandHandler("next_full_moon", next_full_moon))
    dp.add_handler(CommandHandler("cities", cities))
    dp.add_handler(CommandHandler("calc", calculator))
    dp.add_handler(MessageHandler(Filters.text, lets_talk))
    logging.info('Bot started')
    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()
