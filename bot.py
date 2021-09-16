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

from datetime import datetime, timedelta
import locale
import logging
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
    print(planet_name)
    planet_name = planet_name.split()
    print(planet_name)
    planet_name = planet_name[1]
    print(planet_name)
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


def main():
    mybot = Updater(settings.API_KEY, use_context=True, request_kwargs=PROXY)
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler("planet", astrolog))
    dp.add_handler(MessageHandler(Filters.text, lets_talk))
    logging.info('Bot started')
    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()
