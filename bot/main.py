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
    text = await utils.retrieve_text_from_voice(voice)

    await message.reply(text)


if __name__ == "__main__":
    executor.start_polling(dp)
