from aiogram import Bot
from aiogram import Dispatcher
from aiogram import executor
from aiogram import types

import config
from bot import utils
from bot.utils import hold_files_temporarily
from file_converter.file_converter import FileConverter
from speech_converter.speech_converter import SpeechConverter

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(content_types=["voice"])
async def speech_to_text(message: types.Message):
    voice = message.voice

    # For file to be able to be read by speech_recognition
    new_format = ".aiff"

    name_for_unconverted_file = utils.resolve_name_for_new_unconverted_file()
    name_for_converted_file = utils.resolve_name_for_new_converted_file()

    unconverted_file_path = \
        config.UNCONVERTED_VOICE_FILES_PATH / \
        (name_for_unconverted_file + new_format)

    converted_file_path = \
        config.CONVERTED_VOICE_FILES_PATH / \
        (name_for_converted_file + new_format)

    await voice.download(unconverted_file_path)

    created_file_path = FileConverter.convert_file(
        input_path=unconverted_file_path,
        output_path=converted_file_path
    )

    # Delete files after exiting context manager
    with hold_files_temporarily(converted_file_path, unconverted_file_path):
        text = SpeechConverter.audio_to_text(
            filename=created_file_path, language="en-US"
        )

    await message.reply(text)


if __name__ == "__main__":
    executor.start_polling(dp)
