import os
import asyncio
import json
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Update
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
# Токен бота
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Создаем бота и диспетчер
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Создаем меню с кнопками
def get_main_menu():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="?? Контакты"), KeyboardButton(text="?? О нас")],
            [KeyboardButton(text="?? Цены"), KeyboardButton(text="??? Услуги")],
            [KeyboardButton(text="?? Акции"), KeyboardButton(text="?? Записаться")],
            [KeyboardButton(text="?? купить технику Apple")]  # Добавил новую кнопку в меню
        ],
        resize_keyboard=True,  # Кнопки подстраиваются под размер
        one_time_keyboard=False  # Меню остается всегда
    )
    return keyboard


# Команда /start - с меню
@dp.message(Command("start"))
async def start_command(message: types.Message):
    user = message.from_user
    await message.answer(
        f"?? Привет псина, чего мы тут вынюхиваем? Если хочешь ахуевший ремнт трубки, то ты по адресу))) {user.first_name}!\n"
        f"Твой ID: {user.id}\n\n"
        f"Выбери нужный вариант из меню ниже ??",
        reply_markup=get_main_menu()
    )

# Команда /menu - показать меню
@dp.message(Command("menu"))
async def menu_command(message: types.Message):
    await message.answer(
        "?? Главное меню:",
        reply_markup=get_main_menu()
    )

# Команда /help
@dp.message(Command("help"))
async def help_command(message: types.Message):
    await message.answer(
        "?? Команды:\n"
        "/start - приветствие с меню\n"
        "/menu - показать меню\n"
        "/help - помощь\n"
        "/hide - скрыть меню"
    )

# Команда чтобы скрыть меню
@dp.message(Command("hide"))
async def hide_menu(message: types.Message):
    await message.answer(
        "Меню скрыто. Используй /menu чтобы вернуть.",
        reply_markup=types.ReplyKeyboardRemove()
    )

# Обработка нажатий на кнопки меню
@dp.message()
async def handle_menu_buttons(message: types.Message):
    text = message.text
    
    if text == "? Частые вопросы":
        await message.answer(
            "?? <b>Частые вопросы:</b>\n\n"
            "1. Как записаться на ремонт?\n"
            "2. Сколько времени идет диагностика?\n"
            "3. График работы\n"
            "4. Стоимость услуг\n\n"
            "Напиши номер вопроса (1-4)",
            parse_mode="HTML"
        )
    
    elif text == "?? Контакты":
        await message.answer(
            "?? <b>Наши контакты:</b>\n\n"
            "?? Телефон: +7 (999)-451-79-64\n"
            "?? Адрес: Езжай в Сибирский молл\n"
            "?? График: от расцвета до утра\n"
            "Наш сайт : https://asx.sc\n"
            "?? Email: asx.com",
            parse_mode="HTML"
        )
    
    elif text == "?? О нас":
        await message.answer(
            "?? <b>О нашей компании:</b>\n\n"
            "Мы работаем с 2010 года!\n"
            "Более 1000000 довольных клиентов\n"
            "Профессиональная команда, инженеры со стажет 10+ лет\n"
            "Даём гарантию на работу и запчасти",
            parse_mode="HTML"
        )
    
    elif text == "?? Цены":
        await message.answer(
            "?? <b>Наши цены:</b>\n\n"
            "• Диагностика - 0 руб.\n"
            "• Услуги по настройке телефона - от 300 руб.\n"
            "• Ремонт от 2000 руб.\n"
            "• Сложный ремонт (ремонты на материнской плате) от 4900 руб.\n\n"
            "?? Есть скидки постоянным клиентам!",
            parse_mode="HTML"
        )
    
    elif text == "??? Услуги":
        await message.answer(
            "?? <b>Наши услуги:</b>\n\n"
            "1. Диагностика и анализ неисправностей\n"
            "2. Профессиональный ремонт любой техники Apple\n"
            "3. Услуги по настройке телефона ( перенос данных, настройка телефона,  установка приложений)\n\n"
            "Что интересует?",
            parse_mode="HTML"
        )
    
    elif text == "?? Акции":
        await message.answer(
            "?? <b>Текущие акции:</b>\n\n"
            "??  Бесплатная диагностика!\n"
            "?? Приведи друга - скидка 10%\n"
            "?? При комлексном ремонте - скидка 10% на общий чек\n"
            "?? При ремонте - скидка на стекла и аксесуары до 50%\n\n"
            "Акции действуют до конца месяца!",
            parse_mode="HTML"
        )
    
    elif text == "?? Записаться":
        await message.answer(
            "?? <b>Запись на ремонт:</b>\n\n"
            "Для записи укажите:\n"
            "1. Ваше имя\n"
            "2. Желаемую дату\n"
            "3. Услугу\n\n"
            "Или позвоните по номеру: +7 (999) 451-79-64",
            parse_mode="HTML"
        )
    
    elif text == "?? купить технику Apple":
        await message.answer(
            "?? <b>Какая техника у нас есть:</b>\n\n"
            "1. Iphone с 15 до 17 pro max любая модель, с любым объёмом памяти\n"
            "2. Наушники Air pods/ Air pods pro\n"
            "3. Apple Watch\n"
            "4. Mac book / Imac",
            parse_mode="HTML"
        )
        
    else:
        # Если это не кнопка меню, обрабатываем как обычное сообщение
        await message.answer(f"Вы сказали: {message.text} , если я не знаю ответа на ваш вопрос, позвоните по номеру 89994517964")

# Главнвя функция
async def handler(event, context):
    """
    Функция-обработчик для Yandex Cloud Functions
    """
    try:
        # Парсим входящий запрос от Telegram
        if isinstance(event, dict):
            # В Yandex Cloud тело запроса может быть в разных полях
            body = event.get('body', '')
            if isinstance(body, str):
                update_data = json.loads(body)
            else:
                update_data = body
        else:
            update_data = json.loads(event)
        
        # Создаем объект Update из данных
        update = Update(**update_data)
        
        # Передаем обновление диспетчеру
        await dp.feed_update(bot, update)
        
        # Возвращаем успешный ответ
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({'ok': True})
        }
    except Exception as e:
        print(f"Ошибка: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
# залупа тигра
