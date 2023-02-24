import ffmpeg
import speech_recognition as sr

from config import CONVERTED_MESSAGES_PATH
from config import DEFAULT_CONVERTED_FILENAME
from config import DEFAULT_UNCONVERTED_FILENAME
from config import UNCONVERTED_MESSAGES_PATH


def resolve_name_for_new_unconverted_file() -> str:
    amount_of_files_inside_dir = len(
        tuple(True for _ in UNCONVERTED_MESSAGES_PATH.iterdir()),
    )

    digit = 1 if not amount_of_files_inside_dir else amount_of_files_inside_dir
    filename = DEFAULT_UNCONVERTED_FILENAME + "_" + str(digit)
    return UNCONVERTED_MESSAGES_PATH / filename


def resolve_name_for_new_converted_file() -> str:
    amount_of_files_inside_dir = len(
        tuple(True for _ in CONVERTED_MESSAGES_PATH.iterdir()),
    )

    digit = 1 if not amount_of_files_inside_dir else amount_of_files_inside_dir
    filename = DEFAULT_CONVERTED_FILENAME + "_" + str(digit)
    return CONVERTED_MESSAGES_PATH / filename


def convert_audio_file(input_path, output_path, format_) -> str:
    stream = ffmpeg.input(input_path)

    new_file_path = output_path + "." + format_
    stream = ffmpeg.output(stream, new_file_path)
    ffmpeg.run(stream)

    return new_file_path


def audio_to_text(filename: str, language="en-US") -> str:
    r = sr.Recognizer()

    with sr.AudioFile(filename) as source:
        audio_data = r.record(source)
        text = r.recognize_google(audio_data, language=language)

    return text
