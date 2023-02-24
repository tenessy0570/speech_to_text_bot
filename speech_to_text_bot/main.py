import asyncio

from aiogram import Bot
from aiogram import Dispatcher
from aiogram import types

import config
from speech_to_text_bot import utils
from speech_to_text_bot.utils import audio_to_text
from speech_to_text_bot.utils import convert_audio_file

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(content_types=["voice"])
async def speech_to_text(message: types.Message):
    voice = message.voice

    # For file to be able to be read by speech_recognition
    new_format = "aiff"

    unconverted_filename = utils.resolve_name_for_new_unconverted_file()
    converted_filename = utils.resolve_name_for_new_converted_file()

    await voice.download(config.UNCONVERTED_MESSAGES_PATH / unconverted_filename)

    created_file_path = convert_audio_file(
        input_path=config.UNCONVERTED_MESSAGES_PATH / unconverted_filename,
        output_path=config.CONVERTED_MESSAGES_PATH / converted_filename,
        format_=new_format,
    )

    text = audio_to_text(filename=created_file_path, language="en-US")
    await message.reply(text)


if __name__ == "__main__":
    asyncio.run(dp.start_polling(dp))
