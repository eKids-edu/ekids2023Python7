from datetime import datetime
import telebot
from settings import BOT_TOKEN


HELLO_WORDS = ["вітаю", "привіт", "hi", "hello", "sava"]
bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=["help"])
def send_help(message):
    print("Обробка команди /help")
    bot.send_message(message.from_user.id, "Список команд, які використовує бот: ")


@bot.message_handler(commands=["start"])
def send_welcome(message):
    print("Обробка команди /start")
    bot.send_message(
        message.from_user.id,
        f"{hello()}! Цей бот вміє працювати зі списком товарів. "
        "Наберіть /help для отримання допомоги"
    )


@bot.message_handler(func=lambda message: message.text.lower() in HELLO_WORDS)
def send_hello(message):
    name = message.from_user.first_name
    print(f"Відповідь на привітання від {name}")
    bot.reply_to(message, f"{hello()}, {name}!")


# Функція відповідей на решту повідомлень
@bot.message_handler(content_types=['text'])
def echo_all(message):
    print(f"Відповідь на {message.text=}")
    bot.send_message(message.from_user.id, message.text)


def hello():
    now = datetime.now()
    if 6 <= now.hour < 12:
        return "Доброго ранку"
    elif 12 <= now.hour < 18:
        return "Добрий день"
    elif 18 <= now.hour < 23:
        return "Доброго вечора"
    else:
        return "Доброї ночі"


print("Бот слухає запити...")
bot.infinity_polling()
