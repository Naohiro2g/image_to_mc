# image_to_mc module returns block ID list
# convert_to_block_ids(original_image_path: str,
#                      block_size: int,
#                      contrast_ratio: float = 1.0,
#                      brightness_offset: float = 0.0,
#                      color_map_path: str = "color_map_rgb.json",
#                      ) -> list[list[str]]:

import json
from PIL import Image, ImageEnhance


def _get_block_name(pixel: tuple, blocks: list[dict]) -> str:
    """
    Returns the name of the block that matches the given pixel color the closest.
    """
    matching_block_id = "none"
    smallest_value = float("inf")
    for block in blocks:
        r = abs(pixel[0] - block["r"])
        g = abs(pixel[1] - block["g"])
        b = abs(pixel[2] - block["b"])

        if r + g + b < smallest_value:
            smallest_value = r + g + b
            matching_block_id = block["block_id"]
    return matching_block_id


def _calculate_average_pixel_color(
    image: Image, x: int, y: int, block_size: int
) -> list[int]:
    """
    Calculates the average RGB values of a block in the given image.
    """
    pixel_sum = [0, 0, 0]  # Initialize sum of pixel values for RGB channels

    # Iterate over the block area
    for block_y in range(y, y + block_size):
        for block_x in range(x, x + block_size):
            pixel = image.getpixel((block_x, block_y))
            pixel_sum[0] += pixel[0]  # Add red value
            pixel_sum[1] += pixel[1]  # Add green value
            pixel_sum[2] += pixel[2]  # Add blue value

    pixel_count = block_size * block_size
    average_pixel = [
        pixel_sum[0] // pixel_count,
        pixel_sum[1] // pixel_count,
        pixel_sum[2] // pixel_count,
    ]

    return average_pixel


def _adjust_image(
    image: Image, contrast_ratio: float, brightness_offset: float
) -> Image:
    """
    Adjusts the contrast and brightness of the image.
    """
    # Adjust contrast
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(contrast_ratio)

    # Adjust brightness
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(1 + brightness_offset)

    return image


def convert_to_block_ids(
    original_image_path: str,
    block_size: int,
    contrast_ratio: float = 1.0,
    brightness_offset: float = 0.0,
    color_map_path: str = "color_map_rgb.json",
) -> list[list[str]]:
    with open(color_map_path, "r", encoding="utf-8") as data:
        blocks = json.loads(str(data.read()))

    original_image = Image.open(original_image_path)
    original_image = _adjust_image(original_image, contrast_ratio, brightness_offset)

    width, height = original_image.size
    block_count_x = width // block_size
    block_count_y = height // block_size
    print(block_count_x, block_count_y)
    area_avarage_pixel = []

    # Iterate over the blocks in the image
    for y in range(block_count_y):
        for x in range(block_count_x):
            average_color = _calculate_average_pixel_color(
                original_image, x * block_size, y * block_size, block_size
            )
            area_avarage_pixel.append(average_color)

    block_ids = []
    # Iterate over the blocks in the main image
    for y in range(block_count_y):
        row = []
        for x in range(block_count_x):
            block_name = _get_block_name(
                area_avarage_pixel[x + y * block_count_x], blocks
            )
            row.append(block_name)
        block_ids.append(row)

    return block_ids, block_count_x, block_count_y
