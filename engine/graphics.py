"""
The goal of this file is to draw stuff on the window using meters as a metric.
For pixel graphics, we should use pygame's natives API calls.
"""

import math
import pygame

from . import globals as g
from . import metrics as m


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


def draw_sprite(sprite: pygame.Surface, position: pygame.math.Vector2) -> None:
    """
    This is mostly intended for drawing a precached - prescaled - texture.
    """
    origin_vec = m.meters_position_to_window_position(position)
    x = int(origin_vec.x)
    y = int(origin_vec.y)
    width = sprite.get_width()
    height = sprite.get_height()
    #  (after testing, this increase performance by about 30% if a lot of objects are of screen)
    if x+width < 0 or y+height < 0 or x >= g.window.get_width() or y >= g.window.get_height():
        return
    g.window.blit(sprite, (x, y))


def draw_sprite_big(sprite: pygame.Surface, position: pygame.math.Vector2):
    origin_vec = m.meters_position_to_window_position(position)
    x = int(origin_vec.x)
    y = int(origin_vec.y)
    width = sprite.get_width()
    height = sprite.get_height()
    if x+width < 0 or y+height < 0 or x >= g.window.get_width() or y >= g.window.get_height():
        return

    offset_x = 0
    if x < 0:
        offset_x = -x
        x = 0

    offset_y = 0
    if y < 0:
        offset_y = -y
        y = 0

    area_w = width - offset_x
    if area_w + x >= g.window.get_width():
        area_w = g.window.get_width() - x

    area_h = height - offset_y
    if area_h + y >= g.window.get_height():
        area_h = g.window.get_height() - y

    print((offset_x, offset_y, area_w, area_h))
    g.window.blit(sprite, (x, y), (offset_x, offset_y, area_w, area_h))


def draw_sprite_scale(sprite: pygame.Surface, rect_to_draw: tuple[float, float, float, float]):
    """
    This will scale the sprite to fill the rectangle
    """
    origin_vec = m.meters_position_to_window_position(pygame.Vector2(rect_to_draw[0], rect_to_draw[1]))
    x = int(origin_vec.x)
    y = int(origin_vec.y)
    width = m.meters_to_pixels(rect_to_draw[2])
    height = m.meters_to_pixels(rect_to_draw[3])
    # This is efficient because we check this before applying transformations
    if x+width < 0 or y+height < 0 or x >= g.window.get_width() or y >= g.window.get_height():
        return
    space_to_draw = (x, y, width, height)
    scaled_surface = pygame.transform.scale(sprite, (width, height))
    g.window.blit(scaled_surface, space_to_draw)


def draw_sprite_rot(sprite: pygame.Surface, position: pygame.math.Vector2, size: pygame.math.Vector2, rotation: float):
    """
    Draw a sprite using a position and rotation
    :param sprite: the sprite we want to draw
    :param position: center of where we want to draw the sprite (in m position)
    :param size: size at which we want to draw the sprite (in m)
    :param rotation: angle
    :return:
    """
    pixel_pos = m.meters_position_to_window_position(position)
    x = int(pixel_pos.x)
    y = int(pixel_pos.y)
    width = m.meters_to_pixels(size.x)
    height = m.meters_to_pixels(size.y)

    # This is efficient because we check this before applying transformations
    half_diagonal = math.sqrt(width*width + height*height) / 2
    if x+half_diagonal < 0 or y+half_diagonal < 0 or x-half_diagonal >= g.window.get_width() or y-half_diagonal >= g.window.get_height():
        return

    scaled_surface = pygame.transform.scale(sprite, (width, height))
    rotated_surface = pygame.transform.rotate(scaled_surface, rotation)
    size_rec = rotated_surface.get_rect()

    # Currently, x and y are storing the position of the middle, however the pygame blit API take the top left position.
    # Therefore, we want to actually calculate this position using the size of the resulting surface
    x -= int(size_rec.width / 2)
    y -= int(size_rec.height / 2)

    # print((x, y, size_rec.width, size_rec.height))
    g.window.blit(rotated_surface, (x, y, size_rec.width, size_rec.height))