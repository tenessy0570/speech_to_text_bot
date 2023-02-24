import asyncio

from aiogram import Bot
from aiogram import Dispatcher
from aiogram import types

import config
from bot import utils
from file_converter.file_converter import FileConverter
from speech_converter.speech_converter import SpeechConverter

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

    created_file_path = FileConverter.convert_file(
        input_path=config.UNCONVERTED_MESSAGES_PATH / unconverted_filename,
        output_path=config.CONVERTED_MESSAGES_PATH / converted_filename,
        new_format=new_format,
    )

    text = SpeechConverter.audio_to_text(
        filename=created_file_path, language="en-US"
    )

    await message.reply(text)


if __name__ == "__main__":
    asyncio.run(dp.start_polling(dp))
