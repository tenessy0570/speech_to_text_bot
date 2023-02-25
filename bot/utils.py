import os
import typing
from contextlib import contextmanager
from pathlib import Path

from config import CONVERTED_VOICE_FILES_PATH
from config import DEFAULT_CONVERTED_FILENAME
from config import DEFAULT_UNCONVERTED_FILENAME
from config import UNCONVERTED_VOICE_FILES_PATH


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
def hold_files_temporarily(*args: typing.Iterable[Path | str]):
    yield
    for path in args:
        if isinstance(path, Path):
            path = str(path)

        os.remove(path)


def resolve_new_converted_file_path(new_format: str):
    name_for_converted_file = _resolve_name_for_new_converted_file()
    converted_file_path = CONVERTED_VOICE_FILES_PATH / \
        (name_for_converted_file + new_format)
    return converted_file_path


def resolve_new_unconverted_file_path(new_format: str):
    name_for_unconverted_file = _resolve_name_for_new_unconverted_file()
    unconverted_file_path = UNCONVERTED_VOICE_FILES_PATH / \
        (name_for_unconverted_file + new_format)
    return unconverted_file_path
