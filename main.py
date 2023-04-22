from datetime import datetime
import json
import telebot
from settings import BOT_TOKEN


HELLO_WORDS = ["вітаю", "привіт", "hi", "hello", "bonjour"]
GOODS_KEYS = ("Назва", "Ціна", "Опис", "Кількість")
PRIMARY_KEY = "Назва"
GOODS_FILE_NAME = "goods.json"

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=["help"])
def send_help(message):
    print(f"Обробка команди /help від {message.from_user.first_name}")
    bot.send_message(
        message.chat.id,
        "*Список команд, які використовує бот*:\n\n"
        "/add _назва, ціна, опис, кількість_ \- додати товар\n"
        "/delete _назва\\[, назва2, \\.\\.\\.\\]_ \- видалити товар\\[и\\]\n"
        "/print \- вивести список товарів",
        parse_mode="MarkdownV2")


@bot.message_handler(commands=["start"])
def send_welcome(message):
    print(f"Обробка команди /start від {message.from_user.first_name}")
    bot.send_message(
        message.chat.id,
        f"{hello()}, {message.from_user.first_name}!\n"
        "Цей бот вміє працювати зі списком товарів. "
        "Додавати та видаляти товари. "
        "Наберіть /help для отримання допомоги по командам")


@bot.message_handler(commands=["add"])
def add_goods(message):
    global goods
    print(f"Обробка команди /add від {message.from_user.first_name}")
    new_article = parse_command_args(message.text)
    if len(new_article) != len(GOODS_KEYS):
        bot.send_message(message.chat.id,
                         f"❌️ Аргументів повинно бути {len(GOODS_KEYS)}")
        return
    index = find_goods(new_article[0])
    if index != -1:
        bot.send_message(message.chat.id,
                         f"{pretty_view(goods[index])}\n❗вже є у списку")
        return
    try:
        new_article[1] = round(float(new_article[1]), 2)
    except ValueError:
        bot.send_message(message.chat.id, "❌ Хибна ціна товару")
        return
    goods.append(dict(zip(GOODS_KEYS, new_article)))
    save(goods)
    bot.send_message(
        message.chat.id,
        f"{pretty_view(goods[-1])}\n✅ додано до списку товарів"
    )


@bot.message_handler(commands=["print"])
def print_goods(message):
    global goods
    print(f"Обробка команди /print від {message.from_user.first_name}")
    bot.send_message(message.chat.id, pretty_view(goods))


@bot.message_handler(commands=["delete"])
def delete_goods(message):
    global goods
    print(f"Обробка команди /delete від {message.from_user.first_name}")
    names = parse_command_args(message.text)
    if not names:
        bot.send_message(message.chat.id, "❌ Потрібен хоча б один товар")
        return
    for name in names:
        index = find_goods(name)
        if index == -1:
            bot.send_message(message.chat.id,
                             f"❗️'{name}' не знайдено у списку товарів")
        else:
            bot.send_message(
                message.chat.id,
                f"{pretty_view(goods.pop(index))}\n"
                "❎ видалено зі списку товарів")
    save(goods)


@bot.message_handler(func=lambda message: message.text.lower() in HELLO_WORDS)
def send_hello(message):
    name = message.from_user.first_name
    print(f"Відповідь на привітання від {name}")
    bot.reply_to(message, f"{hello()}, {name}!")


@bot.message_handler(content_types=['text'])
def echo_all(message):
    print(f"Луна на {message.text=} від {message.from_user.first_name}")
    bot.send_message(message.chat.id, message.text)


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


def load():
    with open(GOODS_FILE_NAME, "r", encoding="utf8") as saved_goods:
        loaded_goods = json.load(saved_goods)
    print(f"Завантажено список товарів:\n{pretty_view(loaded_goods)}")
    return loaded_goods


def save(json_obj):
    with open(GOODS_FILE_NAME, "w", encoding="utf8") as f:
        json.dump(json_obj, f, indent=2, ensure_ascii=False)
    print("Збережено список товарів")


def pretty_view(json_obj):
    return json.dumps(json_obj, indent=2, ensure_ascii=False)


def parse_command_args(text):
    args = skip_command_and_split(text, ",")
    if args[0][0] == "/":
        args.pop(0)
    for i in range(len(args)):
        args[i] = delete_spaces(args[i])
    return args


def skip_command_and_split(text, split_symbol):
    return text.strip()[text.find(" ") + 1:].split(split_symbol)


def delete_spaces(text):
    return " ".join(text.split())


def find_goods(name):
    global goods, PRIMARY_KEY
    for i in range(len(goods)):
        if goods[i][PRIMARY_KEY] == name:
            return i
    return -1


if __name__ == "__main__":
    goods = load()
    print("Бот слухає запити...")
    bot.infinity_polling()
