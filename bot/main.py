from aiogram import Bot
from aiogram import Dispatcher
from aiogram import executor
from aiogram import types

import config
from bot import utils

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(content_types=["voice"])
async def speech_to_text(message: types.Message):
    voice = message.voice
    result: dict = await utils.retrieve_text_from_voice(voice, show_all=True)

    possible_transcripts = tuple(
        item["transcript"]
        for item in result["alternative"]
    )

    buttons = tuple(
        types.InlineKeyboardButton(transcript, callback_data=transcript)
        for transcript in possible_transcripts
    )

    keyboard = types.ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True
    )

    for button in buttons:
        keyboard.add(button)

    keyboard.add(types.InlineKeyboardButton("Cancel", callback_data="cancel"))

    await message.reply("Choose correct variant", reply_markup=keyboard)


@dp.message_handler(content_types=["text"])
async def handle_said_sentence(message: types.Message):
    data: str = message.text

    if data == "cancel":
        return None

    binary_operator = amount = item_name = "null"

    if data.startswith(("+", "-")):
        binary_operator = data[0]
        amount, item_name = data[1:].strip().split(" ")
    elif data.startswith(("plus", "minus")):
        binary_operator, amount, item_name = data.split(" ")

    await message.reply(f"{binary_operator=}, {amount=}, {item_name=}")

if __name__ == "__main__":
    executor.start_polling(dp)
