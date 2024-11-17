from telebot import types

def register_menu_handlers(bot):
    @bot.message_handler(func=lambda message: message.text == 'Меню' or message.text == 'Выход')
    def menu_handler(message):
        if message.text == 'Выход':
            bot.send_message(message.chat.id, 'Вы проиграли! УХАХАХА')
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('Играть')
        bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)