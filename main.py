import asyncio
from pathlib import Path

from PIL import Image

from src.core import clear, get_paths, change_settings, get_watermark_settings
from src.updater import do_update
from src.place_watermark import place_watermarks
from src.rename import rename_images
from src.save import save_images
from src.utils import get_image_paths
from src import APP_NAME, __version__


async def main():
    error_msg = "Неверная опция! Попробуйте снова!\n"
    actions = ["Добавить лого", "Переименовать", "Добавить лого и переименовать"]

    is_choosing = True
    while is_choosing:
        print(
            "Выберите действие:",
            "0. Настройки",
            *[f"{i+1}. {action}" for i, action in enumerate(actions)],
            sep="\n\t"
        )
        action = input("--> ")

        if not action.isdigit():
            print(error_msg)
            continue

        action = int(action)

        if action == 0:
            change_settings()
            continue

        if action in [i for i in range(1, len(actions)+1)]:
            src, out = get_paths().values()

            clear()
            print(f"Папка с фото: {src}\n"
                  f"Папка для результатов: {out}\n\n")

            images = [Image.open(path) for path in get_image_paths(src)]
        else:
            print(error_msg)
            continue

        clear()
        match action:
            case 1:
                watermark = Image.open(get_watermark_settings()["path"])
                place_watermarks(images, watermark)
            case 2:
                rename_images(images, input("Введите новое имя: "))
            case 3:
                watermark = Image.open(get_watermark_settings()["path"])
                place_watermarks(images, watermark)
                rename_images(images, input("Введите новое имя: "))
            case _:
                clear()
                print(error_msg)
                continue

        is_choosing = False
        await save_images(images, Path(out))

        clear()
        print("Операция успешно выполнена!")


if __name__ == '__main__':
    print(f'Starting {APP_NAME} {__version__}...')
    do_update()
    asyncio.run(main())
