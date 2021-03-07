import telebot
import configure
from telebot import types

client = telebot.TeleBot(configure.config['token'])


@client.message_handler(commands=['application'])
def application(message):
    rmk = types.ReplyKeyboardMarkup()
    rmk.add(types.KeyboardButton('Да'), types.KeyboardButton('Нет'))

    msg = client.send_message(message.chat.id,'Желаете подать заявку на модератора проекта?', reply_markup = rmk)
    client.register_next_step_handler(msg, user_answer)


def user_answer(message):
    if message.text == 'Да':
        msg = client.send_message(message.chat.id, 'Впишите ваши даные')
        client.register_next_step_handler(msg, user_reg)
    elif message.text == 'Нет':
        client.send_message(message.chat.id, 'Хорошо! смешнявка!')
    else:
        client.send_message(message.chat.id, 'Ты, что смешнявка?')


def user_reg(message):
    client.send_message(message.chat.id, f'Your data: {message.text}')




@client.message_handler(commands = ['get_info', 'info'])
def get_user_info(message):
    markup_inline = types.InlineKeyboardMarkup()
    item_yes = types.InlineKeyboardButton(text = 'Да', callback_data = 'yes')
    item_no = types.InlineKeyboardButton(text = 'Нет', callback_data = 'No')

    markup_inline.add(item_yes, item_no)
    client.send_message(message.chat.id, 'Желаете узнать небольшую информацию о вас', reply_markup = markup_inline)

    @client.message_handler(content_types=['text'])
    def get_text(message):
        print(message)
        if message.text == 'Мой ID':
            client.send_message(message.chat.id, f'Your ID: {message.from_user.id}')
        elif message.text == 'Мой ник':
            client.send_message(message.chat.id, f'Your ID: {message.from_user.first_name}')


    @client.callback_query_handler(func = lambda call: True)
    def anwswer(call):
        if call.data == 'yes':
            markup_reply = types.ReplyKeyboardMarkup(resize_keyboard = True)
            item_id = types.KeyboardButton('Мой ID')
            item_username = types.KeyboardButton( 'Мой ник' )

            markup_reply.add(item_id, item_username)
            client.send_message(call.message.chat.id, 'Нажмите на одну из кнопок',reply_markup = markup_reply )

        elif call.data == 'no':
           pass


@client.message_handler(content_types = ['text'])
def get_text(message):
    name = message.from_user.first_name

    # print(message.text)

    if message.text.lower() == 'привет':
        client.send_message(message.chat.id, 'Привет! ' + name)

    if message.text.lower() == 'что ты умеeшь?':
        client.send_message(message.chat.id, 'Много чего!😝')

    if message.text == 'Мой ID':
        client.send_message(message.chat.id, f'Your ID: {message.from_user.id}')
    if message.text == 'Мой ник':
        client.send_message(message.chat.id, f'Your ID: {message.from_user.first_name}')


client.polling(none_stop = True, interval = 0)