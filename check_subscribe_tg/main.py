from aiogram import Bot, Dispatcher, executor, types

TOKEN = "YOUR TOKEN"
CHANNEL_ID = "YOUR CHANNEL ID"

bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot)


@dispatcher.message_handler(commands=['start'])
async def start(message: types.Message):
    user_channel_status = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=message.from_user.id)

    if user_channel_status['status'] != 'left':
        await bot.send_message(message.from_user.id, "Спасибо за подписку на канал!")
    else:
        button = types.InlineKeyboardButton("Я подписался", callback_data="Я подписался")
        markup = types.InlineKeyboardMarkup(row_width=1).add(button)

        await bot.send_message(message.from_user.id, "Сначала подпишись на канал!", reply_markup=markup)


@dispatcher.callback_query_handler(lambda call: True)
async def callback(call: types.CallbackQuery):
    if call.message:
        user_channel_status = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=call.from_user.id)

        if user_channel_status["status"] != "left":
            await bot.send_message(call.from_user.id, "Спасибо за подписку!")
        else:
            await bot.send_message(call.from_user.id, "Вы не подписались :(")


if __name__ == '__main__':
    executor.start_polling(dispatcher)
