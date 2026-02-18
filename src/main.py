from aiogram.types import Update
import os
import asyncio
import json
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import Update
from aiogram.enums import ParseMode

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Токен бота из переменных окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    logger.error("BOT_TOKEN not set in environment variables")
    raise ValueError("BOT_TOKEN environment variable is required")

# Создаем бота и диспетчер
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Создаем меню с кнопками


def get_main_menu():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📞 Контакты"),
             KeyboardButton(text="ℹ️ О нас")],
            [KeyboardButton(text="💰 Цены"), KeyboardButton(text="🛠️ Услуги")],
            [KeyboardButton(text="🎁 Акции"),
             KeyboardButton(text="📝 Записаться")],
            [KeyboardButton(text="🍏 купить технику Apple")]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    return keyboard

# Команда /start


@dp.message(Command("start"))
async def start_command(message: types.Message):
    user = message.from_user
    await message.answer(
        f"👋 Привет, {user.first_name}!\n"
        f"Твой ID: {user.id}\n\n"
        f"Выбери нужный вариант из меню ниже 👇",
        reply_markup=get_main_menu()
    )

# Команда /menu


@dp.message(Command("menu"))
async def menu_command(message: types.Message):
    await message.answer(
        "📋 Главное меню:",
        reply_markup=get_main_menu()
    )

# Команда /help


@dp.message(Command("help"))
async def help_command(message: types.Message):
    await message.answer(
        "🔍 Команды:\n"
        "/start - приветствие с меню\n"
        "/menu - показать меню\n"
        "/help - помощь\n"
        "/hide - скрыть меню"
    )

# Команда /hide


@dp.message(Command("hide"))
async def hide_menu(message: types.Message):
    await message.answer(
        "Меню скрыто. Используй /menu чтобы вернуть.",
        reply_markup=types.ReplyKeyboardRemove()
    )

# Обработка кнопок меню


@dp.message()
async def handle_menu_buttons(message: types.Message):
    text = message.text

    if text == "📞 Контакты":
        await message.answer(
            "📞 <b>Наши контакты:</b>\n\n"
            "📱 Телефон: +7 (999) 451-79-64\n"
            "📍 Адрес: Езжай в Сибирский молл\n"
            "🕒 График: от расцвета до утра\n"
            "🌐 Сайт: https://asx.sc\n"
            "📧 Email: asx.com",
            parse_mode="HTML"
        )

    elif text == "ℹ️ О нас":
        await message.answer(
            "ℹ️ <b>О нашей компании:</b>\n\n"
            "Мы работаем с 2010 года!\n"
            "Более 1000000 довольных клиентов\n"
            "Профессиональная команда, инженеры со стажем 10+ лет\n"
            "Даём гарантию на работу и запчасти",
            parse_mode="HTML"
        )

    elif text == "💰 Цены":
        await message.answer(
            "💰 <b>Наши цены:</b>\n\n"
            "• Диагностика - 0 руб.\n"
            "• Услуги по настройке телефона - от 300 руб.\n"
            "• Ремонт от 2000 руб.\n"
            "• Сложный ремонт от 4900 руб.\n\n"
            "🎁 Есть скидки постоянным клиентам!",
            parse_mode="HTML"
        )

    elif text == "🛠️ Услуги":
        await message.answer(
            "🛠️ <b>Наши услуги:</b>\n\n"
            "1. Диагностика и анализ неисправностей\n"
            "2. Профессиональный ремонт любой техники Apple\n"
            "3. Услуги по настройке телефона (перенос данных, настройка)\n\n"
            "Что интересует?",
            parse_mode="HTML"
        )

    elif text == "🎁 Акции":
        await message.answer(
            "🎁 <b>Текущие акции:</b>\n\n"
            "✅ Бесплатная диагностика!\n"
            "✅ Приведи друга - скидка 10%\n"
            "✅ При комплексном ремонте - скидка 10%\n"
            "✅ Скидка на аксессуары до 50%\n\n"
            "Акции действуют до конца месяца!",
            parse_mode="HTML"
        )

    elif text == "📝 Записаться":
        await message.answer(
            "📝 <b>Запись на ремонт:</b>\n\n"
            "Для записи укажите:\n"
            "1. Ваше имя\n"
            "2. Желаемую дату\n"
            "3. Услугу\n\n"
            "Или позвоните: +7 (999) 451-79-64",
            parse_mode="HTML"
        )

    elif text == "🍏 купить технику Apple":
        await message.answer(
            "🍏 <b>Техника Apple в наличии:</b>\n\n"
            "1. iPhone 15/16/17 Pro Max (любая модель, память)\n"
            "2. AirPods / AirPods Pro\n"
            "3. Apple Watch\n"
            "4. MacBook / iMac",
            parse_mode="HTML"
        )

    else:
        await message.answer(
            f"Вы сказали: {message.text}\n\n"
            f"Если я не знаю ответа на ваш вопрос, позвоните: +7 (999) 451-79-64"
        )

# ОСНОВНАЯ ФУНКЦИЯ ДЛЯ YANDEX CLOUD


async def handler(event, context):
    """
    Функция-обработчик для Yandex Cloud Functions
    Документация: https://cloud.yandex.com/docs/functions/concepts/function-invoke
    """
    try:
        logger.info(f"Received event: {json.dumps(event)[:200]}...")

        # Извлекаем тело запроса в зависимости от типа события
        if isinstance(event, dict):
            # Проверяем, есть ли httpMethod (это API Gateway запрос)
            if 'httpMethod' in event:
                # Запрос через API Gateway
                body = event.get('body', '')
                if event.get('isBase64Encoded', False):
                    import base64
                    body = base64.b64decode(body).decode('utf-8')
            else:
                # Прямой вызов функции
                body = event.get('body', event)
        else:
            body = event

        # Парсим JSON
        if isinstance(body, str):
            update_data = json.loads(body)
        else:
            update_data = body

        logger.info(f"Parsed update data: {json.dumps(update_data)[:200]}...")

        # Создаем объект Update с помощью model_validate (aiogram 3.x)
        update = Update.model_validate(update_data)

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
        logger.error(f"Error processing update: {e}", exc_info=True)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

# Для локального тестирования (не используется в облаке)
if __name__ == "__main__":
    async def test():
        await dp.start_polling(bot)

    asyncio.run(test())
