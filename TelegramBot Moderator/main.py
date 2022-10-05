from aiogram import Bot, Dispatcher, executor, types
from database import Database
from config import API_TOKEN, ADMIN_ID

bot = Bot(token=API_TOKEN)
dispatcher = Dispatcher(bot)

database = Database("database.db")

censure = []
with open("censure.txt", "r", encoding="utf8") as file:
    for word in file:
        censure.append("".join(word.split()))


@dispatcher.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("👋 Привет! Я плохой ботик, который будет всех банить :)")


@dispatcher.message_handler(commands=['get_id'])
async def get_id(message: types.Message):
    await message.answer(message.from_user.id)


@dispatcher.message_handler(commands=['kick'])
async def kick(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        if not message.reply_to_message:
            await message.answer("😖 Команда должна быть отправлена ответом на сообщение")
            return
        await message.bot.kick_chat_member(message.chat.id, message.reply_to_message.from_user.id)
        await message.answer(f"✅ Пользователь @{message.reply_to_message.from_user.username} исключён из беседы.")
        await message.delete()


@dispatcher.message_handler(commands=['ban'])
async def kick(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        if not message.reply_to_message:
            await message.answer("😖 Команда должна быть отправлена ответом на сообщение")
            return
        await message.bot.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
        await message.answer(f"✅ Пользователь @{message.reply_to_message.from_user.username} заблокирован в беседе.")
        await message.delete()


@dispatcher.message_handler(commands=['unban'])
async def unban(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        if not message.reply_to_message:
            await message.answer("😖 Команда должна быть отправлена ответом на сообщение")
            return
        await message.bot.unban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
        await message.answer(f"✅ Пользователь @{message.reply_to_message.from_user.username} разбанен в беседе.")
        await message.delete()


@dispatcher.message_handler(commands=['mute'])
async def mute(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        if not message.reply_to_message:
            await message.answer("😖 Команда должна быть отправлена ответом на сообщение")
            return
        if len(message.text) < 6:
            await message.answer("❓ Для того чтобы замутить пользователя нужно ввести время в секундах, пример: /mute 60")
            return
        mute_time = int(message.text[6:])
        database.add_mute(user_id=message.reply_to_message.from_user.id, mute_time=mute_time)
        await message.delete()
        await message.reply_to_message.reply(f"🤐 Пользователь @{message.reply_to_message.from_user.username} замучен на {mute_time} секунд!")


@dispatcher.message_handler(content_types=['new_chat_members'])
async def new_user_in_chat(message: types.Message):
    await message.delete()
    # await message.answer(f"Привет, {message.from_user.first_name}!")


@dispatcher.message_handler(content_types=['left_chat_member'])
async def user_left_from_chat(message: types.Message):
    await message.delete()


@dispatcher.message_handler()
async def delete_censure(message: types.Message):
    message_list = message.text.lower().split()
    for user_message in message_list:
        if user_message in censure:
            await message.delete()
            await message.answer("😡 Ай-яй-яй, материться не хорошо :)")
            break

    if not database.examination(message.from_user.id):
        database.add(message.from_user.id)
    if not database.mute(message.from_user.id):
        pass
    else:
        await message.delete()


if __name__ == '__main__':
    executor.start_polling(dispatcher)
