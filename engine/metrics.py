"""
The goal of this file is to convert meters positions to pixel on the screen
"""

import pyray
from engine import globals as g

print("metrics module instantiated")

# This should not be modified directly. Instead, set_pixels_per_meter() should be used.
pixels_per_meter = 50

# absolute position of the origin on the window in pixel
# if it is equal to {40, 40} then the entire content will be shifter a bit towards the down-right direction
x_offset_pixel = 0
y_offset_pixel = 0


def set_pixels_per_meter(new_pixels_per_meter: int):
    """
    Set a new pixels per meter value. Will set zoom_changed to True.
    If we need to change the amount of pixels per meters, this should be called before updating objects, as early as
    possible in the game loop.
    """
    global pixels_per_meter
    # We do this because some stuff might rely on zoom_changed to update their cached texture. Therefore, we don't want
    # to reload their cache if the length didn't change. (also prevent negative size and 0 here, because why not)
    if pixels_per_meter == new_pixels_per_meter or new_pixels_per_meter <= 0:
        return

    previous_center = get_camera_center()
    pixels_per_meter = new_pixels_per_meter
    g.zoom_changed = True
    set_camera_center(previous_center)


def set_camera_center(position: pyray.Vector2):
    """
    Set the position of the center of the "camera"
    :param position: new position in meter
    """
    global x_offset_pixel, y_offset_pixel
    distance_x = meters_to_pixels(position.x)
    distance_y = meters_to_pixels(position.y)
    # print("Relative position from center :", distance_x, distance_y)
    x_offset_pixel = -distance_x + int(pyray.get_screen_width()/2)
    y_offset_pixel = -distance_y + int(pyray.get_screen_height()/2)
    # print("New calculated camera pos :", x_offset_pixel, y_offset_pixel)


def get_camera_center() -> pyray.Vector2:
    return window_position_to_meters_position(int(pyray.get_screen_width()/2), int(pyray.get_screen_height()/2))


def window_position_to_meters_position(x: int, y: int) -> pyray.Vector2:
    """
    Convert pixel coordinates on the window to a meters position in the world
    :param x: x position on the window
    :param y: y position on the window
    :return: vector with relative position in meters  (from the origin/offset)
    """
    relative_x = x - x_offset_pixel
    relative_y = y - y_offset_pixel
    return pyray.Vector2(relative_x / pixels_per_meter, relative_y / pixels_per_meter)


def meters_position_to_window_position(position: pyray.Vector2) -> pyray.Vector2:
    """
    Convert meters position to absolute pixel coordinates on the window
    :param position: position in meters
    :return:vector with position in absolute pixels
    """
    relative_x = int(position.x * pixels_per_meter)
    relative_y = int(position.y * pixels_per_meter)
    return pyray.Vector2(relative_x + x_offset_pixel, relative_y + y_offset_pixel)


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
