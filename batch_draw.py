# draw images on Minecraft Java Edition
# usage: python batch_draw.py <config_set_indices>
#   config_set_indices: 0, 1, 2, ...
#   ex. python batch_draw.py 2 0 5 1
#   The configuration sets are defined in batch_list.yml.

import sys
from time import sleep
import yaml
# mc-remote
from mc_remote.minecraft import Minecraft
import param_MCJE as param
from param_MCJE import PLAYER_ORIGIN as po
# image converter
from image_to_mc import convert_to_block_ids


def start_mc_remote_session():
    mc = Minecraft.create(address=param.ADRS_MCR, port=param.PORT_MCR)
    result = mc.setPlayer(param.PLAYER_NAME, po.x, po.y, po.z)
    if "Error" in result:
        sys.exit()
    else:
        print(result)
    mc.postToChat("image to minecraft")
    return mc


def draw_image(mc, block_ids,
               block_count_axis1, block_count_axis2,
               x0, y0, z0, view_from):
    for axis2 in range(block_count_axis2):
        for axis1 in range(block_count_axis1):
            if view_from == "y":  # looking down on the ground, or on x-z plane.
                block_id = block_ids[axis2][axis1]
                x, y, z = x0 + axis1, y0, z0 + axis2
            elif view_from == "x":  # on z-y plane, viewed from positive x.
                block_id = block_ids[block_count_axis2 - axis2 - 1][axis1]
                x, y, z = x0, y0 + axis2, z0 + axis1
            elif view_from == "z":  # on x-y plane, viewed from positive z.
                block_id = block_ids[block_count_axis2 - axis2 - 1][axis1]
                x, y, z = x0 + axis1, y0 + axis2, z0
            else:
                print("Invalid view_from option. Set to 'y', 'x', or 'z'.")
                sys.exit()
            mc.setBlock(x, y, z, block_id)
            print(po.x + x, po.y + y, po.z + z, block_id)
            sleep(0.001)


def load_config(_config_set):
    with open("batch_list.yml", "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)
    return config["config_sets"][_config_set]


def main(_config_set):
    config = load_config(_config_set)

    img_path = config["image"]["img_path"]
    block_size = config["size_ratio"]["block_size"]
    view_from = config["location"]["view_from"]
    x0 = config["location"]["x0"]
    y0 = config["location"]["y0"]
    z0 = config["location"]["z0"]
    contrast_ratio = config["image_adjust"]["contrast_ratio"]
    brightness_offset = config["image_adjust"]["brightness_offset"]
    color_map_path = config["color_map"]["color_map_path"]

    mc = start_mc_remote_session()

    block_ids, block_count_axis1, block_count_axis2 = convert_to_block_ids(
        original_image_path=img_path,
        block_size=block_size,
        contrast_ratio=contrast_ratio,
        brightness_offset=brightness_offset,
        color_map_path=color_map_path,
    )

    draw_image(mc, block_ids,
               block_count_axis1, block_count_axis2,
               x0, y0, z0, view_from)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python mcimg.py <config_set_indices>")
        sys.exit(1)

    config_set_indices = [int(arg) for arg in sys.argv[1:]]
    for config_set in config_set_indices:
        main(config_set)
