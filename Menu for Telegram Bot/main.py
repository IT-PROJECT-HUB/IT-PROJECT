from aiogram.types import ReplyKeyboardMarkup, KeyboardButton  # pip install aiogram
from aiogram import Dispatcher, Bot, executor, types
from random import randint, choice
from string import ascii_letters, digits, punctuation

API_TOKEN = "Ваш API ключ"

# инициализация ботика...
bot = Bot(token=API_TOKEN)
dispatcher = Dispatcher(bot)

# Создание клавиатуры
btn_random = KeyboardButton("🎲 Рандомное число")
btn_pass = KeyboardButton('🔐 Придумать пароль')
btn_other = KeyboardButton("🔷 Другое")

main_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_random, btn_pass, btn_other)

btn_info = KeyboardButton('ℹ️ Информация')
btn_main = KeyboardButton('🟡 Главное меню')

other_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_info, btn_main)


@dispatcher.message_handler(commands=['start'])
async def start(message: types.Message):
    await bot.send_message(message.from_user.id, f"👋 Привет, {message.from_user.first_name}!", reply_markup=main_menu)


@dispatcher.message_handler()
async def messages(message: types.Message):
    if message.text == '🎲 Рандомное число':
        await bot.send_message(message.from_user.id, f'🎲 Рандомное число: {randint(0, 100)}')
    elif message.text == '🔐 Придумать пароль':
        password = "".join([choice(str(digits + ascii_letters + punctuation)) for _ in range(24)])
        await bot.send_message(message.from_user.id, f'🔐 Надёжный пароль: {password}')
    elif message.text == '🔷 Другое':
        await bot.send_message(message.from_user.id, '🔷 Открываю...', reply_markup=other_menu)
    elif message.text == 'ℹ️ Информация':
        await bot.send_message(message.from_user.id, f'👽 Ваше имя: {message.from_user.first_name}\n\nБот создан by Neor 👨‍💻')
    elif message.text == '🟡 Главное меню':
        await bot.send_message(message.from_user.id, '🟡 Открываю меню...', reply_markup=main_menu)
    else:
        await bot.send_message(message.from_user.id, f'😐 Ботик вас не понял... :(')


if __name__ == '__main__':
    executor.start_polling(dispatcher, skip_updates=True)
