import pygame
import math

from engine import globals as g, graphics as gr
from engine.object import kinematicobject as ko

# TODO : move this in engine
#        and rename to KinematicPrediction ?

class TestObjPrediction(ko.KinematicObject):
    def __init__(self, x, y, w, h, mass, velocity, acceleration):
        """
        :param x: x posittion of the object
        :param y: y posittion of the object
        :param w: width
        :param h: height
        :param mass: mass in kg
        :param velocity: initial velocity in m/s
        :param acceleration: initial acceleration in m/s² (in most cases we probably want this to be {0, 0})
        """
        super().__init__(x, y, w, h, mass)
        self.velocity = pygame.Vector2(velocity.x, velocity.y)      # do this to copy velocity (and not store a ref)
        self.acceleration = pygame.Vector2(acceleration.x, acceleration.y)
        self.enable_physics = True

    @classmethod
    def from_other_object(cls, other: ko.KinematicObject):
        """
        Call the constructor using another object as a base
        NOTE : if we want to clear the acceleration, this should be done manually after the initialisation of the object
        :param other: the other object we want to "copy"
        :return: The prediction object
        """
        return cls(other.position.x, other.position.y, other.width, other.height, other.mass, other.velocity, other.acceleration)


    def draw_simulation(self, step: int, simulation_amount: int = 100, dt: float = 0.01):
        """
        :param step: if this is 5 this will draw every 5 points of the simulation
        :param simulation_amount: the number of time we want to simulate
        :param dt: the deltatime we want to simulate (can/should be something else than the ont calculated from FPS, default of 0.01, but can be smaller for higher accuracy)
        :return:
        """
        #Backup all physics state
        a = self.acceleration.copy()
        v = self.velocity.copy()
        p = self.position.copy()

        for i in range(0, simulation_amount):
            self.process_physics(dt)
            if i%step != 0: continue
            gr.draw_circle(self.position, 0.1, (100, 100, 255))

        self.acceleration = a
        self.velocity = v
        self.position = p
