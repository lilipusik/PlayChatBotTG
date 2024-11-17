from telebot import types

def register_start_handlers(bot):
    @bot.message_handler(commands=['start'])
    def start_command(message):
        bot.send_message(message.chat.id, 'Привет! Как тебя зовут?')
        bot.register_next_step_handler(message, get_name)

    def get_name(message):
        name = message.text
        bot.send_message(message.chat.id, f'Приятно познакомиться, {name}!')
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add('Меню')
        bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)