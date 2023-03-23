# Блок завантажування необхідних модулів
from datetime import datetime
# Модуль для роботи із збереженими змінними оточення
from dotenv import load_dotenv
# Модуль для роботи із змінними оточення
from os import environ
# Модуль для роботи з Телеграм ботами
import telebot

# Встановлюємо збережені зміні оточення
load_dotenv()
# Знаходимо значення змінної оточення BOT_TOKEN
BOT_TOKEN = environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    print("Не знайдено змінну оточення BOT_TOKEN")
    exit(1)
bot = telebot.TeleBot(BOT_TOKEN)


# Функція для обробки команд start та help
@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    print(f"Відповідь на '{message.text}'")
    bot.send_message(message.from_user.id, "Цей бот працює із списком товарів")


# Функція відповідей на повідомлення
@bot.message_handler(content_types=['text'])
def echo_all(message):
    print(f"Відповідь на {message.text=}")
    if message.text.lower() in {"привіт", "hi", "hello"}:
        reply_message = hello()
    else:
        reply_message = message.text
    bot.send_message(message.from_user.id, reply_message)


# Функція відповіді на привітання
def hello():
    now = datetime.now()
    if 6 <= now.hour < 12:
        return "Доброго ранку"
    elif 12 <= now.hour < 18:
        return "Добрий день"
    elif 12 <= now.hour < 23:
        return "Доброго вечора"
    else:
        return "Доброї ночі"


print("Бот слухає запити...")
bot.infinity_polling()
