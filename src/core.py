import os
import win32con
import win32gui
from ctypes import windll
from tkinter import filedialog

import tomli_w

import src.settings as stngs
from src.settings import settings, Watermark, Paths, Settings, load_settings

TRANSPARENCY_DEFAULT_PERCENT = 50

windll.shcore.SetProcessDpiAwareness(1)


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def ask_filename(filetypes_string: str) -> str:
    """

    :param filetypes_string: >>> "Text Files\0*.TXT;*.DOC;*.BAK\0 Something cool\0*.png\0\0"
    :return:
    """
    customfilter = "Other file types\0*.*\0"
    fname, customfilter, flags = win32gui.GetOpenFileNameW(
        Flags=win32con.OFN_ALLOWMULTISELECT | win32con.OFN_EXPLORER | win32con.OFN_FILEMUSTEXIST,
        DefExt="py",
        Filter=filetypes_string,
        CustomFilter=customfilter,
        FilterIndex=0,
    )

    return fname


def get_paths(*, force_rewrite: bool = False) -> Paths:
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

    if not all((src, out)) or force_rewrite:
        src, out = _ask_user()

    paths = Paths(source=src, output=out)
    settings["paths"] = paths

    return paths


def get_watermark_settings(*, force_rewrite: bool = False) -> Watermark:
    watermark = settings["watermark"]
    path, tncy_percent, *_ = watermark.values()

    if not all((path, tncy_percent)) or force_rewrite:
        input("Выберите файл с лого. \nНажмите клавишу Enter чтобы продолжить.")
        path = ask_filename("*.SVG;*.png\0\0")
        tncy_percent = TRANSPARENCY_DEFAULT_PERCENT

        if force_rewrite:
            user_in = input("Введите процент прозрачности лого (50 по умолчанию): ")
            if user_in.isdigit():
                tncy_percent = int(user_in)

    watermark = Watermark(path=path, transparency_percent=tncy_percent)
    settings["watermark"] = watermark

    return watermark


def _write_update_settings(settings_):
    with open(stngs.settings_path, mode="wb") as fp:
        tomli_w.dump(settings_, fp)

    stngs.settings = settings_


def _change_paths() -> Settings:
    settings_ = load_settings()
    settings_["paths"] = get_paths(force_rewrite=True)

    return settings_


def _change_watermark_settings() -> Settings:
    settings_ = load_settings()
    settings_["watermark"] = get_watermark_settings(force_rewrite=True)

    return settings_


def change_settings():
    settings_ = stngs.settings
    is_choosing = True
    while is_choosing:
        print(
            "Выберите действие:",
            "1. Папка с исходными фото и результатами",
            "2. Настройки добавления лого",
            sep="\n\t"
        )
        action = input("--> ")

        match action:
            case "1":
                settings_ = _change_paths()
            case "2":
                settings_ = _change_watermark_settings()
            case _:
                print("Неверная опция! Попробуйте снова!\n")
                continue

        is_choosing = False
    _write_update_settings(settings_)
