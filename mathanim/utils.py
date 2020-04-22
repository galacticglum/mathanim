import math
import functools
from colour import Color

def rgetattr(obj, name, *args):
    '''
    A recursive implementatin of the ``getattr`` function that supports "dot" notation.

    :param obj:
        The object whose attribute to get.
    :param name:
        The name of the attribute to get.
    
    '''
    def _getattr(obj, name):
        return getattr(obj, name, *args)

    return functools.reduce(_getattr, [obj] + name.split('.'))

def rsetattr(obj, name, value):
    '''
    A recursive implementatin of the ``setattr`` function that supports "dot" notation.

    :param obj:
        The object whose attribute to set.
    :param name:
        The name of the attribute to set.
    :param value:   
        The value to set the attribute to.

    '''
    
    pre, _, post = name.rpartition('.')
    return setattr(rgetattr(obj, pre) if pre else obj, post, value)

def convert_colour(value):
    '''
    Converts a value to a :class:`colour.Color` object.

    '''

    if isinstance(value, Color): return value
    return Color(value)

class Vector2:
    '''
    A two-dimensional Vector2.

    '''

    def __init__(self, x=0, y=0):
        '''
        Initializes an instance of :class:`Vector2`.

        :note:
            The first argument to this constructor can also be a tuple, list, or another Vector2.
            If it is a tuple or list, the first two elements are used to initialize the Vector2;
            otherwise, if it is a Vector2 object, the coordinates of the specified Vector2 are used.

        :param x:
            The x-coordinate of the position Vector2.
        :param y:
            The y-cooridnate of the position Vector2.

        '''

        # If the first argument to the constructor is a tuple, list
        # or another Vector2 object, we use that to initialize this Vector2.
        if isinstance(x, tuple) or isinstance(x, list):
            self.x, self.y = x
        elif isinstance(x, Vector2):
            self.x, self.y  = x.x, x.y
        else:
            self.x = x
            self.y = y

    @property    
    def magnitude(self):
        '''
        Gets the magnitude of this :class:`Vector2`.

        '''

        return math.sqrt(self.magnitude)

    @property
    def sqr_magnitude(self):
        '''
        Gets the square magnitude of this :class:`Vector2`.
        
        '''

        return self.x**2 + self.y**2

    def __add__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x + other.x, self.y + other.y)
        elif  isinstance(other, tuple) or isinstance(other, list):
            return Vector2(self.x + other[0], self.y + other[1])
        elif isinstance(other, int) or isinstance(other, float):
            return Vector2(self.x + other, self.y + other)
        else:
            return NotImplemented
    
    def __sub__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x - other.x, self.y - other.y)
        if  isinstance(other, tuple) or isinstance(other, list):
            return Vector2(self.x - other[0], self.y - other[1])
        elif isinstance(other, int) or isinstance(other, float):
            return Vector2(self.x - other, self.y - other)
        else:
            return NotImplemented

    def __rsub__(self, other):
        if isinstance(other, Vector2):
            return Vector2(other.x - self.x, other.y - self.y)
        elif  isinstance(other, tuple) or isinstance(other, list):
            return Vector2(other[0] - self.x, other[1] - self.y)
        elif isinstance(other, int) or isinstance(other, float):
            return Vector2(other - self.x, other - self.y)
        else:
            return NotImplemented
        
    def __mul__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x * other.x, self.y * other.y)
        elif  isinstance(other, tuple) or isinstance(other, list):
            return Vector2(self.x * other[0], self.y * other[1])
        elif isinstance(other, int) or isinstance(other, float):
            return Vector2(self.x * other, self.y * other)
        else:
            return NotImplemented
        
    def __truediv__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x / other.x, self.y / other.y)
        elif  isinstance(other, tuple) or isinstance(other, list):
            return Vector2(self.x / other[0], self.y / other[1])
        elif isinstance(other, int) or isinstance(other, float):
            return Vector2(self.x / other, self.y / other)
        else:
            return NotImplemented
    
    def __pow__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Vector2(self.x ** other, self.y ** other)
        else:
            return NotImplemented
    
    def __iadd__(self, other):
        if isinstance(other, Vector2):
            self.x += other.x
            self.y += other.y
            return self
        elif  isinstance(other, tuple) or isinstance(other, list):
            self.x += other[0]
            self.y += other[1]
            return self
        elif isinstance(other, int) or isinstance(other, float):
            self.x += other
            self.y += other
            return self
        else:
            return NotImplemented
        
    def __isub__(self, other):
        if isinstance(other, Vector2):
            self.x -= other.x
            self.y -= other.y
            return self
        elif  isinstance(other, tuple) or isinstance(other, list):
            self.x -= other[0]
            self.y -= other[1]
            return self
        elif isinstance(other, int) or isinstance(other, float):
            self.x -= other
            self.y -= other
            return self
        else:
            return NotImplemented
        
    def __imul__(self, other):
        if isinstance(other, Vector2):
            self.x *= other.x
            self.y *= other.y
            return self
        elif  isinstance(other, tuple) or isinstance(other, list):
            self.x *= other[0]
            self.y *= other[1]
            return self
        elif isinstance(other, int) or isinstance(other, float):
            self.x *= other
            self.y *= other
            return self
        else:
            return NotImplemented
        
    def __itruediv__(self, other):
        if isinstance(other, Vector2):
            self.x /= other.x
            self.y /= other.y
            return self
        elif  isinstance(other, tuple) or isinstance(other, list):
            self.x /= other[0]
            self.y /= other[1]
            return self
        elif isinstance(other, int) or isinstance(other, float):
            self.x /= other
            self.y /= other
            return self
        else:
            return NotImplemented
        
    def __ipow__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            self.x **= other
            self.y **= other
            return self
        else:
            return NotImplemented
    
    def __eq__(self, other):
        if isinstance(other, Vector2):
            return self.x == other.x and self.y == other.y
        else:
            return NotImplemented

    def __ne__(self, other):
        if isinstance(other, Vector2):
            return self.x != other.x or self.y != other.y
        else:
            return NotImplemented

    def __gt__(self, other):
        if isinstance(other, Vector2):
            return self.getLength() > other.getLength()
        else:
            return NotImplemented

    def __ge__(self, other):
        if isinstance(other, Vector2):
            return self.getLength() >= other.getLength()
        else:
            return NotImplemented

    def __lt__(self, other):
        if isinstance(other, Vector2):
            return self.getLength() < other.getLength()
        else:
            return NotImplemented
            
    def __le__(self, other):
        if isinstance(other, Vector2):
            return self.getLength() <= other.getLength()
        else:
            return NotImplemented
           
    def __eq__(self, other):
        if isinstance(other, Vector2):
            return self.x == other.x and self.y == other.y
        else:
            return NotImplemented

    def __neg__(self): return Vector2(-self.x, -self.y)
    def __str__(self): return '({}, {})'.format(x, y)

class BidirectionalMap(dict):
    '''
    A bidirectional dictionary. It supports key-value and value-key mapping.

    '''

    def __setitem__(self, key, value):
        if key in self:
            del self[key]
        
        if value in self:
            del self[value]

        dict.__setitem__(self, key, value)
        dict.__setitem__(self, value, key)
    
    def __delitem__(self, key):
        dict.__delitem__(self, self[key])
        dict.__delitem__(self, key)
    
    def __len__(self):
        return dict.__len__(self) // 2
    