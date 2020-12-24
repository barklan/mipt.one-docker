import os
API_TOKEN = os.environ.get('TGBOTTOKEN', 'none')
import quote


from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.message import ContentType
import re
import random
import json
import urllib.request
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
sem_dict = {}


def change_sem_keyboard():
    keyboard_markup = types.InlineKeyboardMarkup(row_width=3)
    text_and_data = ((str(i), str(i)) for i in range(1, 6))
    row_btns = (types.InlineKeyboardButton(text, callback_data=data) for text, data in text_and_data)
    keyboard_markup.row(*row_btns)
    return keyboard_markup


@dp.message_handler(commands='start')
async def start_cmd_handler(message: types.Message):
    await message.reply("Привет!\nУ меня есть много задач по физике!\nПросто выбери семестр и набери номер задачи.\nТакже вы всегда можете выбрать семестр набрав 'семестр'", reply_markup=change_sem_keyboard())


@dp.callback_query_handler(text='1')
@dp.callback_query_handler(text='2')
@dp.callback_query_handler(text='3')
@dp.callback_query_handler(text='4')
@dp.callback_query_handler(text='5')
async def inline_kb_answer_callback_handler(query: types.CallbackQuery):
    answer_data = query.data
    sem_dict[query.from_user.id] = answer_data
    await query.answer(f'Выбранный семестр: {answer_data!r}')
    await bot.send_message(query.from_user.id, "Номер задачи?")


@dp.message_handler(regexp=r'^\d{1,2}\.\d{1,3}$')
async def all_msg_handler(message: types.Message):
    if message.from_user.id in sem_dict:
        sem = sem_dict[message.from_user.id]
        zad = message.text
        url = f'http://web:8000/phys/?sem={sem}&zad={zad}'
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode())
        output = result['search_output']

        await message.answer(output)

        if result['image_found'] == True:
            await bot.send_photo(message.from_user.id, 'https://mipt.one' + result['image_url'] + '.jpg')
            if result['second_file'] == True:
                await bot.send_photo(message.from_user.id, 'https://mipt.one' + result['image_url'] + '-2.jpg')
            else:
                pass
        elif result['wrong_input'] == False:
            await bot.send_message(
                message.from_user.id, 
                'Отправьте свое решение 🤏',
            )
        else:
            pass
    else:
        await bot.send_message(
            message.from_user.id, 
            'Пожалуйста выберете семестр.\nВыбранный семестр мог сброситься при обновленни бота.',
            reply_markup=change_sem_keyboard()
        )


@dp.message_handler(regexp=r'^семестр$')
async def change_sem(message: types.Message):
    await bot.send_message(
            message.from_user.id, 
            'Хотите сменить семестр?',
            reply_markup=change_sem_keyboard()
        )


@dp.message_handler(content_types=ContentType.PHOTO)
async def photo(message: types.Message):
    '''
    TODO change file path of download
    '''
    sem = sem_dict[message.from_user.id]
    zad = message.caption
    url = f'http://web:8000/phys/?sem={sem}&zad={zad}'
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req)
    result = json.loads(response.read().decode())

    if message.caption is None:
        await bot.send_message(message.from_user.id, 'Фотку нужно подписать номером задачи.')
    else:
        if (result['wrong_input'] == True):
            await bot.send_message(message.from_user.id, 'Вы неправильно подписали фотку :(')
        elif (result['wrong_input'] == False):
            if (result['image_found'] == False):
                file_id = message.photo[-1].file_id
                await bot.download_file_by_id(file_id, f'/usr/src/aiogram/mediafiles/imgbank/{sem}/{message.caption}.jpg')
                emo_list = ['👍', '😁', '😊', '🥰', '😍', '😗', '😚', '🤗', '😎', '😻']
                await bot.send_message(message.from_user.id, 'Решение выложено. Спасибо ' + random.choice(emo_list))
            else:
                await bot.send_message(message.from_user.id, 'Решение к этой задаче уже есть.')
        else:
            pass


@dp.message_handler()
async def echo(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)
    try:
        answer = quote.get_quote(model)
    except:
        answer = 'Я не понимаю этот запрос :('
    await message.answer(answer)


if __name__ == '__main__':
    global model
    model = quote.fit_model()
    executor.start_polling(dp, skip_updates=True)
