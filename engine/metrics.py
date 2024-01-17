"""
The goal of this file is to convert meters positions to pixel on the screen
"""

import pygame

print("metrics module instantiated")

pixels_per_meter = 50

# absolute position of the origin on the window in pixel
# if it is equal to {40, 40} then the entire content will be shifter a bit towards the down-right direction
x_offset_pixel = 0
y_offset_pixel = 0


def window_position_to_meters_position(x: int, y: int) -> pygame.math.Vector2:
    """
    Convert pixel coordinates on the window to a meters position in the world
    :param x: x position on the window
    :param y: y position on the window
    :return: vector with relative position in meters  (from the origin/offset)
    """
    relative_x = x - x_offset_pixel
    relative_y = y - y_offset_pixel
    return pygame.math.Vector2(relative_x / pixels_per_meter, relative_y / pixels_per_meter)


def meters_position_to_window_position(position: pygame.math.Vector2) -> pygame.math.Vector2:
    """
    Convert meters position to absolute pixel coordinates on the window
    :param position: position in meters
    :return:vector with position in absolute pixels
    """
    relative_x = int(position.x * pixels_per_meter)
    relative_y = int(position.y * pixels_per_meter)
    return pygame.math.Vector2(relative_x + x_offset_pixel, relative_y + y_offset_pixel)


def pixels_to_meters(pixels: int) -> float:
    """
    Convert an amount of pixel (ex : distance) from pixels to meters
    :param pixels: amount of pixels
    :return: length in meters
    """
    return float(pixels)/float(pixels_per_meter)


def meters_to_pixels(meters: float) -> int:
    """
    Convert meters to pixels
    :param meters: distance in meters
    :return: length in pixel
    """
    return int(meters*pixels_per_meter)
