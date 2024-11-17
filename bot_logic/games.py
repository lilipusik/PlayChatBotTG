import json
import bot_logic.helpers as help
from telebot import types

with open("data/cities.json", "r", encoding="utf-8") as f:
    file = json.load(f)
    cities_list = file['city']

used_cities = set()
last_letters = list()
level = None

def register_game_handlers(bot):

    def start(chat_id):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('Игра "Города"', 'Выход')
        bot.send_message(chat_id, 'Выберите действие:', reply_markup=markup)

    def hide_buttons(chat_id):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('Выход')
        return markup

    @bot.message_handler(func=lambda message: message.text == "Играть")
    def start_game(message):
        start(message.chat.id)

    @bot.message_handler(func=lambda message: message.text == 'Игра "Города"')
    def select_level(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('Легкий', 'Средний', 'Сложный', 'Выход')
        bot.send_message(message.chat.id, 'Выберите сложность игры:', reply_markup=markup)

    @bot.message_handler(func=lambda message: message.text in ['Легкий', 'Средний', 'Сложный'])
    def select_cities(message):
        level = message
        if help.who_first_start() == 'Пользователь':
            bot.send_message(message.chat.id, "Игра началась! Назовите город.", reply_markup=hide_buttons(message.chat.id))
        else:
            bot.send_message(message.chat.id, "Игра началась! Я хожу первым.", reply_markup=hide_buttons(message.chat.id))
            bot_city = help.bot_first_respond(cities_list)
            if bot_city:
                used_cities.add(bot_city)
                bot.send_message(message.chat.id, f"Мой город: {bot_city}. Ваш ход!")
            else:
                bot.send_message(message.chat.id, "Вы выиграли!")
        last_letters.clear()
        used_cities.clear()

    @bot.message_handler(func=lambda message: message.text)
    def cities_game(message):
        city = help.extract_city(message.text, [info['name'] for info in cities_list])
        if not city:
            bot.send_message(message.chat.id, "Неверный ввод.")
            return

        if help.is_used_city(city, used_cities):
            bot.send_message(message.chat.id, "Этот город уже использовался в игре.")
            return
        
        if len(last_letters) > 0:
            if not help.is_valid_city(city, last_letters[-1]):
                bot.send_message(message.chat.id, f"Название вашего города должно начинаться на букву {last_letters[-1]}")
                return
        
        used_cities.add(city)
        
        last_letters.append(help.get_last_letter(city))

        bot_city = help.bot_respond(last_letters[-1], cities_list, used_cities, level)

        if bot_city:
            used_cities.add(bot_city)
            last_letters.append(help.get_last_letter(bot_city))
            bot.send_message(message.chat.id, f"Мой город: {bot_city}. Ваш ход!")
        else:
            bot.send_message(message.chat.id, "Я сдаюсь. Вы выиграли!")
            start(message.chat.id)
