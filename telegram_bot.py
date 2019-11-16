import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from lib import get_types, creation, get_creator_answers, vote, get_vote
from statlib import stats
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

    if message.chat.type != "private":
        bot.send_message(message.chat.id, "Please, vote in private chat with bot")
        return

    users_vote_now.pop(message.chat.id, None)
    users_create_now.pop(message.chat.id, None)
    vote_types = get_types()
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    for vote_type in vote_types:
        markup.add(InlineKeyboardButton(vote_type, callback_data="type" + vote_type))
    users_create_now[message.chat.id] = {'type_message': bot.send_message(message.chat.id, "Select type of electronic voting system:", reply_markup=markup)}


@bot.message_handler(commands=['get_statistic'])
def get_statistic(message):
    try:
        print(message.text[14:])
        code = int(message.text[14:])
    except:
        bot.reply_to(message, "Incorrect command's arguments")
        return

    print(message)

    if not queries.is_owner(code, message.chat.id):
        bot.reply_to(message, "vote doesn't exist or you aren't creater")
        return

    stats(code)
    bot.send_photo(message.chat.id, open('hists/hist' + str(code) + '.png', 'rb'))


@bot.callback_query_handler(func=lambda call: len(call.data) >= 4 and call.data[:4] == "type" and call.message.chat.id in users_create_now)
def callback_evote(call):
    vote_type = call.data[4:]
    bot.edit_message_text("Your choice: " + vote_type, chat_id=call.message.chat.id, message_id=users_create_now[call.message.chat.id]['type_message'].message_id)
    questions = creation(vote_type)
    users_create_now[call.message.chat.id] = {'type': vote_type, 'question': [i[1] for i in questions], 'question_header': [i[0] for i in questions], 'answer': []}
    bot.send_message(call.message.chat.id, questions[0][1])


@bot.message_handler(commands=['vote'])
def print_vote_with_code(message):

    if message.chat.type != "private":
        bot.send_message(message.chat.id, "Please, vote in private chat with bot")
        return

    users_create_now.pop(message.chat.id, None)
    users_vote_now.pop(message.chat.id, None)

    try:
        code = int(message.text[5:])
        vote_type, vote_params = vote(code)
    except:
        bot.send_message(message.chat.id, "after /vote should be correct code of vote")
        return

    if not queries.has_user_access(message.chat.id, code):
        bot.send_message(message.chat.id, "You don't have access or vote doesn't exist")
        return

    if queries.has_user_voted(message.chat.id, code):
        bot.send_message(message.chat.id, "You have already voted")
        return

    if vote_type == "choose_one" or vote_type == "choose_many":
        vote_question, vote_answers = vote_params
        users_vote_now[message.chat.id] = {'type': vote_type, 'code': code, 'vote_question': vote_question, 'vote_answer': vote_answers}
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

        if vote_type == "choose_many":
            markup.add(InlineKeyboardButton("SUBMIT", callback_data="SUBMIT"))
            users_vote_now[message.chat.id]['chosed_button'] = [False for _ in range(index)]

        users_vote_now[message.chat.id]['message_sended'] = bot.send_message(message.chat.id, send_message,
                                                                             reply_markup=markup)
    elif vote_type == "choose_prioritets" or vote_type == "choose_by_prioritets":
        if vote_type == "choose_prioritets":
            vote_question, vote_answers, vote_power = vote_params
            users_vote_now[message.chat.id] = {'type': vote_type, 'code': code, 'vote_question': vote_question,
                                               'vote_answer': vote_answers, 'vote_power': vote_power}
        elif vote_type == "choose_by_prioritets":
            vote_question, vote_answers = vote_params
            users_vote_now[message.chat.id] = {'type': vote_type, 'code': code, 'vote_question': vote_question,
                                               'vote_answer': vote_answers}

        send_message = vote_question + '\n'
        index = 0
        for answer in vote_answers:
            index += 1
            send_message += str(index)
            send_message += ") "
            send_message += answer
            send_message += '\n'
        if vote_type == "choose_prioritets":
            send_message += "Please, write list of " + str(index) + " non-negative integer splited by comma, which mean priority of each variant\n"
        elif vote_type == "choose_by_prioritets":
            send_message += "Please, write list of transposition numbers from 1 to " + str(index) + " , which mean priority of each variant\n"
        bot.send_message(message.chat.id, send_message)
    elif vote_type == "laws":
        vote_statement = vote_params
        users_vote_now[message.chat.id] = {'type': vote_type, 'code': code, 'vote_statement': vote_statement}

        send_message = "Are you agree with the statement:\n " + vote_statement + "?"
        markup = InlineKeyboardMarkup()
        markup.row_width = 1
        markup.add(InlineKeyboardButton("For", callback_data="voteFor"))
        markup.add(InlineKeyboardButton("Abstained", callback_data="voteAbstained"))
        markup.add(InlineKeyboardButton("Against", callback_data="voteAgainst"))

        users_vote_now[message.chat.id]['message_sended'] = bot.send_message(message.chat.id, send_message, reply_markup=markup)


@bot.message_handler(func=lambda message: message.chat.id in users_create_now and users_create_now[message.chat.id] is not None and users_create_now[message.chat.id].get('answer') is not None)
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

