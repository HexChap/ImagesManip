import os
from pathlib import Path

from PIL.ImageFile import ImageFile


def rename_images(images: list[ImageFile], new_name: str = ""):
    for i, image in enumerate(images):
        rename_image(image, f"{new_name}{i}")


def rename_image(image: ImageFile, new_name: str):
    image_dir = Path(image.filename).parent
    _, image_ext = os.path.splitext(image.filename)

    image.filename = image_dir / f"{new_name}{image_ext}"
