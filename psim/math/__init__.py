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
    
    def normalize(self):
        mag = self.magnitude()
        self.x = self.x / mag
        self.y = self.y / mag
        return self

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
        elif isinstance(other, tuple):
            return Vector2D(self.x + other[0], self.y + other[1])
        else:
            raise TypeError(f"Cannot add Vector2D and {type(other).__name__}")

    def __radd__(self, other):
        if isinstance(other, Vector2D):
            return Vector2D(self.x + other.x, self.y + other.y)
        elif isinstance(other, tuple):
            return Vector2D(self.x + other[0], self.y + other[1])
        else:
            raise TypeError(f"Cannot add Vector2D and {type(other).__name__}")
        
    def __sub__(self, other):
        if isinstance(other, Vector2D):
            return Vector2D(self.x - other.x, self.y - other.y)
        elif isinstance(other, tuple):
            return Vector2D(self.x - other[0], self.y - other[1])
        else:
            raise TypeError(f"Cannot add Vector2D and {type(other).__name__}")
    
    def __rsub__(self, other):
        if isinstance(other, Vector2D):
            return Vector2D(self.x - other.x, self.y - other.y)
        elif isinstance(other, tuple):
            return Vector2D(self.x - other[0], self.y - other[1])
        else:
            raise TypeError(f"Cannot add Vector2D and {type(other).__name__}")

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
    
class Vector2DRot(Vector2D):
    def __init__(self, distance, angle):
        super().__init__(math.cos(angle) * distance, math.sin(angle) * distance)
        self.angle = angle
        self.dist = distance

    def __add__(self, other):
        if isinstance(other, Vector2DRot):
            return Vector2DRot(math.sqrt((self.x + other.x)**2 + (self.y + other.y)**2), \
                               math.atan2(self.y + other.y, self.x + other.x))
        elif isinstance(other, tuple):
            return Vector2DRot(self.dist + other[0], self.angle + other[1])
        else:
            raise TypeError(f"Cannot add Vector2DRot and {type(other).__name__}")

    def __radd__(self, other):
        if isinstance(other, Vector2DRot):
            return Vector2DRot(self.dist + other.dist, self.angle + other.angle)
        elif isinstance(other, tuple):
            return Vector2DRot(self.dist + other[0], self.angle + other[1])
        else:
            raise TypeError(f"Cannot add Vector2DRot and {type(other).__name__}")
        
    def __sub__(self, other):
        if isinstance(other, Vector2DRot):
            return Vector2DRot(self.dist - other.dist, self.angle - other.angle)
        elif isinstance(other, tuple):
            return Vector2DRot(self.dist - other[0], self.angle - other[1])
        else:
            raise TypeError(f"Cannot add Vector2DRot and {type(other).__name__}")

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
        self._field = np.empty(self._field_size, dtype=np.object)
        self._poi = []
    
    def __getitem__(self, key):
        return self._field[key]

    def _get_index_of_vector(self, vec: Vector):
        index = vec[0] + (vec[1] * (self._adj_dims[0]))
        return index
    
    def _translate_to_local(self, vec: Vector):
        return Vector2D(math.floor(vec[0]/self.resolution), math.floor(vec[1]/self.resolution))

    def swap(self, indx1, indx2):
        c1 = self.get(indx1)
        c2 = self.get(indx2)
        if c1 and c2:
            self._field[indx1] = c2
            self._field[indx2] = c1

    def set(self, index, obj):
        if self.get(index):
            self._field[index] = obj
    
    def insert(self, position: Vector, object):
        posSize = len(position)
        fieldSize = len(self.dims)
        if posSize != fieldSize:
            return
        loc = self._get_index_of_vector(position)
        self._field[loc] = object
        self._poi.append(loc)
    
    def get(self, indx = None, vec = None):
        if vec != None:
            i, res = self.valueAt(vec)
            # If valueAt returns an index, then we know the result is valid regardless of its type.
            if i:
                return (i, res)
            res = self._get_index_of_vector(vec)
            if res < len(self._field):
                return res, self._field[res]
            else:
                return (None, None)
        if indx == None:
            return enumerate(self._field)
        if indx >= 0 and indx < len(self._field):
            return indx,self._field[indx]

    def getNeighborIndices(self, index):
        toCheck = []
        val = index + self._adj_dims[0]
        # Above and Below
        if val + 1 < len(self._field):
            toCheck.append(val)
        val = index - self._adj_dims[0]
        if val >= 0:
            toCheck.append(val)
    
        # Left and Right
        if index % self._adj_dims[0] != 0:
            toCheck.append(index - 1)
            val = index - 1 - self._adj_dims[0]
            if val >= 0:
                toCheck.append(val)
            val = index - 1 + self._adj_dims[0]
            if val + 1 < len(self._field):
                toCheck.append(val)

        if index % self._adj_dims[0] != self._adj_dims[0] - 1:
            toCheck.append(index + 1)
            val = index + 1 - self._adj_dims[0]
            if val >= 0:
                toCheck.append(val)
            val = index + 1 + self._adj_dims[0]
            if val + 1 < len(self._field):
                toCheck.append(val)
        return toCheck

    # Attempts to get value of vector 
    def valueAt(self, vec: Vector, translate = True):
        if vec[0] <= self.dims[0] and vec[1] <= self.dims[1]:
            if translate:
                vec = self._translate_to_local(vec)
            index = self._get_index_of_vector(vec)
            if index < len(self._field):
                val = self._field[index]
                return (index, val)
        return None, None

    def getCoordsAt(self, index, translate = False):
        if translate:
            return ((index % self._adj_dims[0]) * self.resolution, (index // self._adj_dims[0]) * self.resolution)
        return (index % self._adj_dims[0], (index // self._adj_dims[0]))
