from abc import abstractmethod
from pathlib import Path

import speech_recognition as sr


class BaseConverter:
    @classmethod
    @abstractmethod
    def audio_to_text(cls, *args, **kwargs) -> str:
        pass


class SpeechConverter(BaseConverter):
    @classmethod
    def audio_to_text(cls, filename: str | Path, language: str = "en-US") -> str:
        if not isinstance(filename, (str, Path)):
            raise TypeError("Allowed types for filename argument: [str, Path]")

        if not isinstance(filename, str):
            filename = str(filename)

        r = sr.Recognizer()

        with sr.AudioFile(filename) as source:
            audio_data = r.record(source)
            text = r.recognize_google(audio_data, language=language)

        return text
