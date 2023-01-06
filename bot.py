import config
import telebot
from telebot import types
from database import Database

db = Database('db.db')

bot = telebot.TeleBot(config.TOKEN)


def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Поиск собеседника')
    markup.add(item1)
    return markup


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Я Парень')
    item2 = types.KeyboardButton('Я Девушка')
    markup.add(item1, item2)

    bot.send_message(
        message.chat.id,
        'Привет, {0.first_name}! Добро пожаловать в анонимный чат! Укажи свой пол!'.format(
            message.from_user),
        reply_markup=markup)


@bot.message_handler(commands=['menu'])
def menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Поиск собеседника')
    markup.add(item1)

    bot.send_message(message.chat.id, 'Меню'.format(message.from_user), reply_markup=markup)


@bot.message_handler(commands=['stop'])
def stop(message):
    chat_info = db.get_active_chat(message.chat.id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if chat_info:
        db.delete_chat(chat_info[0])
        item1 = types.KeyboardButton('Поиск собеседника')
        markup.add(item1)

        bot.send_message(chat_info[1], 'Собеседник вышел из чата', reply_markup=markup)
        bot.send_message(message.chat.id, 'Вы вышли из чата', reply_markup=markup)

    else:
        bot.send_message(message.chat.id, 'Вы не начали чат!', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.chat.type == 'private':
        if message.text == 'Поиск собеседника':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('Остановить поиск')
            markup.add(item1)

            chat_two = db.get_chat()  # получаем собеседника, который стоит в очереди первым

            if not db.create_chat(message.chat.id, chat_two):
                db.add_queue(message.chat.id)
                bot.send_message(message.chat.id, 'Поиск собеседника...', reply_markup=markup)
            else:
                mess = 'Собеседник найден! Чтобы остановить диалог, напишите /stop'
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1 = types.KeyboardButton('/stop')
                markup.add(item1)

                bot.send_message(message.chat.id, mess, reply_markup=markup)
                bot.send_message(chat_two, mess, reply_markup=markup)

        elif message.text == 'Остановить поиск':
            db.delete_queue(message.chat.id)
            bot.send_message(message.chat.id, 'Поиск остановлен, напишите /menu')

        elif message.text == 'Я Парень':
            if db.set_gender(message.chat.id, 'male'):
                bot.send_message(message.chat.id, 'Ваш пол успешно добавлен!', reply_markup=main_menu())
            else:
                bot.send_message(message.chat.id, 'Вы уже указали свой пол!')

        elif message.text == 'Я Девушка':
            if db.set_gender(message.chat.id, 'female'):
                bot.send_message(message.chat.id, 'Ваш пол успешно добавлен!', reply_markup=main_menu())
            else:
                bot.send_message(message.chat.id, 'Вы уже указали свой пол!')

        else:
            chat_info = db.get_active_chat(message.chat.id)
            bot.send_message(chat_info[1], message.text)


bot.polling(none_stop=True)
