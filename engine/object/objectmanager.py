import pygame
import entityobject


class ObjectManager():
    def __init__(self):
        self.nb_object: int = 0
        self.list_object: list[entityobject.EntityObject] = []

    def add_object(self, some_object: entityobject.EntityObject):
        self.list_object.append(some_object)
        self.nb_object += 1

    def update(self, dt: float):
        # This is a while loop on purpose in order to not break the iterator if an object
        # destruct another one
        i = 0
        while i < self.nb_object:
            self.list_object[i].update(dt)
            i+=1

    def draw(self):
        for i in self.list_object:
            i.draw()

    def get_collision(self, item_moving: entityobject.EntityObject) -> tuple[bool, entityobject.EntityObject]:
        item_moving_rect = item_moving.get_rectangle()
        for i in self.list_object:
            i_rect = i.get_rectangle()
            if i != item_moving and ((item_moving_rect[0] < i_rect[0] + i_rect[2]) and (item_moving_rect[0] + item_moving_rect[2] > i_rect[0])) and ((item_moving_rect[1] < (i_rect[1] + i_rect[3]) and (item_moving_rect[1] + item_moving_rect[3]) > i_rect[1])):
                return True, i
        return False, item_moving
