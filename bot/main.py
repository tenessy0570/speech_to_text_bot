import logging

from aiogram import Bot
from aiogram import Dispatcher
from aiogram import executor
from aiogram import types

import config
from bot import utils

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot)


logging.basicConfig(
    filename=config.LOGGING_FILE,
    encoding='utf-8',
    level=logging.INFO,
    format="[%(asctime)s] [%(name)s] [%(levelname)s] > %(message)s"
)


@dp.message_handler(content_types=["voice"])
async def speech_to_text(message: types.Message):
    voice = message.voice
    result: dict = await utils.retrieve_text_from_voice(voice, show_all=True)

    possible_transcripts = tuple(
        item["transcript"]
        for item in result["alternative"]
    )

    # buttons = tuple(
    #     types.InlineKeyboardButton(transcript, callback_data=transcript)
    #     for transcript in possible_transcripts
    # )
    #
    # keyboard = types.ReplyKeyboardMarkup(
    #     resize_keyboard=True, one_time_keyboard=True
    # )
    #
    # for button in buttons:
    #     keyboard.add(button)

    # keyboard.add(types.InlineKeyboardButton("Cancel", callback_data="Cancel"))
    #
    # await message.reply("Choose correct variant", reply_markup=keyboard)
    await message.reply(possible_transcripts[0])


# @dp.message_handler(content_types=["text"])
# async def handle_said_sentence(message: types.Message):
#     data: str = message.text
#
#     if data == "Cancel":
#         return None
#
#     binary_operator, amount, item_name = utils.parse_query(data)
#
#     if binary_operator == amount == item_name == "null":
#         await message.reply("Wrong query format.")
#         return None
#
#     await message.reply(f"{binary_operator=}, {amount=}, {item_name=}")
#
#     try:
#         with db_session as session:
#             query = select(CafeItem).where(
#                 CafeItem.name.ilike(f"%{item_name}%")  # Case-insensitive
#             )
#             found_item: CafeItem | None = session.scalar(query)
#
#             if found_item is None:
#                 await message.reply(f"Item with `{item_name}` in its name doesn't exist.")
#                 return None
#
#             old_amount = found_item.amount
#             new_amount = utils.execute_binary_operation(
#                 left_operand=old_amount,
#                 right_operand=int(amount),
#                 binary_operator=binary_operator
#             )
#             found_item_name = found_item.name
#
#             found_item.amount = new_amount
#
#             session.commit()
#     except Exception as exc:
#         await message.reply(repr(exc))
#     finally:
#         result_message = f"Updated `{found_item_name}` amount from {old_amount} to {new_amount}"
#         await message.reply(result_message)


if __name__ == "__main__":
    executor.start_polling(dp)
