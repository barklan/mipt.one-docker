import os

API_TOKEN = os.environ.get("TGBOTTOKEN", "none")
import quote


from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.message import ContentType
from aiogram.types.input_media import InputMediaPhoto
import re
import random
import json
import urllib.request
import ssl
import pickle

ssl._create_default_https_context = ssl._create_unverified_context


from nn_module import load_model, get_model_output


import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


welcome_message = 'Приветик!\nПросто выбери семестр и набери номер задачи.\n\
Вы можете поменять семестр набрав "сем", "семестр", "sem", "semester".'


# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
sem_dict = {}

# Load blacklist
blacklist_path = "/usr/src/aiogram/mediafiles/imgbank/blacklist.pkl"
global blacklist
if os.path.isfile(blacklist_path):
    with open(blacklist_path, "rb") as f:
        blacklist = pickle.load(f)
else:
    blacklist = set()
    with open(blacklist_path, "wb") as f:
        pickle.dump(blacklist, f)


def add_to_blacklist(user_id):
    """
    Adds user_id to blacklist
    """
    blacklist.add(user_id)
    with open(blacklist_path, "wb") as f:
        pickle.dump(blacklist, f)


def change_sem_keyboard():
    """
    Provides keyboard for semester changes
    """
    keyboard_markup = types.InlineKeyboardMarkup(row_width=3)
    text_and_data = ((str(i), str(i)) for i in range(1, 6))
    row_btns = (
        types.InlineKeyboardButton(text, callback_data=data)
        for text, data in text_and_data
    )
    keyboard_markup.row(*row_btns)
    return keyboard_markup


@dp.message_handler(commands="start")
async def start_cmd_handler(message: types.Message):
    await bot.send_message(
        message.from_user.id, welcome_message, reply_markup=change_sem_keyboard()
    )


@dp.callback_query_handler(text="1")
@dp.callback_query_handler(text="2")
@dp.callback_query_handler(text="3")
@dp.callback_query_handler(text="4")
@dp.callback_query_handler(text="5")
async def inline_kb_answer_callback_handler(query: types.CallbackQuery):
    """
    Handler for semester queries
    """
    answer_data = query.data
    sem_dict[query.from_user.id] = answer_data
    await query.answer(f"Выбранный семестр: {answer_data!r}")
    await bot.send_message(query.from_user.id, "Номер задачи?")


@dp.message_handler(regexp=r"^\d{1,2}\.\d{1,3}$")
async def all_msg_handler(message: types.Message):
    """
    Main request for task solutions
    """
    id = message.from_user.id
    if id in sem_dict:
        sem = sem_dict[id]
        zad = message.text
        url = f"http://web:8000/phys/?sem={sem}&zad={zad}"
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode())
        output = result["search_output"]

        await message.answer(output)

        if result["image_found"] == True:
            base_img_url = "https://mipt.one" + result["image_url"]
            if result["second_file"] == True:
                if result["third_file"] == True:
                    await bot.send_media_group(
                        id,
                        media=[
                            InputMediaPhoto(base_img_url + prefix + ".jpg")
                            for prefix in ["", "-2", "-3"]
                        ],
                    )
                else:
                    await bot.send_media_group(
                        id,
                        media=[
                            InputMediaPhoto(base_img_url + prefix + ".jpg")
                            for prefix in ["", "-2"]
                        ],
                    )
            else:
                await bot.send_photo(id, base_img_url + ".jpg")
        elif result["wrong_input"] == False:
            if id not in blacklist:
                await bot.send_message(id, "Отправь мне свое решение одной фоткой 🤏")
            else:
                pass
        else:
            pass
    else:
        await bot.send_message(
            id,
            "Пожалуйста выберете семестр.\nВыбранный семестр мог сброситься при обновленни бота.",
            reply_markup=change_sem_keyboard(),
        )


@dp.message_handler(regexp=r"(^семестр$|^сем$|^sem$|^semester$)")
async def change_sem(message: types.Message):
    """
    To change semester
    """
    await bot.send_message(
        message.from_user.id,
        "Хотите сменить семестр?",
        reply_markup=change_sem_keyboard(),
    )


@dp.message_handler(content_types=ContentType.PHOTO)
async def photo(message: types.Message):
    """
    Function to handle images from user
    """
    id = message.from_user.id
    sem = sem_dict[id]
    zad = message.caption
    url = f"http://web:8000/phys/?sem={sem}&zad={zad}"
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req)
    result = json.loads(response.read().decode())

    if id in blacklist:
        await bot.send_message(
            id, "Вы находитесь в черном списке. Ваши фото не принимаются."
        )
    elif message.caption is None:
        await bot.send_message(id, "Фотку нужно подписать номером задачи.")
    else:
        if result["wrong_input"] == True:
            await bot.send_message(id, "Вы неправильно подписали фотку :(")
        elif result["wrong_input"] == False:
            if result["image_found"] == False:
                file_id = message.photo[-1].file_id

                temp_path = (
                    f"/usr/src/aiogram/mediafiles/imgbank/666/{message.caption}.jpg"
                )
                await bot.download_file_by_id(file_id, temp_path)
                image_is_good = get_model_output(model_ft, temp_path)
                if image_is_good:
                    await bot.download_file_by_id(
                        file_id,
                        f"/usr/src/aiogram/mediafiles/imgbank/{sem}/{message.caption}.jpg",
                    )
                    emo_list = ["👍", "😁", "😊", "🥰", "😍", "😗", "😚", "🤗", "😎", "😻"]
                    await bot.send_message(
                        id, "Решение выложено. Спасибо " + random.choice(emo_list)
                    )
                else:
                    await bot.send_message(
                        id,
                        "Нейронная сеть отвергла это изображение.\nА вы думали просто будет дикпики выкладывать? :|",
                    )
                    add_to_blacklist(id)
                os.remove(temp_path)
            else:
                await bot.send_message(id, "Решение к этой задаче уже есть.")
        else:
            pass


@dp.message_handler()
async def echo(message: types.Message):
    """
    Answer to random queries
    """
    try:
        answer = quote.get_quote(model)
    except:
        answer = "Я не понимаю этот запрос :("
    await message.answer(answer)


if __name__ == "__main__":
    global model
    model = quote.fit_model()
    global model_ft
    model_ft = load_model("saved_model")
    executor.start_polling(dp, skip_updates=True)
