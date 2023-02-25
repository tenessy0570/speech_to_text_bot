import os
from contextlib import contextmanager
from pathlib import Path

import aiogram.types

from config import CONVERTED_VOICE_FILES_PATH
from config import DEFAULT_CONVERTED_FILENAME
from config import DEFAULT_UNCONVERTED_FILENAME
from config import UNCONVERTED_VOICE_FILES_PATH
from file_converter.file_converter import FileConverter
from speech_converter.speech_converter import SpeechConverter


def _resolve_name_for_new_unconverted_file() -> str:
    amount_of_files_inside_dir = len(
        tuple(True for _ in UNCONVERTED_VOICE_FILES_PATH.iterdir()),
    )

    digit = 1 if not amount_of_files_inside_dir else amount_of_files_inside_dir
    filename = DEFAULT_UNCONVERTED_FILENAME + "_" + str(digit)
    return filename


def _resolve_name_for_new_converted_file() -> str:
    amount_of_files_inside_dir = len(
        tuple(True for _ in CONVERTED_VOICE_FILES_PATH.iterdir()),
    )

    digit = 1 if not amount_of_files_inside_dir else amount_of_files_inside_dir
    filename = DEFAULT_CONVERTED_FILENAME + "_" + str(digit)
    return filename


@contextmanager
def hold_files_temporarily(*args: Path | str):
    yield
    for path in args:
        if isinstance(path, Path):
            path = str(path)

        os.remove(path)


def resolve_new_converted_file_path(new_format: str) -> Path:
    name_for_converted_file = _resolve_name_for_new_converted_file()
    converted_file_path = CONVERTED_VOICE_FILES_PATH / \
        (name_for_converted_file + new_format)
    return converted_file_path


def resolve_new_unconverted_file_path(new_format: str) -> Path:
    name_for_unconverted_file = _resolve_name_for_new_unconverted_file()
    unconverted_file_path = UNCONVERTED_VOICE_FILES_PATH / \
        (name_for_unconverted_file + new_format)
    return unconverted_file_path


async def retrieve_text_from_voice(
        voice: aiogram.types.Voice,
        show_all: bool = False
) -> str | dict:
    # Convert to aiff so file can be read by speech-recognition
    new_format = ".aiff"

    unconverted_file_path = resolve_new_unconverted_file_path(
        new_format=new_format
    )
    converted_file_path = resolve_new_converted_file_path(
        new_format=new_format
    )

    await voice.download(unconverted_file_path)

    created_file_path = FileConverter.convert_file(
        input_path=unconverted_file_path,
        output_path=converted_file_path
    )

    # Delete files after exiting context manager
    with hold_files_temporarily(converted_file_path, unconverted_file_path):
        text = SpeechConverter.audio_to_text(
            filename=created_file_path, language="en-US", show_all=show_all
        )

    return text


def parse_query(data: str) -> tuple[str, str, str]:
    binary_operator = amount = item_name = "null"

    if data.startswith(("+", "-")):
        binary_operator = data[0]
        splitted = data[1:].strip().split(" ")
        amount, item_name = splitted[0], " ".join(splitted[1:])
    elif data.startswith(("plus", "minus")):
        splitted = data.split(" ")
        binary_operator, amount, item_name = \
            splitted[0], splitted[1], " ".join(splitted[2:])

    return binary_operator, amount, item_name


def execute_binary_operation(
        left_operand: int,
        right_operand: int,
        binary_operator: str
) -> int:
    binary_method_by_string = {
        "plus": "__add__",
        "+": "__add__",
        "minus": "__sub__",
        "-": "__sub__"
    }

    result = getattr(
        left_operand,
        binary_method_by_string[binary_operator]
    )(int(right_operand))

    return result
