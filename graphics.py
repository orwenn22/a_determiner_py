"""
The goal of this file is to convert meters positions to pixel on the screen
"""

import pygame

import globals as g

pixels_per_meter = 50

# absolute position of the origin on the window
x_offset_pixel = 0
y_offset_pixel = 0

def draw_rectangle(x, y, w, h, c):
    """
    Take rec in meters
    :param x: x position in meter
    :param y: y position in meter
    :param w: width in meter
    :param h: height in meter
    :param c: color
    :return: nothing
    """
    pixel_x = x * pixels_per_meter + x_offset_pixel
    pixel_y = y * pixels_per_meter + y_offset_pixel
    pixel_width = w * pixels_per_meter
    pixel_height = h * pixels_per_meter

    pygame.draw.rect(g.window, c, (pixel_x, pixel_y, pixel_width, pixel_height))


def draw_grid():
    """
    Draw a grid at the origin. Each square is 1*1 meter
    :return: nothing
    """

    # TODO : draw_line function with meter parameters ?
    for y in range(-10, 11):
        pygame.draw.line(
            g.window, (0, 0, 255),
            (-pixels_per_meter*10 + x_offset_pixel, y_offset_pixel + y*pixels_per_meter),
            (pixels_per_meter*10 + x_offset_pixel, y_offset_pixel + y*pixels_per_meter))

    for x in range(-10, 11):
        pygame.draw.line(
            g.window, (0, 0, 255),
            (x_offset_pixel + x*pixels_per_meter, -pixels_per_meter*10 + y_offset_pixel),
            (x_offset_pixel + x*pixels_per_meter, pixels_per_meter*10 + y_offset_pixel))
