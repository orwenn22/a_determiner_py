import entityobject
from graphics import draw_rectangle,draw_sprite
import pygame
from metrics import meters_to_pixels


class ObjectManager():
    def __init__(self):
        self.nb_object: int = 0
        self.list_object: list = []

    def AddObject(self, some_object: entityobject.EntityObject):
        if some_object.sprite_path != "":
            self.list_object.append((some_object, pygame.transform.scale(pygame.image.load(
                some_object.sprite_path), (meters_to_pixels(some_object.width), meters_to_pixels(some_object.height)))))
        else:
            self.list_object.append(some_object)
        self.nb_object += 1

    def draw(self, color: tuple[int, int, int] = (255, 255, 255)):
        for i in self.list_object:
            if len(i) == 1:
                one_object = i[0].get_rectangle()
                sprite = ""
            else:
                one_object = i[0].get_rectangle()
                sprite = i[1]
            draw_rectangle(one_object[0], one_object[1],
                           one_object[2], one_object[3], color)
            if sprite != "":
                draw_sprite(sprite, one_object)

    def get_collision(self, item_moving: entityobject.EntityObject) -> tuple[bool, entityobject.EntityObject]:
        item_moving_rect = item_moving.get_rectangle()
        for i in self.list_object:
            i_rect = i[0].get_rectangle()
            if i != item_moving and ((item_moving_rect[0] < i_rect[0] + i_rect[2]) and (item_moving_rect[0] + item_moving_rect[2] > i_rect[0])) and ((item_moving_rect[1] < (i_rect[1] + i_rect[3]) and (item_moving_rect[1] + item_moving_rect[3]) > i_rect[1])):
                return True, i
        return False, item_moving
