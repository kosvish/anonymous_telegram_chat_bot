import config
import telebot
from telebot import types
from database import Database

db = Database('db.db')

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Поиск собеседника')
    markup.add(item1)

    bot.send_message(
        message.chat.id,
        'Привет, {0.first_name}! Добро пожаловать в анонимный чат! Нажми на кнопку поиск собеседника'.format(
            message.from_user),
        reply_markup=markup)


@bot.message_handler(commands=['menu'])
def menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Поиск собеседника')
    markup.add(item1)

    bot.send_message(message.chat.id, 'Меню'.format(message.from_user), reply_markup=markup)


@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.chat.type == 'private':
        if message.text == 'Поиск собеседника':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('Остановить поиск')
            markup.add(item1)

            db.add_queue(message.chat.id)

            bot.send_message(message.chat.id, 'Поиск собеседника...', reply_markup=markup)

        elif message.text == 'Остановить поиск':
            db.delete_queue(message.chat.id)
            bot.send_message(message.chat.id, 'Поиск остановлен, напишите /menu')


bot.polling(none_stop=True)
