from datetime import datetime
import json
from telebot import TeleBot
from telebot.types import BotCommand, ReplyKeyboardMarkup, KeyboardButton
from settings import BOT_TOKEN


HELLO_WORDS = ["вітаю", "привіт", "hi", "hello", "bonjour"]
GOODS_KEYS = ("Назва", "Ціна", "Опис", "Кількість")
PRIMARY_KEY = "Назва"
GOODS_FILE_NAME = "goods.json"
MENU = {
    "print": "Вивести список товарів",
    "report": "Звіт по складу",
    "oos": "Звіт по відсутнім товарам",
    "help": "Допомога по командам",
}
BUTTONS = ("🛒 Товари", "📋 Звіт", "❓ Допомога", "📉 Відсутні на складі")

bot = TeleBot(BOT_TOKEN)


@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        f"{hello()}, {message.from_user.first_name}!\n\n"
        "Цей бот вміє працювати зі списком товарів. "
        "Додавати, видаляти, редагувати товари, "
        "змінювати їх кількість на складі, "
        "а також проводити базову аналітику.\n\n"
        "Наберіть /help для отримання допомоги по командам",
        reply_markup=keyboard())


@bot.message_handler(commands=["help"])
def send_help(message):
    bot.send_message(
        message.chat.id,
        "*Список команд, які використовує бот*:\n\n"
        "/add _назва, ціна, опис, кількість_ \- додати товар\n"
        "/delete _назва\\[, назва2, \\.\\.\\.\\]_ \- видалити товар\\[и\\]\n"
        "/price _назва, ціна_ \- редагувати ціну товару\n"
        "/desc _назва, опис_ \- редагувати опис товару\n"
        "/stock _назва, кількість_ \- змінити кількість товару на складі\n"
        "/report \- сумарний звіт по товарам на складі\n"
        "/oos \- звіт по товарам, що відсутні на складі\n"
        "/print \- вивести список товарів",
        reply_markup=keyboard(),
        parse_mode="MarkdownV2")


@bot.message_handler(commands=["add"])
def add_goods(message):
    global goods, GOODS_KEYS
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
    new_article[1] = set_price(new_article[1])
    new_article[3] = set_stock(new_article[3])
    if new_article[1] < 0 or new_article[3] < 0:
        bot.send_message(message.chat.id, "❌ Хибна ціна або кількість товару")
        return
    goods.append(dict(zip(GOODS_KEYS, new_article)))
    save(goods)
    bot.send_message(message.chat.id,
                     f"{pretty_view(goods[-1])}\n✅ додано до списку товарів")


@bot.message_handler(commands=["print"])
def print_goods(message):
    global goods
    bot.send_message(message.chat.id, pretty_view(goods))


@bot.message_handler(commands=["delete"])
def delete_goods(message):
    global goods
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


@bot.message_handler(commands=["price"])
def change_price(message):
    change_key("Ціна", message, set_price)


@bot.message_handler(commands=["stock"])
def change_stock(message):
    change_key("Кількість", message, set_stock)


@bot.message_handler(commands=["desc"])
def change_desc(message):
    change_key("Опис", message)


@bot.message_handler(commands=["report"])
def view_report(message):
    global goods
    bot.send_chat_action(message.chat.id, 'typing')
    total_stock = sum([g["Кількість"] for g in goods])
    total_value = sum([g["Ціна"] * g["Кількість"] for g in goods])
    sorted_goods = sorted([(g["Назва"], g["Ціна"]) for g in goods],
                          key=lambda item: item[1])
    bot.send_message(
        message.chat.id,
        "📋 Всього найменувань товарів:\n"
        f"{len(goods)} од.\n\n"
        "📦 Загальна кількість товарів на складі:\n"
        f"{total_stock} шт.\n\n"
        "🛒 Загальна вартість складу:\n"
        f"{total_value} грн.\n\n"
        "⬆️ Найдорожчий товар:\n"
        f"'{sorted_goods[-1][0]}' за ціною {sorted_goods[-1][1]} грн.\n\n"
        "⬇️ Найдешевший товар:\n'"
        f"{sorted_goods[0][0]}' за ціною {sorted_goods[0][1]} грн.")


@bot.message_handler(commands=["oos"])
def out_of_stock(message):
    global goods
    oos_list = [g for g in goods if not g["Кількість"]]
    if oos_list:
        bot.send_message(
            message.chat.id,
            f"{pretty_view(oos_list)}\n⚠️ Список відсутніх на складі товарів")
    else:
        bot.send_message(message.chat.id, "ℹ️ Всі товари є в наявності")


@bot.message_handler(func=lambda message: message.text.lower() in HELLO_WORDS)
def send_hello(message):
    bot.reply_to(message, f"{hello()}, {message.from_user.first_name}!")


@bot.message_handler(content_types=['text'])
def check_buttons(message):
    global BUTTONS
    if message.text == BUTTONS[0]:
        print_goods(message)
    elif message.text == BUTTONS[1]:
        view_report(message)
    elif message.text == BUTTONS[2]:
        send_help(message)
    elif message.text == BUTTONS[3]:
        out_of_stock(message)
    else:
        bot.send_message(message.chat.id, message.text)


def listener(messages):
    for m in messages:
        if m.content_type == 'text':
            print(f"{m.from_user.first_name} [{m.chat.id=}]: {m.text}")


def keyboard():
    global BUTTONS
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(*(KeyboardButton(b) for b in BUTTONS))
    return markup


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
    global GOODS_FILE_NAME
    try:
        with open(GOODS_FILE_NAME, "r", encoding="utf8") as g:
            loaded_goods = json.load(g)
    except FileNotFoundError:
        print(f"{GOODS_FILE_NAME} не знайдено.")
        loaded_goods = []
    print("Завантажено список товарів:\n"
          f"{pretty_view(loaded_goods)}")
    return loaded_goods


def save(json_obj):
    global GOODS_FILE_NAME
    try:
        with open(GOODS_FILE_NAME, "w", encoding="utf8") as f:
            json.dump(json_obj, f, indent=2, ensure_ascii=False)
        print("Список товарів збережено")
    except IOError as err:
        print(f"Помилка запису {GOODS_FILE_NAME} {err}")


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


def set_price(text_price):
    try:
        return round(float(text_price), 2)
    except ValueError:
        return -1


def set_stock(text_stock):
    try:
        return int(text_stock)
    except ValueError:
        return -1


def change_key(key, message, func=None):
    global goods
    args = parse_command_args(message.text)
    if len(args) != 2:
        bot.send_message(message.chat.id, "❌ Повинно бути два аргументи")
        return
    index = find_goods(args[0])
    if index == -1:
        bot.send_message(
            message.chat.id,
            f"❗️'{args[0]}' не знайдено у списку товарів")
        return
    if func:
        value = func(args[1])
        if isinstance(value, int) and value < 0:
            bot.send_message(message.chat.id,
                             f"❌ Другий аргумент неправильний")
            return
        goods[index][key] = value
    else:
        goods[index][key] = args[1]
    bot.send_message(message.chat.id,
                     f"{pretty_view(goods[index])}\n✅ {key} товару змінено")
    save(goods)


if __name__ == "__main__":
    bot.delete_my_commands()
    bot.set_my_commands([BotCommand(k, v) for k, v in MENU.items()])
    bot.set_update_listener(listener)
    goods = load()
    print("Бот слухає запити...")
    bot.infinity_polling()
