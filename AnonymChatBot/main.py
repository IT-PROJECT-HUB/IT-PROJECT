from aiogram import Bot, Dispatcher, executor, types
from config import TOKEN
from database import Database

bot = Bot(TOKEN)
dispatcher = Dispatcher(bot)

database = Database()


@dispatcher.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(" Hello, I'm AnonymousChatBot!")

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = types.KeyboardButton("Find a partner")
    markup.add(btn)

    await message.answer("Press the button to find a partner", reply_markup=markup)


@dispatcher.message_handler(content_types=["text"])
async def bot_message(message: types.Message):
    if message.chat.type == 'private':
        if message.text == 'Find a partner':
            partner = database.get_queue()

            if database.create_chat(message.from_user.id, partner) is False:
                database.add_queue(message.from_user.id)

                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn = types.KeyboardButton("Stop searching")
                markup.add(btn)

                await message.answer("Find a partner...", reply_markup=markup)

            else:
                database.delete_queue(message.from_user.id)
                database.delete_queue(partner)

                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn = types.KeyboardButton("Disconnect")
                markup.add(btn)

                await message.answer("You are connect to the chat!", reply_markup=markup)
                await bot.send_message(partner, "You are connect to the chat!", reply_markup=markup)

        elif message.text == "Disconnect":
            chat = database.get_chat(message.from_user.id)

            if chat:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn = types.KeyboardButton("Find a partner")
                markup.add(btn)

                await message.answer("You are disconnect from the chat!", reply_markup=markup)
                await bot.send_message(chat[1], "Partner disconnected!", reply_markup=markup)

                database.delete_chat(message.from_user.id)
            else:
                await message.answer("You are not connected to the chat!")
        elif message.text == 'Stop searching':
            database.delete_queue(message.from_user.id)

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn = types.KeyboardButton("Find a partner")
            markup.add(btn)

            await message.answer("Search stopped!", reply_markup=markup)
        else:
            chat = database.get_chat(message.chat.id)
            await bot.send_message(chat[1], message.text)
    else:
        await message.answer("Bot work only in private chat!")


@dispatcher.message_handler(content_types=types.ContentTypes.VOICE)
async def voice_handler(message: types.Message):
    chat = database.get_chat(message.chat.id)

    if chat:
        await bot.send_voice(chat[1], message.voice.file_id)


@dispatcher.message_handler(content_types=types.ContentTypes.PHOTO)
async def photo_handler(message: types.Message):
    chat = database.get_chat(message.chat.id)

    if chat:
        await bot.send_photo(chat[1], message.photo[-1].file_id)


@dispatcher.message_handler(content_types=types.ContentTypes.DOCUMENT)
async def doc_handler(message: types.Message):
    chat = database.get_chat(message.chat.id)

    if chat:
        await bot.send_document(chat[1], message.document.file_id)


@dispatcher.message_handler(content_types=types.ContentTypes.VIDEO)
async def video_handler(message: types.Message):
    chat = database.get_chat(message.chat.id)

    if chat:
        await bot.send_video(chat[1], message.video.file_id)


@dispatcher.message_handler(content_types=types.ContentTypes.STICKER)
async def stick_handler(message: types.Message):
    chat = database.get_chat(message.chat.id)

    if chat:
        await bot.send_sticker(chat[1], message.sticker.file_id)


@dispatcher.message_handler(content_types=types.ContentTypes.AUDIO)
async def audio_handler(message: types.Message):
    chat = database.get_chat(message.chat.id)

    if chat:
        await bot.send_audio(chat[1], message.audio.file_id)


@dispatcher.message_handler(content_types=types.ContentTypes.VIDEO_NOTE)
async def video_note_handler(message: types.Message):
    chat = database.get_chat(message.chat.id)

    if chat:
        await bot.send_video_note(chat[1], message.video_note.file_id)


if __name__ == '__main__':
    executor.start_polling(dispatcher)
