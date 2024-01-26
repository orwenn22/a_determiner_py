import pygame
from . import entityobject
from .. import utils


class ObjectManager():
    def __init__(self):
        self.nb_object: int = 0
        self.list_object: list[entityobject.EntityObject] = []

    def add_object(self, some_object: entityobject.EntityObject):
        assert entityobject.EntityObject.__subclasscheck__(type(some_object)), "ObjectManager : Trying to add something that is not an entity object."
        if some_object in self.list_object:
            return
        self.list_object.append(some_object)
        self.nb_object += 1
        some_object.manager = self

    def remove_object(self, some_object: entityobject):
        if some_object in self.list_object:
            self.list_object.remove(some_object)
            self.nb_object -= 1
            # TODO : remove the reference to the manager of some_object here maybe ?

    def update(self, dt: float):
        # This is a while loop on purpose in order to not break the iterator if an object
        # destruct another one
        i = 0
        while i < self.nb_object:
            self.list_object[i].update(dt)
            i += 1

    def draw(self):
        for i in self.list_object:
            i.draw()

    def get_collision(self, current_object: entityobject.EntityObject, object_type: type = entityobject.EntityObject) -> list[entityobject.EntityObject]:
        """
        Get all the objects of a specific type (include subclasses) that are colliding with a specific object
        :param current_object: The object we are looking collisions for
        :param object_type: The type of objects we want to look for collisions
        """
        result = []
        current_object_rect = current_object.get_rectangle()
        for i in self.list_object:
            if i == current_object or not isinstance(i, object_type):
                continue
            i_rect = i.get_rectangle()
            if utils.check_collision_rectangles(current_object_rect, i_rect):
                result.append(i)
        return result
