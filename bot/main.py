from aiogram import Bot
from aiogram import Dispatcher
from aiogram import executor
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

    # Convert to aiff so file can be read by speech-recognition
    new_format = ".aiff"

    unconverted_file_path = utils.resolve_new_unconverted_file_path(
        new_format=new_format
    )
    converted_file_path = utils.resolve_new_converted_file_path(
        new_format=new_format
    )

    await voice.download(unconverted_file_path)

    created_file_path = FileConverter.convert_file(
        input_path=unconverted_file_path,
        output_path=converted_file_path
    )

    # Delete files after exiting context manager
    with utils.hold_files_temporarily(converted_file_path, unconverted_file_path):
        text = SpeechConverter.audio_to_text(
            filename=created_file_path, language="en-US"
        )

    await message.reply(text)


if __name__ == "__main__":
    executor.start_polling(dp)