@bot.callback_query_handler(func=lambda call: len(call.data) >= 4 and call.data[:4] == "vote" and call.message.chat.id in users_vote_now and users_vote_now[call.message.chat.id] is not None)
def callback_vote_evote(call):
    if users_vote_now[call.message.chat.id]['type'] == "choose_one":
        vote_answer = int(call.data[4:])
        get_vote(call.message.chat.id, users_vote_now[call.message.chat.id]['code'], vote_answer)
        bot.edit_message_text(users_vote_now[call.message.chat.id]['vote_question'] + "\nYour choice: " + users_vote_now[call.message.chat.id]['vote_answer'][vote_answer - 1], chat_id=call.message.chat.id, message_id=users_vote_now[call.message.chat.id]['message_sended'].message_id)
        bot.send_message(call.message.chat.id, "Your vote is really important for us")
        users_vote_now.pop(call.message.chat.id, None)
    elif users_vote_now[call.message.chat.id]['type'] == "choose_many":
        vote_answer = int(call.data[4:])
        users_vote_now[call.message.chat.id]['chosed_button'][vote_answer - 1] = not users_vote_now[call.message.chat.id]['chosed_button'][vote_answer - 1]

        markup = InlineKeyboardMarkup()
        markup.row_width = 1
        send_message = users_vote_now[call.message.chat.id]['vote_question'] + '\n'
        index = 0
        for answer in users_vote_now[call.message.chat.id]['vote_answer']:
            send_message += str(index + 1)
            send_message += ") "
            send_message += answer
            if users_vote_now[call.message.chat.id]['chosed_button'][index]:
                send_message += " ✓"
            send_message += '\n'
            markup.add(InlineKeyboardButton(str(index + 1) + (" ✓" if users_vote_now[call.message.chat.id]['chosed_button'][index] else ""), callback_data="vote" + str(index + 1)))
            index += 1

        markup.add(InlineKeyboardButton("SUBMIT", callback_data="SUBMIT"))

        bot.edit_message_text(send_message, chat_id=call.message.chat.id, message_id=users_vote_now[call.message.chat.id]['message_sended'].message_id, reply_markup=markup)
    elif users_vote_now[call.message.chat.id]['type'] == "laws":
        vote_answer = call.data[4:]

        bot.edit_message_text(users_vote_now[call.message.chat.id]['message_sended'].text + "\n Your choice: " + vote_answer, chat_id=call.message.chat.id,
                              message_id=users_vote_now[call.message.chat.id]['message_sended'].message_id)

        get_vote(call.message.chat.id, users_vote_now[call.message.chat.id]['code'], vote_answer)

        users_vote_now.pop(call.message.chat.id, None)


@bot.message_handler(func=lambda message: message.chat.id in users_vote_now and 'type' in users_vote_now[message.chat.id])
def voting_in_evote(message):
    if users_vote_now[message.chat.id]['type'] == "choose_prioritets":
        vote_answer = message.text
        try:
            vote_answer = [int(i) for i in vote_answer.split(',')]
            if len(vote_answer) != len(users_vote_now[message.chat.id]['vote_answer']):
                raise ValueError("Incorrect number of element")
            sum_of_answer = 0
            for i in vote_answer:
                if i < 0:
                    raise ValueError("Negative number")
                sum_of_answer += i
            if sum_of_answer > users_vote_now[message.chat.id]['vote_power']:
                raise ValueError("Sum more than power")
        except:
            bot.reply_to(message, "Incorrect array")
            return

        bot.send_message(message.chat.id, "Your vote is really important for us")

        get_vote(message.chat.id, users_vote_now[message.chat.id]['code'], vote_answer)
        users_vote_now.pop(message.chat.id, None)

    elif users_vote_now[message.chat.id]['type'] == "choose_by_prioritets":
        vote_answer = message.text
        try:
            vote_answer = [int(i) for i in vote_answer.split(',')]
            len_of_answer = len(users_vote_now[message.chat.id]['vote_answer'])
            if sorted(vote_answer) != [i for i in range(1, len_of_answer + 1)]:
                raise ValueError("Incorrect elements")
        except:
            bot.reply_to(message, "Incorrect array")
            return

        bot.send_message(message.chat.id, "Your vote is really important for us")

        get_vote(message.chat.id, users_vote_now[message.chat.id]['code'], vote_answer)
        users_vote_now.pop(message.chat.id, None)


@bot.callback_query_handler(func=lambda call: call.data == "SUBMIT")
def submit_vote(call):
    if users_vote_now[call.message.chat.id]['type'] == "choose_many":
        list_of_answer = []
        for i in range(len(users_vote_now[call.message.chat.id]['vote_answer'])):
            if users_vote_now[call.message.chat.id]['chosed_button'][i]:
                list_of_answer.append(users_vote_now[call.message.chat.id]['vote_answer'][i])
        bot.edit_message_text(users_vote_now[call.message.chat.id]['vote_question'] + '\n' + "Your choise: " + ' '.join(list_of_answer), chat_id=call.message.chat.id,
                              message_id=users_vote_now[call.message.chat.id]['message_sended'].message_id)
        get_vote(call.message.chat.id, users_vote_now[call.message.chat.id]['code'], list_of_answer)
        users_vote_now.pop(call.message.chat.id, None)


bot.polling()
