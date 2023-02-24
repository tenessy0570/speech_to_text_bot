from abc import abstractmethod
from pathlib import Path

import ffmpeg

created_file_path = str


class BaseConverter:
    @classmethod
    @abstractmethod
    def convert_file(
            cls,
            input_path: str | Path,
            output_path: str | Path,
            new_format: str
    ) -> created_file_path:
        pass


class FileConverter(BaseConverter):
    @classmethod
    def convert_file(
            cls,
            input_path: str | Path,
            output_path: str | Path,
            new_format: str
    ) -> created_file_path:
        if not isinstance(output_path, str):
            output_path = str(output_path)

        if not isinstance(input_path, str):
            input_path = str(input_path)

        stream = ffmpeg.input(input_path)

        new_file_path = output_path + "." + new_format
        stream = ffmpeg.output(stream, new_file_path)
        ffmpeg.run(stream)

        return new_file_path
