from aiogram import Bot
from aiogram import Dispatcher
from aiogram import executor
from aiogram import types
from sqlalchemy import select

import config
from bot import utils
from database.db import db_session
from database.models import BarItem

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

    binary_method_by_string = {
        "plus": "__add__",
        "+": "__add__",
        "minus": "__sub__",
        "-": "__sub__"
    }

    try:
        with db_session as session:
            query = select(BarItem).where(
                BarItem.name.op('regexp')(fr'.*{item_name}.*')
            )
            found_item: BarItem | None = session.scalar(query)

            if found_item is None:
                await message.reply(f"Item named {item_name} doesn't exist.")
                return None

            old_amount = found_item.amount
            new_amount = getattr(
                old_amount,
                binary_method_by_string[binary_operator]
            )(int(amount))
            found_item_name = found_item.name

            found_item.amount = new_amount

            session.commit()
    except Exception as exc:
        await message.reply(repr(exc))
    finally:
        result_message = f"Updated `{found_item_name}` amount from {old_amount} to {new_amount}"
        await message.reply(result_message)


if __name__ == "__main__":
    executor.start_polling(dp)
