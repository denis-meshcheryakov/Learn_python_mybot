import logging
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


def main():
    mybot = Updater(settings.API_KEY, use_context=True, request_kwargs=PROXY)
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(MessageHandler(Filters.text, lets_talk))
    logging.info('Bot started')
    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()
