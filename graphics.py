"""
The goal of this file is to draw stuf on the window using meters as a metric.
For pixel graphics, we should use pygame's natives API calls.
"""

import pygame

import globals as g
import metrics as m


print("graphics module instantiated")


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
    origin_vec = m.meters_position_to_window_position(pygame.math.Vector2(x, y))
    pixel_x = int(origin_vec.x)
    pixel_y = int(origin_vec.y)
    pixel_width = m.meters_to_pixels(w)
    pixel_height = m.meters_to_pixels(h)

    #print(pixel_x, pixel_y, pixel_width, pixel_height)
    pygame.draw.rect(g.window, c, (pixel_x, pixel_y, pixel_width, pixel_height))


def draw_line(start: pygame.math.Vector2, end: pygame.math, c):
    """
    Draw a line using two point in meters
    :param start: start postion in meters
    :param end: end position in meters
    :param c: color
    :return: nothing
    """
    start_pixel = m.meters_position_to_window_position(start)
    end_pixel = m.meters_position_to_window_position(end)
    pygame.draw.line(g.window, c, start_pixel, end_pixel)

def draw_grid():
    """
    Draw a grid at the origin. Each square is 1*1 meter
    :return: nothing
    """
    # TODO : draw the grid only on the visible space of the window.
    for y in range(-10, 11):
        draw_line(pygame.math.Vector2(-10, y), pygame.math.Vector2(10, y), (0, 0, 255))
    for x in range(-10, 11):
        draw_line(pygame.math.Vector2(x, -10), pygame.math.Vector2(x, 10), (0, 0, 255))
