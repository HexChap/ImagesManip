import asyncio

from PIL import Image

from src.core import clear, get_paths
from src.place_watermark import place_watermarks
from src.rename import rename_images
from src.save import save_images
from src.utils import get_image_paths


async def main():
    src, out = get_paths().values()

    clear()
    print(f"Папка с фото: {src}\n"
          f"Папка для результатов: {out}\n\n")

    images = [Image.open(path) for path in get_image_paths(src)]
    is_choosing = True
    while is_choosing:
        print(
            "Выберите действие:",
            "0. Настройки",
            "1. Добавить лого",
            "2. Переименовать",
            "3. Добавить лого и переименовать",
            sep="\n\t"
        )
        action = input("--> ")
        clear()
        match action:
            case "1":
                place_watermarks(images)
            case "2":
                rename_images(images, input("Введите новое имя: "))
            case "3":
                place_watermarks(images)
                rename_images(images, input("Введите новое имя: "))
            case _:
                clear()
                print("Неверная опция! Попробуйте снова\n")

                continue

        is_choosing = False
        await save_images(images)

        clear()
        print("Операция успешно выполнена!")


asyncio.run(main())
