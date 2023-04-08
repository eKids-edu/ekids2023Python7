from datetime import datetime
import json
import telebot
from settings import BOT_TOKEN


HELLO_WORDS = ["вітаю", "привіт", "hi", "hello", "bonjour"]
GOODS_KEYS = ("Назва", "Ціна", "Опис")
GOODS_FILE_NAME = "goods.json"

with open(GOODS_FILE_NAME, "r", encoding="utf8") as saved_goods:
    goods = json.load(saved_goods)
print(
    "Завантажено список товарів:\n"
    f"{json.dumps(goods, indent=2, ensure_ascii=False)}"
)
bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=["help"])
def send_help(message):
    print("Обробка команди /help")
    bot.send_message(
        message.from_user.id,
        "*Список команд, які використовує бот*:\n\n"
        "/add _назва, ціна, опис_ \- додати товар\n"
        "/delete _назва_ \- видалити товар\n"
        "/print \- вивести список товарів",
        parse_mode="MarkdownV2"
    )


@bot.message_handler(commands=["start"])
def send_welcome(message):
    print("Обробка команди /start")
    bot.send_message(
        message.from_user.id,
        f"{hello()}! Цей бот вміє працювати зі списком товарів. "
        "Наберіть /help для отримання допомоги"
    )


@bot.message_handler(commands=["add"])
def add_goods(message):
    global goods, GOODS_KEYS, GOODS_FILE_NAME
    print(f"Обробка команди /add від {message.from_user.first_name}")
    new_article = message.text[message.text.find(" ") + 1:].split(",")
    if len(new_article) != len(GOODS_KEYS):
        bot.send_message(message.from_user.id, "Хибна кількість аргументів")
        return
    for i in range(len(new_article)):
        new_article[i] = " ".join(new_article[i].split())
    try:
        new_article[1] = round(float(new_article[1]), 2)
    except ValueError:
        bot.send_message(message.from_user.id, "Хибна ціна товару")
        return
    for g in goods:
        if new_article[0] == g[GOODS_KEYS[0]]:
            bot.send_message(message.from_user.id, "Товар вже є у списку")
            return
    goods.append(dict(zip(GOODS_KEYS, new_article)))
    with open(GOODS_FILE_NAME, "w", encoding="utf8") as f:
        json.dump(goods, f, indent=2, ensure_ascii=False)
    bot.send_message(
        message.from_user.id,
        f"{goods[-1]}\nдодано до списку товарів"
    )


@bot.message_handler(commands=["print"])
def print_goods(message):
    global goods
    print(f"Обробка команди /print від {message.from_user.first_name}")
    bot.send_message(
        message.from_user.id,
        json.dumps(goods, indent=2, ensure_ascii=False),
    )


@bot.message_handler(commands=["delete"])
def delete_goods(message):
    global goods, GOODS_KEYS, GOODS_FILE_NAME
    print(f"Обробка команди /delete від {message.from_user.first_name}")
    del_article = " ".join(message.text[message.text.find(" ") + 1:].split())
    if del_article == '/delete':
        bot.send_message(message.from_user.id, "Хибна кількість аргументів")
        return
    for i in range(len(goods)):
        if goods[i][GOODS_KEYS[0]] == del_article:
            deleted = goods.pop(i)
            with open(GOODS_FILE_NAME, "w", encoding="utf8") as f:
                json.dump(goods, f, indent=2, ensure_ascii=False)
            bot.send_message(
                message.from_user.id,
                f"{deleted}\nвиключено зі списку товарів"
            )
            return
    bot.send_message(
        message.from_user.id,
        f"'{del_article}' не знайдено у списку товарів"
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
