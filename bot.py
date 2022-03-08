import telebot
from Parsing_anime import *

try:
    with open("config", mode="r") as f:
        token = f.readline()
except EOFError:
    print('Не найден токен в конфиге')
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.from_user.id, 'Привет')


@bot.message_handler(commands=['check'])
def decode(message):
    m = message.text
    n = str(m[7:])
    bot.reply_to(message, f"Поиск аниме, которое смотрит пользователь {n}")
    info = check_anime(nickname=n)
    if info:
        bot.send_message(message.from_user.id, info)
    else:
        bot.send_message(message.from_user.id, "Я не нашла этого пользователя")


@bot.message_handler(commands=['list'])
def decode(message):
    m = message.text
    n = str(m).split()
    try:
        nickname = n[1]
        bot.reply_to(message, f"Поиск аниме, которое уже просмотрел пользователь {n[1]}")
        info = list_anime(n[1])
        try:
            temp = n[2]
        except IndexError:
            temp = len(info)
        if int(temp) > len(info):
            bot.send_message(message.from_user.id, f"Будет выведено 20 аниме")
            for i in range(len(info)):
                bot.send_message(message.from_user.id, f"{info[i]['name']},\nОценка {info[i]['rate']}")

        else:
            for i in range(int(temp)):
                bot.send_message(message.from_user.id, f"{info[i]['name']},\nОценка {info[i]['rate']}")
    except IndexError:
        bot.reply_to(message, f"Неверно указан пользователь")


@bot.message_handler(commands=['season'])
def decode(message):
    bot.send_message(message.from_user.id, "Вывод аниме данного сезона")
    bot.send_message(message.from_user.id, season_anime())


@bot.message_handler(commands=['best'])
def decode(message):
    bot.send_message(message.from_user.id, "Вывод аниме с наибольшим рейтингом")
    bot.send_message(message.from_user.id, best_anime())


@bot.message_handler(commands=['update'])
def decode(message):
    bot.send_message(message.from_user.id, "Вывод недавно обновленного аниме")
    bot.send_message(message.from_user.id, update_anime())


@bot.message_handler(commands=['popular'])
def decode(message):
    try:
        m = message.text.split()[1]
    except IndexError:
        m = 3
    bot.send_message(message.from_user.id, "Вывод самого популярного аниме")
    bot.send_message(message.from_user.id, 'Это может занять какое-нибудь время...')
    bot.send_message(message.from_user.id, popular_anime(int(m)))


@bot.message_handler(commands=['random'])
def decode(message):
    bot.send_message(message.from_user.id, "Случайное аниме")
    bot.send_message(message.from_user.id, random_anime())


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Привет":
        bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
    elif message.text == "help" or message.text == "/help":
        bot.send_message(message.from_user.id, '/check + \'никнейм\' - текущее аниме\n'
                                               '/list + \'никнейм\' + \'кол-во записей\' - просмотренное аниме\n'
                                               '/random - вывод случайного аниме\n'
                                               '/season - вывод аниме сезона\n'
                                               '/popular + \'число(длительность поиска, не рекомендуется выставлять '
                                               'больше 5 - будет обрабатываться больше минуты, по умолчанию - 3)\' - '
                                               'вывод самого популярного аниме\n '
                                               '/update - вывод обновленного аниме\n'
                                               '/best - вывод аниме с наилучшим рейтингом')
    elif message.text == "Инфо Хозяин":
        bot.send_message(message.from_user.id, "Секунду")
        info = "\n".join(check_anime(nickname='Notsliw'))
        bot.send_message(message.from_user.id, info)
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши help.")


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, message.text)


bot.polling(none_stop=True)
