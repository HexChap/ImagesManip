import os
from ctypes import windll
from tkinter import filedialog
import tkinter as tk

from src.settings import settings, Watermark, Paths

TRANSPARENCY_DEFAULT_PERCENT = 50

windll.shcore.SetProcessDpiAwareness(1)


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def get_paths() -> Paths:
    """
    Get source and output paths from settings or ask user

    :return: Tuple of source and output paths
    """
    def _ask_user() -> tuple[str, str]:
        clear()
        input("Выберите папку с фотками. \nНажмите клавишу Enter чтобы продолжить.")
        in_folder = filedialog.askdirectory()
        # in_folder = r"D:\Работа\ADVANCE\Бургас\Възраждане\Возраждение 1шка 40м2 - Copy"

        clear()
        input("Выберите папку куда сохранить результат. \nНажмите клавишу Enter чтобы продолжить.")
        src_folder = filedialog.askdirectory()
#         src_folder = r"D:\Работа\ADVANCE\Бургас\Възраждане"

        return in_folder, src_folder

    paths = settings["paths"]
    src, out, *_ = paths.values()

    if not all((src, out)):
        src, out = _ask_user()

    paths = Paths(source=src, output=out)
    settings["paths"] = paths

    return paths


def get_watermark_settings() -> Watermark:
    watermark = settings["watermark"]
    path, tncy_percent, *_ = watermark.values()

    if not all((path, tncy_percent)):
        input("Выберите файл с лого. \nНажмите клавишу Enter чтобы продолжить.")
        path = filedialog.askopenfilename()
        tncy_percent = TRANSPARENCY_DEFAULT_PERCENT

    watermark = Watermark(path=path, transparency_percent=tncy_percent)
    settings["watermark"] = watermark

    return watermark
