import asyncio
from io import BytesIO
from pathlib import Path

import aiofiles
from PIL.ImageFile import ImageFile

from src.core import get_paths


async def save_images(images: list[ImageFile], output: Path):
    async with asyncio.TaskGroup() as tg:
        for image in images:
            tg.create_task(save_image(image, output))


async def save_image(image: ImageFile, output: Path):
    """
    Asynchronously saves images.

    :param output: Output path
    :param image: Image to save
    :return:
    """
    path = output / Path(image.filename).name

    image = image.convert("RGB")
    image.save(buf := BytesIO(), format="JPEG")

    await _write_memory(path, buf.getbuffer())


async def _write_memory(path: Path, memory: memoryview):
    async with aiofiles.open(path, "wb") as file:
        await file.write(memory)
