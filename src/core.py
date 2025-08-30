import os
import platform
from tkinter import Tk, filedialog

import tomli_w

import src.settings as stngs
from src.settings import Paths, Settings, Watermark, load_settings, settings

TRANSPARENCY_DEFAULT_PERCENT = 50

# Windows-only: high-DPI awareness
if platform.system() == "Windows":
    try:
        from ctypes import windll

        windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def ask_filename(filetypes_string: str) -> str:
    """
    Cross-platform file dialog
    :param filetypes_string: >>> "*.svg;*.png"
    :return: selected file path
    """
    root = Tk()
    root.withdraw()

    # Parse Windows-style "*.SVG;*.png\0\0" → [("Images", ("*.svg", "*.png"))]
    filetypes = []
    if filetypes_string:
        exts = [
            e.strip()
            for e in filetypes_string.replace("\0", "").split(";")
            if e.strip()
        ]
        if exts:
            filetypes.append(("Allowed files", exts))
    filetypes.append(("All files", "*.*"))

    fname = filedialog.askopenfilename(title="Выберите файл", filetypes=filetypes)
    root.destroy()
    return fname


def get_paths(*, force_rewrite: bool = False) -> Paths:
    """
    Get source and output paths from settings or ask user
    """

    def _ask_user() -> tuple[str, str]:
        clear()
        input("Выберите папку с фотками. \nНажмите клавишу Enter чтобы продолжить.")
        root = Tk()
        root.withdraw()
        in_folder = filedialog.askdirectory(title="Папка с исходными фото")
        root.destroy()

        clear()
        input(
            "Выберите папку куда сохранить результат. \nНажмите клавишу Enter чтобы продолжить."
        )
        root = Tk()
        root.withdraw()
        out_folder = filedialog.askdirectory(title="Папка для сохранения")
        root.destroy()

        return in_folder, out_folder

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
        path = ask_filename("*.svg;*.png")
        tncy_percent = TRANSPARENCY_DEFAULT_PERCENT

        if force_rewrite:
            user_in = input("Введите процент прозрачности лого (50 по умолчанию): ")
            if user_in.isdigit():
                tncy_percent = int(user_in)

    watermark = Watermark(path=path, transparency_percent=tncy_percent)
    settings["watermark"] = watermark

    return watermark


def is_debug() -> bool:
    return settings["misc"]["debug"]


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


def _change_misc() -> Settings:
    misc = settings["misc"]
    user_in = ""
    prompts = {"debug": " режим отладки."}
    actions = {"debug": lambda: misc.update(debug=not misc["debug"])}

    if misc["debug"]:
        prompts["debug"] = "Выклюить" + prompts["debug"]
    else:
        prompts["debug"] = "Вклюить" + prompts["debug"]

    for i, promt in enumerate(prompts.values(), start=1):
        print(f"{i}. {promt}")

    while not user_in.isdigit():
        user_in = input("--> ")
    user_in = int(user_in)

    actions[tuple(actions.keys())[user_in - 1]]()

    settings_ = load_settings()
    settings_["misc"] = misc

    return settings_


def change_settings():
    settings_ = stngs.settings
    is_choosing = True
    while is_choosing:
        print(
            "Выберите действие:",
            "1. Папка с исходными фото и результатами",
            "2. Настройки добавления лого",
            "3. Прочее",
            sep="\n\t",
        )
        action = input("--> ")

        match action:
            case "1":
                settings_ = _change_paths()
            case "2":
                settings_ = _change_watermark_settings()
            case "3":
                settings_ = _change_misc()
            case _:
                print("Неверная опция! Попробуйте снова!\n")
                continue

        is_choosing = False
    _write_update_settings(settings_)
