import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from lib import get_types, creation, get_creator_answers, vote, get_vote
import schema.query as queries

TOKEN = "783657766:AAHh0XwRqUoYseLKyxZxhPr-vwhukp9iMCc"

bot = telebot.TeleBot(TOKEN)
users_create_now = dict()
users_vote_now = dict()


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Hello. Make vote")
    if message.chat.username is not None:
        queries.create_user(message.chat.id, message.chat.username)
    else:
        queries.create_user(message.chat.id)


@bot.message_handler(commands=['create'])
def create_create_evote(message):
    users_create_now.pop(message.chat.id, None)
    users_create_now[message.chat.id] = None
    vote_types = get_types()
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    for vote_type in vote_types:
        markup.add(InlineKeyboardButton(vote_type, callback_data="type" + vote_type))
    bot.send_message(message.chat.id, "Select type of electronic voting system:", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: len(call.data) >= 4 and call.data[:4] == "type")
def callback_evote(call):
    if call.message.chat.id in users_create_now and users_create_now[call.message.chat.id] is None:
        vote_type = call.data[4:]
        questions = creation(vote_type)
        users_create_now[call.message.chat.id] = {'type': vote_type, 'question': [i[1] for i in questions], 'question_header': [i[0] for i in questions], 'answer': []}
        bot.send_message(call.message.chat.id, questions[0][1])
        print(users_create_now)


@bot.message_handler(func=lambda message: (message.chat.id in users_create_now and users_create_now[message.chat.id] is not None and users_create_now[message.chat.id].get('answer') is not None))
def ask_and_create_evote(message):
    users_create_now[message.chat.id]['answer'].append(message.text)
    if len(users_create_now[message.chat.id]['answer']) == len(users_create_now[message.chat.id]['question']):
        to_create_answer = [[users_create_now[message.chat.id]['question_header'][i], users_create_now[message.chat.id]['answer'][i]] for i in range(len(users_create_now[message.chat.id]['question_header']))]

        id_of_created_vote = get_creator_answers(message.chat.id, users_create_now[message.chat.id]['type'], to_create_answer)

        if id_of_created_vote < 0:
            bot.send_message(message.chat.id, "ERROR")
        else:
            bot.send_message(message.chat.id, "Voting created with code: " + str(id_of_created_vote))

        users_create_now.pop(message.chat.id, None)
    else:
        bot.send_message(message.chat.id, users_create_now[message.chat.id]['question'][len(users_create_now[message.chat.id]['answer'])])


@bot.message_handler(commands=['vote'])
def print_vote_with_code(message):
    #try:
    code = int(message.text[5:])
    vote_type, (vote_question, vote_answers) = vote(code)
    #except:
    #    bot.send_message(message.chat.id, "after /vote might go code of vote")
    #    return

    users_vote_now.pop(message.chat.id, None)
    users_create_now[message.chat.id] = code

    if vote_type == "choose_one":
        markup = InlineKeyboardMarkup()
        markup.row_width = 1
        send_message = vote_question + '\n'
        index = 0
        for answer in vote_answers:
            index += 1
            send_message += str(index)
            send_message += ") "
            send_message += answer
            send_message += '\n'
            markup.add(InlineKeyboardButton(index, callback_data="vote" + str(index)))

        bot.send_message(message.chat.id, send_message, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: len(call.data) >= 4 and call.data[:4] == "vote" and call.message.chat.id in users_vote_now and users_vote_now[call.message.chat.id] is not None)
def callback_vote_evote(call):
    if users_vote_now[call.message.chat.id] == "choose_one":
        vote_answer = int(call.data[4:])
        if call.message.chat.id in users_vote_now:
            get_vote(call.message.chat.id, users_vote_now[call.message.chat.id], vote_answer)
            bot.send_message(call.message.chat.id, "You vote is really important for us")
            users_vote_now.pop(call.message.chat.id, None)
        else:
            bot.send_message(call.message.chat.id, "ERROR")


bot.polling()
