import telebot
from config.settings import TOKEN
from bot_logic.start import register_start_handlers
from bot_logic.menu import register_menu_handlers
from bot_logic.games import register_game_handlers

bot = telebot.TeleBot(TOKEN)

# Регистрация обработчиков
register_start_handlers(bot)
register_menu_handlers(bot)
register_game_handlers(bot)

if __name__ == "__main__":
    print("Бот запущен!")
    bot.polling()
