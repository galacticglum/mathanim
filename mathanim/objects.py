from colour import Color
from abc import ABC, abstractmethod
from mathanim.utils import Vector2, convert_colour

class SceneObject(ABC):
    '''
    The base class for all objects which can be rendered in the scene.

    '''

    def __init__(self, position=None, rotation=0, scale=None, opacity=1):
        '''
        Initializes an instance of :class:`SceneObject`.

        :param position:
            The position of the object in the scene given as coordiantes in the scene's reference frame.
            Defaults to the zero vector (top-left corner of the screen).
        :param rotation:
            The rotation of the object, in radians. Defaults to 0.
        :param scale:
            The scale of the object. Defaults to the unit vector.
        :param opacity:
            The opacity of the object. Defaults to 1 (fully opaque).

        '''

        self.position = position if position is not None else Vector2()
        self.rotation = rotation
        self.scale = scale if scale is not None else Vector2(1, 1)
        self.opacity = opacity

    @abstractmethod
    def draw(self, render_context):
        '''
        Draw this object onto the specified :class:`cairo.Context`.

        :param:
            A :class:`cairo.Context` that this object will be rendered onto.

        '''

        pass

class Rectangle(SceneObject):
    '''
    A rectangle shape.

    '''

    def __init__(self, width=1, height=1, position=None, rotation=0, 
                scale=None, fill_colour='white', fill_opacity=1, 
                opacity=1):
        '''
        Initializes an instance of :class:`Rectangle`.

        :param width:
            The width of the rectangle. Defaults to 1 unit.
        :param height:
            The height of the rectangle. Defaults to 1 unit.
        :param position:
            The position of the centre of the rectangle given as coordiantes in the scene's 
            reference frame. Defaults to the zero vector (top-left corner of the screen).
        :param rotation:
            The rotation of the rectangle, in radians. Defaults to 0.
        :param scale:
            The scale of the rectangle. Defaults to the unit vector.
        :param fill_colour:
            The fill colour of the rectangle. Defaults to white.
            If set to ``None``, the rectangle has no fill.
        :param fill_opacity:
            The opacity of the rectangle fill. Defaults to 1 (fully opaque).
        :param opacity:
            The opacity of the rectangle. Defaults to 1 (fully opaque).
            This affects the WHOLE rectangle.

        '''

        super().__init__(position, rotation, scale, opacity)

        self.fill_colour = convert_colour(fill_colour)
        self.fill_opacity = fill_opacity
        self.size = Vector2(width, height)

    @property
    def size(self):
        '''
        The size of the rectangle as a two-dimensional vector.

        '''

        return self.__size

    @size.setter
    def size(self, value):
        '''
        Sets the size of the rectangle.

        :param value:
            A :class:`mathanim.utils.Vector2` whose x and y components represent
            the width and height of the rectangle respectively.

        '''

        self.__size = value
        self.__real_size = value * self.scale

    @property
    def width(self):
        '''
        The width of the rectangle.

        '''
        
        return self.size.x

    @property
    def height(self):
        '''
        The height of the rectangle.

        '''
        
        return self.size.y

    def draw(self, render_context):
        '''
        Draw this rectangle onto the specified :class:`cairo.Context`.

        :param:
            A :class:`cairo.Context` that this object will be rendered onto.

        '''

        half_size = self.__real_size / 2
        centre = self.position - half_size

        # Translate to the centre of the rectangle.
        render_context.translate(centre.x, centre.y)
        # Rotate about the centre of the rectangle in the new translated matrix.
        render_context.translate(half_size.x, half_size.y)
        render_context.rotate(self.rotation)
        render_context.translate(-half_size.x, -half_size.y)
        render_context.scale(self.scale.x, self.scale.y)

        # Draw the rectangle. We use the coordinate (0, 0) since the transformation matrix
        # has already been set to the position of the rectangle.
        render_context.rectangle(0, 0, self.width, self.height)
        if self.fill_colour is not None:
            render_context.set_source_rgba(*self.fill_colour.rgb, self.opacity * self.fill_opacity)
            render_context.fill()
        
