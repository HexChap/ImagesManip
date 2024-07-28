import asyncio
from io import BytesIO
from pathlib import Path

import aiofiles
from PIL.ImageFile import ImageFile

from src.core import get_paths

output_path = Path(get_paths()["output"])


async def save_images(images: list[ImageFile]):
    async with asyncio.TaskGroup() as tg:
        for image in images:
            tg.create_task(save_image(image))


async def save_image(image: ImageFile):
    """
    Asynchronously saves images.

    :param image: Image to save
    :return:
    """
    path = output_path / Path(image.filename).name

    image = image.convert("RGB")
    image.save(buf := BytesIO(), format="JPEG")

    await _write_memory(path, buf.getbuffer())


async def _write_memory(path: Path, memory: memoryview):
    async with aiofiles.open(path, "wb") as file:
        await file.write(memory)
