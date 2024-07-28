from PIL.ImageFile import ImageFile, Image

from src.core import get_watermark_settings

path, opacity_percent = get_watermark_settings().values()
watermark = Image.open(path)


def place_watermarks(images: list[ImageFile]):
    for image in images:
        place_watermark(image)


def place_watermark(image: ImageFile):
    wmark = _get_resized_watermark(*image.size)
    offset = _get_watermark_offset(*image.size)
    mask = _get_watermark_opacity_mask(wmark)

    image.paste(wmark, box=offset, mask=mask)


def _get_watermark_opacity_mask(wmark: Image.Image) -> Image.Image:
    alpha = wmark.getchannel("A")

    return alpha.point(lambda a: a * opacity_percent / 100)


def _get_resized_watermark(width: int, height: int) -> Image.Image:
    width = _calc_watermark_width(width, height)
    return _resize_with_proportion(watermark, width)


def _get_watermark_offset(width: int, height: int) -> tuple[int, int]:
    x = (width // 2) - (watermark.width // 2)
    y = (height // 2) - (watermark.height // 2)

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
