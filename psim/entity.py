from abc import abstractmethod
from psim.math import Vector2D
import math

class Entity:
    def __init__(self, x, y):
        self.__position = Vector2D(x, y)
        self.debugmode = False
    
    @abstractmethod
    def display(self):
        pass

    @abstractmethod
    def update(self):
        pass

    def updatePosition(self, pos: Vector2D):
        self.__position = pos

    def getPosition(self):
        return self.__position
    
    def getIntPosition(self):
        x = math.floor(self.__position.x)
        y = math.floor(self.__position.y)
        return Vector2D(x, y)
