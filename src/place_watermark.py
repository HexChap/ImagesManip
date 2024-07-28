from PIL.ImageFile import ImageFile, Image

from src.core import get_watermark_settings


def place_watermarks(images: list[ImageFile], watermark: ImageFile):
    for image in images:
        place_watermark(image, watermark)


def place_watermark(image: ImageFile, watermark: ImageFile):
    watermark = _get_resized_watermark(image.size, watermark)
    offset = _get_watermark_offset(image.size, watermark)
    mask = _get_watermark_opacity_mask(watermark)

    image.paste(watermark, box=offset, mask=mask)


def _get_watermark_opacity_mask(wmark: Image.Image) -> Image.Image:
    opacity = get_watermark_settings()["transparency_percent"]
    alpha = wmark.getchannel("A")

    return alpha.point(lambda a: a * opacity / 100)


def _get_resized_watermark(size: tuple[int, int], watermark: Image.Image) -> Image.Image:
    width = _calc_watermark_width(size[0], size[1])
    return _resize_with_proportion(watermark, width)


def _get_watermark_offset(size: tuple[int, int], watermark: Image.Image) -> tuple[int, int]:
    x = (size[0] // 2) - (watermark.width // 2)
    y = (size[1] // 2) - (watermark.height // 2)

    return x, y


def _resize_with_proportion(im: Image.Image, base_width: int):
    ratio = (base_width / float(im.width))
    height = int(
        float(im.height) * float(ratio)
    )
    return im.resize((base_width, height), Image.Resampling.LANCZOS)


def _calc_watermark_width(width: int, height: int) -> int:
    """
    Calculates watermark's width according to the image it will be applied to.

    :param width:int: Image's width
    :param height:int: Image's height
    :return:int: calculated width
    """
    return int(width * (0.20 if width > height else 0.40))  # TODO: Better approach?
