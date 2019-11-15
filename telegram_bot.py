import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from lib import get_types, creation, get_creator_answers
import json

TOKEN = "783657766:AAHh0XwRqUoYseLKyxZxhPr-vwhukp9iMCc"

bot = telebot.TeleBot(TOKEN)
users_create_now = dict()


@bot.message_handler(commands=['start'])
def start(message):
    print("Hello. Make vote")
    #TODO: Add user with message.chat.id id


@bot.message_handler(commands=['create'])
def create_evote(message):
    users_create_now.pop(message.chat.id, None)
    users_create_now[message.chat.id] = None
    voit_types = get_types()
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    for voit_type in voit_types:
        markup.add(InlineKeyboardButton(voit_type, callback_data="type" + voit_type))
    bot.send_message(message.chat.id, "Select type of electronic voting system:", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: len(call.data) >= 4 and call.data[:4] == "type")
def callback_evote(call):
    if call.message.chat.id in users_create_now and users_create_now[call.message.chat.id] is None:
        vote_type = call.data[4:]
        questions = creation(vote_type)
        users_create_now[call.message.chat.id] = {'type': vote_type, 'question': [i[1] for i in questions], 'question_header': [i[0] for i in questions], 'answer': []}
        bot.send_message(call.message.chat.id, questions[0][1])
        print(users_create_now)


@bot.message_handler(func=lambda message: message.chat.id in users_create_now)
def ask_and_create_evote(message):
    users_create_now[message.chat.id]['answer'].append(message.text)
    if len(users_create_now[message.chat.id]['answer']) == len(users_create_now[message.chat.id]['question']):
        to_create_answer = [{users_create_now[message.chat.id]['question_header'][i]: users_create_now[message.chat.id]['answer'][i]} for i in range(len(users_create_now[message.chat.id]['question_header']))]

        if get_creator_answers(message.chat.id, users_create_now[message.chat.id]['type'], to_create_answer):
            bot.send_message(message.chat.id, "Voting created")
        else:
            bot.send_message(message.chat.id, "ERROR")
    else:
        bot.send_message(message.chat.id, users_create_now[message.chat.id]['question'][len(users_create_now[message.chat.id]['answer'])])


bot.polling()
