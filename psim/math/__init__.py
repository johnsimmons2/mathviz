from abc import abstractmethod
import math
import numpy as np
import matplotlib.pyplot as plt


class Vector:
    def __init__(self):
        pass
    
    @abstractmethod
    def __len__(self):
        pass

    @abstractmethod
    def magnitude(self):
        pass

    @abstractmethod
    def __getitem__(self, key):
        pass

class Vector2D(Vector):
    def __init__(self, x = 0, y = 0, dims: tuple = None):
        super().__init__()
        if dims != None:
            self.x = dims[0]
            self.y = dims[1]
        else:
            self.x = x
            self.y = y
    
    def __len__(self):
        return 2
    
    def __getitem__(self, key):
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        else:
            raise IndexError("Index out of Bounds")
    
    def magnitude(self):
        return math.sqrt((self.x**2) + (self.y**2))

    def __eq__(self, other):
        if other:
            if self.x == other.x and self.y == other.y:
                return True
        return False
    
    def __truediv__(self, other):
        if isinstance(other, Vector2D):
            return Vector2D(self.x / other.x, self.y / other.y)
        else:
            return Vector2D(self.x / other, self.y / other)
    
    def __floordiv__(self, other):
        if isinstance(other, Vector2D):
            return Vector2D(self.x / other.x, self.y / other.y)
        else:
            return Vector2D(self.x / other, self.y / other)

    def __mul__(self, other):
        if isinstance(other, Vector2D):
            return Vector2D(self.x * other.x, self.y * other.y)
        else:
            return Vector2D(self.x * other, self.y * other)

    def __add__(self, other):
        if isinstance(other, Vector2D):
            return Vector2D(self.x + other.x, self.y + other.y)
        else:
            return Vector2D(self.x + other, self.y + other)
    
    def __radd__(self, other):
        if isinstance(other, Vector2D):
            return Vector2D(self.x + other.x, self.y + other.y)
        else:
            return Vector2D(self.x + other, self.y + other)

    def __str__(self):
        if self.x == 0 and self.y == 0:
            return f"<->"
        return f"<{self.x}, {self.y}>"
    
    def __repr__(self):
        if self.x == 0 and self.y == 0:
            return f"-"
        return f"<{self.x}, {self.y}>"

## VectorPairList: tuple of Vector2D
##  first index is position, second is velocity
class VectorPairList(list):
    def __init__(self, iterable):
        super().__init__((self.__type_check(item) for item in iterable))
    
    def __setitem__(self, index, item):
        super().__setitem__(index, self.__type_check(item))

    def insert(self, index, item):
        super().insert(index, self.__type_check(item))

    def append(self, item):
        super().append(self.__type_check(item))

    def get(self, x, y=None):
        result = self[x]
        if y != None:
            result = result[y]
        return result
    
    def __type_check(self, item):
        if isinstance(item, tuple):
            if len(item) == 2:
                if isinstance(item[0], Vector2D) and isinstance(item[1], Vector2D):
                    return item
                else:
                    if len(item[0]) == 2 and len(item[1]) == 2:
                        return (Vector2D(item[0][0], item[0][1]), Vector2D(item[1][0], item[1][1]))
            elif len(item) == 4:
                return (Vector2D(item[0], item[1]), Vector2D(item[2], item[3]))
        raise TypeError(f"Tuple of Vector2D expected, got {type(item).__name__}")
    
    def __str__(self):
        result = '['
        for i, row in enumerate(self):
            result = result + f"{row}"
            if i < len(self) - 1:
                result = result + ', '
        return result + ']'
    
    def existsInPosition(self, item, pos):
        if pos > 1 or pos < 0:
            raise IndexError(f"Index out of bounds, 2D Vectors are only allowed.")
        for row in self:
            if row[pos] == item:
                return row
        return None
    
class Vector2DRot(Vector):
    def __init__(self, distance, angle):
        super().__init__()
        self.x = math.cos(angle) * distance
        self.y = math.sin(angle) * distance
        self.angle = angle
    
    def __len__(self):
        return 2
    
    def __getitem__(self, key):
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        else:
            raise IndexError("Index out of Bounds")

    def magnitude(self):
        return math.sqrt((self.x**2) + (self.y**2))

class Vector3D(Vector):
    def __init__(self, x, y, z):
        super().__init__()
        self.x = x
        self.y = y
        self.z = z
    
    def __len__(self):
        return 3
    
    def __getitem__(self, key):
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        elif key == 2:
            return self.z
        else:
            raise IndexError("Index out of Bounds")

    def magnitude(self):
        return math.sqrt((self.x**2) + (self.y**2) + (self.z**2))


class Field:
    def __init__(self, dims: Vector, resolution):
        self.dims = dims
        self._adj_dims = (dims[0]//resolution, dims[1]//resolution)
        self._field_size = (dims[0]//resolution) * (dims[1]//resolution)
        self.resolution = resolution
        self._field = [0 for _ in range(self._field_size)]
        self._poi = []
    
    def __getitem__(self, key):
        return self._field[key]

    def _get_local_position(self, vec: Vector):
        index = vec[0]+(vec[1]*self._adj_dims[0])
        return index
    
    def _translate_to_local(self, vec: Vector):
        return Vector2D(round(vec[0]/self.resolution), round(vec[1]/self.resolution))

    def insert(self, position: Vector, object):
        posSize = len(position)
        fieldSize = len(self.dims)
        if posSize != fieldSize:
            return
        loc = self._get_local_position(position)
        self._field[loc] = object
        self._poi.append(loc)
    
    def get(self):
        return enumerate(self._field)

    def getNeighborIndices(self, index):
        toCheck = []
        val = index + self._adj_dims[0]
        # Above and Below
        if val + 1 < len(self._field):
            toCheck.append(val)
        val = index - self._adj_dims[0]
        if val > 0:
            toCheck.append(val)
    
        # Left and Right
        if index % self._adj_dims[0] != 0:
            toCheck.append(index - 1)
            val = index - 1 - self._adj_dims[0]
            if val > 0:
                toCheck.append(val)
            val = index - 1 + self._adj_dims[0]
            if val + 1 < len(self._field):
                toCheck.append(val)
        if index % self._adj_dims[0] != self._adj_dims[0] - 1:
            toCheck.append(index + 1)
            val = index + 1 - self._adj_dims[0]
            if val > 0:
                toCheck.append(val)
            val = index + 1 + self._adj_dims[0]
            if val + 1 < len(self._field):
                toCheck.append(val)
        return toCheck

    # Attempts to get value of vector 
    def valueAt(self, vec: Vector):
        if vec[0] > self.dims[0] or vec[1] > self.dims[1]:
            return None
        index = self._get_local_position(self._translate_to_local(vec))
        val = self._field[index]
        return (index, val)

    def getCoordsAt(self, index):
        return (index % self._adj_dims[0], (index // self._adj_dims[0]))
