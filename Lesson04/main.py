from datetime import datetime
import json
import telebot
from settings import BOT_TOKEN


HELLO_WORDS = ["вітаю", "привіт", "hi", "hello", "bonjour"]
GOODS_FILE_NAME = 'goods.json'
GOODS_KEYS = ("name", "price", "description")


def load_goods():
    global GOODS_FILE_NAME
    with open(GOODS_FILE_NAME, "r", encoding="utf8") as f:
        goods_info = json.load(f)
    return goods_info


def save_goods():
    global goods, GOODS_FILE_NAME
    with open(GOODS_FILE_NAME, "w", encoding="utf8") as f:
        json.dump(goods, f, indent=2, ensure_ascii=False)


goods = load_goods()
print(f"Завантажено товари {json.dumps(goods, indent=2, ensure_ascii=False)}")
bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=["help"])
def send_help(message):
    print("Обробка команди /help")
    bot.send_message(
        message.from_user.id,
        "*Список команд, які використовує бот*:\n\n"
        "/add назва,ціна,опис \- додати товар\n"
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
    global goods, GOODS_KEYS
    print(f"Обробка /add від {message.from_user.first_name=}")
    goods_from_command = parse_command_args(message.text)
    if len(goods_from_command) != len(GOODS_KEYS):
        bot.send_message(message.from_user.id, "Хибна кількість аргументів")
        return
    goods_to_add = dict(zip(GOODS_KEYS, goods_from_command))
    goods.append(goods_to_add)
    save_goods()
    bot.send_message(
        message.from_user.id,
        f"Товар '{goods_to_add['name']}' додано до списку"
    )


def parse_command_args(text):
    skip_position = text.find(" ") + 1
    arguments = text[skip_position:].split(",")
    return arguments


@bot.message_handler(commands=["print"])
def print_goods(message):
    global goods
    print(f"Обробка /print від {message.from_user.first_name=}")
    bot.send_message(
        message.from_user.id,
        f"Список товарів: {json.dumps(goods, indent=2, ensure_ascii=False)}"
    )


@bot.message_handler(func=lambda message: message.text.lower() in HELLO_WORDS)
def send_hello(message):
    name = message.from_user.first_name
    print(f"Відповідь на привітання від {name=}")
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