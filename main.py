import telebot
from telebot import types

# Товары в группах
products = {
    "Квесты Escape from Tarkov": {
        "🥇3 ЧАСА ВЫПОЛНЕНИЯ КВЕСТОВ🥇": 943.48,
        "🥇2 ЧАСА ВЫПОЛНЕНИЯ КВЕСТОВ🥇": 610.49,
        "🥇1 ЧАС ВЫПОЛНЕНИЯ КВЕСТОВ🥇": 332.99,
        "🥼Выполню квест Гренадёр🥼": 721.49,
        "🥼Выполню квест Доктор «Айболит»🥼": 887.98,
        "🥼Выполню квест Стрелок от Бога🥼": 998.98,
        "🥼Выполню квест Проводник🥼": 388.49,
        "🥼Выполню квест Ренегатам тут не место🥼": 443.99,
        "🥼Выполню квест Служба дезинфекции🥼": 499.49
    },
    "Прокачка Escape from Tarkov": {
        "🥇Прокачка 0-20 + Лут + Большие Бонусы🥇": 1665,
        "🥇Прокачка 0-20 + Лут + Большие Бонусы (Без ЗПО)🥇": 2220
    },
    "Рейды Escape from Tarkov": {
        "🥇Репутация у СКУПЩИКА (ЦЕНА ЗА 1 единицу)🥇": 504.07,
        "🥇Репутация у СКУПЩИКА (ЦЕНА ЗА 2 единицы)🥇": 784.11,
        "🥇Репутация у СКУПЩИКА (ЦЕНА ЗА 3 единицы)🥇": 1512,
        "🥇1 РЕЙД НА Лабораторию🥇": 1792,
        "🥇1 РЕЙД НА Берег🥇": 112.02,
        "🥇1 РЕЙД НА Маяк🥇": 112.02,
        "🥇1 РЕЙД НА Развязка🥇": 112.02,
        "🥇1 РЕЙД НА Лес🥇": 112.02,
        "🥇1 РЕЙД НА Резевр🥇": 112.02,
        "🥇1 РЕЙД НА Таможню🥇": 112.02,
        "🥇1 РЕЙД НА Улицы Таркова🥇": 190.43
    },
    "Фарм Escape from Tarkov": {
        "💰ФАРМ 1KK РУБЛЕЙ (БЕЗ ПЕРЕДАЧИ АККАУНТА)💰": 109.98,
        "💰ФАРМ 20KK РУБЛЕЙ (БЕЗ ПЕРЕДАЧИ АККАУНТА)💰": 1650,
        "💰ФАРМ 15KK РУБЛЕЙ (БЕЗ ПЕРЕДАЧИ АККАУНТА)💰": 659.88,
        "💰ФАРМ 10KK РУБЛЕЙ (БЕЗ ПЕРЕДАЧИ АККАУНТА)💰": 494.91,
        "💰ФАРМ 5KK РУБЛЕЙ (БЕЗ ПЕРЕДАЧИ АККАУНТА)💰": 274.95
    }
}

TOKEN = "6493165129:AAEFEhcUmmcUnjKPpHhd2ZiDUhz0kELp_MU"
bot = telebot.TeleBot(TOKEN)

# Функция для отправки товаров в группе
def send_products(chat_id, product_group):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    product_names = []
    for product_name, price in products[product_group].items():
        product_names.append(product_name)
        markup.add(types.KeyboardButton(product_name))
    product_list_text = "\n".join(product_names)
    bot.send_message(chat_id, f"Выберите товар в группе {product_group}:\n{product_list_text}", reply_markup=markup)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    groups = list(products.keys())
    for group in groups:
        markup.add(types.KeyboardButton(group))
    bot.send_message(message.chat.id, "Выберите группу товаров:", reply_markup=markup)

# Обработчик нажатий на кнопки с группами товаров
@bot.message_handler(func=lambda message: message.text in products.keys())
def handle_product_group(message):
    product_group = message.text
    send_products(message.chat.id, product_group)

# Обработчик нажатий на кнопки с названиями товаров
@bot.message_handler(func=lambda message: message.text in [item for sublist in products.values() for item in sublist])
def handle_product(message):
    product_name = message.text
    price = None
    for group, products_in_group in products.items():
        if product_name in products_in_group:
            price = products_in_group[product_name]
            break
    if price is not None:
        bot.send_message(message.chat.id, f"Вы выбрали товар: {product_name}\nЦена: {price}₽\n\n"
                                          f"ТГ для связи: @moraleezz\n\n"
                                          f"Реквизиты для оплаты:\n"
                                          f"Карта Тинькофф: 2200 7007 3254 6519\n\n"
                                          f"Чтобы начать заново, нажмите /start")

# Запуск бота
bot.polling()