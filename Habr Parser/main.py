from bs4 import BeautifulSoup
import urllib.request as urllib
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = "YOUR API KEY"

bot = Bot(token=API_TOKEN)
dispatcher = Dispatcher(bot)

list_buttons = ['Python News', 'Habr News', 'Python Projects']


@dispatcher.message_handler(commands=['start', 'help'])
async def start_command(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    markup.add(types.KeyboardButton(list_buttons[0]))
    markup.add(types.KeyboardButton(list_buttons[1]))
    markup.add(types.KeyboardButton(list_buttons[2]))

    await message.reply("👋 Hi!\n🤖 I'm link bot-parser from habr!", reply_markup=markup)


@dispatcher.message_handler(content_types='text')
async def articles(message: types.Message):
    url = ''

    try:
        if message.text in list_buttons:
            if message.text == list_buttons[0]:
                url = 'https://habr.com/ru/search/?q=Python&target_type=posts&order=date'

            elif message.text == list_buttons[1]:
                url = 'https://habr.com/ru/all/'

            elif message.text == list_buttons[2]:
                url = 'https://habr.com/ru/hub/python/'

            tag = 'a'
            class_tag = 'tm-article-snippet__title-link'
            url_site = 'habr.com'

            page = urllib.urlopen(url)
            soup = BeautifulSoup(page, 'html.parser')
            article_list = (soup.find_all(tag, attrs={'class': class_tag}))[:5]

            for i in article_list:
                article = f"{i.text.strip()}\n\n{url_site}{i['href']}"
                await bot.send_message(message.from_user.id, article)
        else:
            await message.answer("⌨ To open the keyboard, enter the command /start")
    except Exception:
        pass


if __name__ == '__main__':
    executor.start_polling(dispatcher, skip_updates=True)
