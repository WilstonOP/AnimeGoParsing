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
    bot.reply_to(message, message.text.strip('/start'))
    bot.send_message(message.from_user.id, 'Привет, ')


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
    bot.reply_to(message, f"Поиск аниме, которое уже просмотрел пользователь {n[1]}")
    info = list_anime(n[1])
    try:
        temp = n[2]
    except IndexError:
        temp = len(info)
    if int(temp) > len(info):
        bot.send_message(message.from_user.id, f"Вы указали большее кол-во, чем есть, будет выведено всё")
        for i in range(len(info)):
            bot.send_message(message.from_user.id, f"{info[i]['name']},\nОценка {info[i]['rate']}")

    else:
        for i in range(int(temp)):
            bot.send_message(message.from_user.id, f"{info[i]['name']},\nОценка {info[i]['rate']}")


@bot.message_handler(commands=['best'])
def decode(message):
    bot.send_message(message.from_user.id, best_anime())


@bot.message_handler(commands=['update'])
def decode(message):
    bot.send_message(message.from_user.id, update_anime())


@bot.message_handler(commands=['popular'])
def decode(message):
    try:
        m = message.text.split()[1]
    except IndexError:
        m = 3

    bot.send_message(message.from_user.id, 'Это может занять какое-нибудь время...')
    bot.send_message(message.from_user.id, popular_anime(int(m)))


@bot.message_handler(commands=['random'])
def decode(message):
    bot.send_message(message.from_user.id, random_anime())


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Привет":
        bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
    elif message.text == "help":
        bot.send_message(message.from_user.id, "</check + 'Ваш никнейм'> - текущее аниме\n"
                                               "</list + 'Ваш никнейм' + 'Кол-во записей' - просмотренное аниме")
    elif message.text == "Инфо Хозяин":
        bot.send_message(message.from_user.id, "Секунду")
        info = "\n".join(check_anime(nickname='Notsliw'))
        bot.send_message(message.from_user.id, info)
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши help.")

    # while True:
    # time.sleep(20)
    # bot.send_message(message.chat.id, "20 сек")
    # bot.send_message(message.chat.id, loop_new_check())


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, message.text)


bot.polling(none_stop=True)
