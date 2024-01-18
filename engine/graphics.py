"""
The goal of this file is to draw stuff on the window using meters as a metric.
For pixel graphics, we should use pygame's natives API calls.
"""

import pygame

from . import globals as g
from . import metrics as m
# we can delete the next line it's just to avoid having my linter crying
from engine.object.entityobject import EntityObject

print("graphics module instantiated")


def draw_rectangle(x: float, y: float, w: float, h: float, c, fill=True):
    """
    Take rec in meters
    :param x: x position in meter
    :param y: y position in meter
    :param w: width in meter
    :param h: height in meter
    :param c: color
    :return: nothing
    """
    origin_vec = m.meters_position_to_window_position(
        pygame.math.Vector2(x, y))
    pixel_x = int(origin_vec.x)
    pixel_y = int(origin_vec.y)
    pixel_width = m.meters_to_pixels(w)
    pixel_height = m.meters_to_pixels(h)

    # print(pixel_x, pixel_y, pixel_width, pixel_height)
    pygame.draw.rect(g.window, c, (pixel_x, pixel_y, pixel_width,
                     pixel_height), width=(0 if fill else 1))


def draw_line(start: pygame.math.Vector2, end: pygame.math.Vector2, c):
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
        draw_line(pygame.math.Vector2(-10, y),
                  pygame.math.Vector2(10, y), (0, 0, 255))
    for x in range(-10, 11):
        draw_line(pygame.math.Vector2(x, -10),
                  pygame.math.Vector2(x, 10), (0, 0, 255))


def draw_circle(center: pygame.math.Vector2, radius: float, c):
    """
    Draw a circle using meters unit
    :param center: position of the center
    :param radius: radius in meter
    :param c: color
    :return: nothing
    """
    pygame.draw.circle(g.window, c, m.meters_position_to_window_position(
        center), m.meters_to_pixels(radius))


def draw_sprite(sprite: pygame.Surface, rect_to_draw: tuple[float, float, float, float]):
    origin_vec = m.meters_position_to_window_position(
        pygame.Vector2(rect_to_draw[0], rect_to_draw[1]))
    x = int(origin_vec.x)
    y = int(origin_vec.y)
    width = m.meters_to_pixels(rect_to_draw[2])
    height = m.meters_to_pixels(rect_to_draw[3])
    space_to_draw = (x, y, width, height)
    g.window.blit(sprite, space_to_draw, space_to_draw)
