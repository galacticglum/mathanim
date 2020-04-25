import math
from colour import Color
from abc import ABC, abstractmethod
from mathanim.utils import Vector2, convert_colour, convert_vector2

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

        self.position = position
        self.rotation = rotation
        self.scale =  scale
        self.opacity = opacity

    @property
    def position(self):
        '''
        Gets the position of the object in the scene, given as coordiantes in the scene's reference frame.

        '''

        return self.__position

    @position.setter
    def position(self, value):
        '''
        Sets the position of the object in the scene.

        '''

        self.__position = Vector2() if value is None else convert_vector2(value)

    @property
    def scale(self):
        '''
        Gets the scale of the object.

        '''

        return self.__scale

    @scale.setter
    def scale(self, value):
        '''
        Sets the scale of the object.

        '''

        self.__scale = Vector2(1, 1) if value is None else convert_vector2(value)

    @abstractmethod
    def draw(self, render_context):
        '''
        Draw this object onto the specified :class:`cairo.Context`.

        :param:
            A :class:`cairo.Context` that this object will be rendered onto.

        '''

        # Implemented in subclasses
        pass

class Shape(SceneObject):
    '''
    The base class for all primitive shape objects.

    '''

    def __init__(self, position=None, rotation=0, scale=None, fill_colour='white', 
                 fill_opacity=1, border_radius=0, stroke_colour=None, stroke_width=1,
                 stroke_opacity=1, opacity=1):
        '''
        Initializes an instance of :class:`Shape`.

        :param position:
            The position of the centre of the shape given as coordiantes in the scene's 
            reference frame. Defaults to the zero vector (top-left corner of the screen).
        :param rotation:
            The rotation of the shape (about its centre), in radians. Defaults to 0.
        :param scale:
            The scale of the shape. Defaults to the unit vector.
        :param fill_colour:
            The fill colour of the shape. Defaults to white.
            If set to ``None``, the shape has no fill.
        :param fill_opacity:
            The opacity of the shape fill. Defaults to 1 (fully opaque).
        :param border_radius:
            The radius of the corner curvature. Defaults to 0.
        :param stroke_colour:
            The colour of the shape's stroke. Defaults to ``None``, meaining that
            there is no stroke.
        :param stroke_width:
            The width of the stroke from the edge of the shape.
            An inner and outer stroke of this width is applied.

            Defaults to 1.
        :param stroke_opacity:
            The opacity of the stroke. Defaults to 1 (fully opaque).
        :param opacity:
            The opacity of the shape. Defaults to 1 (fully opaque).
            This affects the WHOLE shape (as opposed to fill or stroke opacity which
            only affect their respective functions).

        '''

        super().__init__(position, rotation, scale, opacity)

        self.size = Vector2()
        self.fill_colour = convert_colour(fill_colour)
        self.fill_opacity = fill_opacity
        self.border_radius = border_radius
        self.stroke_colour = convert_colour(stroke_colour)
        self.stroke_width = stroke_width
        self.stroke_opacity = stroke_opacity

    @property
    def size(self):
        '''
        The size of the shape.

        :returns:
            A two-dimensional vector whose horizontal component is the width
            and vertical component is the height of the shape's bounds.

        '''

        return self.__size

    @size.setter
    def size(self, value):
        '''
        Sets the size of the shape.

        :param value:
            A :class:`mathanim.utils.Vector2` whose x and y components represent
            the width and height of the shape respectively.

        '''

        self.__size = value
        self.__real_size = value * self.scale

    @property
    def real_size(self):
        '''
        Gets the actual size of the shape in the scene (including scale of the object).

        '''

        return self.__real_size

    @property
    def width(self):
        '''
        The width of the shape.

        '''
        
        return self.size.x

    @property
    def height(self):
        '''
        The height of the shape.

        '''
        
        return self.size.y

    @property
    def fill_colour(self):
        '''
        The fill colour of the shape.

        '''

        return self.__fill_colour
    
    @fill_colour.setter
    def fill_colour(self, value):
        '''
        Sets the fill colour of the shape.

        '''

        self.__fill_colour = convert_colour(value)

    @property
    def stroke_colour(self):
        '''
        The stroke colour of the shape.

        '''

        return self.__stroke_colour
    
    @stroke_colour.setter
    def stroke_colour(self, value):
        '''
        Sets the stroke colour of the shape.

        '''

        self.__stroke_colour = convert_colour(value)

class Rectangle(Shape):
    '''
    A rectangle shape.

    '''

    def __init__(self, width=1, height=1, position=None, rotation=0, scale=None, 
                 fill_colour='white', fill_opacity=1, border_radius=0, stroke_colour=None, 
                 stroke_width=1, stroke_opacity=1, opacity=1):
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
        :param border_radius:
            The radius of the corner curvature. Defaults to 0.
        :param stroke_colour:
            The colour of the rectangle's stroke. Defaults to ``None``, meaining that
            there is no stroke.
        :param stroke_width:
            The width of the stroke from the edge of the rectangle.
            An inner and outer stroke of this width is applied.

            Defaults to 1.
        :param stroke_opacity:
            The opacity of the stroke. Defaults to 1 (fully opaque).
        :param opacity:
            The opacity of the rectangle. Defaults to 1 (fully opaque).
            This affects the WHOLE rectangle.

        '''

        super().__init__(position, rotation, scale, fill_colour, fill_opacity, border_radius, 
                         stroke_colour, stroke_width, stroke_opacity, opacity)
                        
        self.size = Vector2(width, height)

    def draw(self, render_context):
        '''
        Draw this rectangle onto the specified :class:`cairo.Context`.

        :param:
            A :class:`cairo.Context` that this object will be rendered onto.

        '''

        half_size = self.real_size / 2
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
        render_context.new_sub_path()
        render_context.arc(self.width - self.border_radius, self.border_radius, self.border_radius, math.radians(-90), 0)
        render_context.arc(self.width - self.border_radius, self.height - self.border_radius, self.border_radius, 0, math.radians(90))
        render_context.arc(self.border_radius, self.height - self.border_radius, self.border_radius, math.radians(90), math.radians(180))
        render_context.arc(self.border_radius, self.border_radius, self.border_radius, math.radians(180), math.radians(270))
        render_context.close_path()

        do_stroke = self.stroke_colour is not None
        if self.fill_colour is not None:
            render_context.set_source_rgba(*self.fill_colour.rgb, self.opacity * self.fill_opacity)

            if do_stroke:
                # the fill command consumes the current path so if we 
                # want to draw a stroke AND a fill, we need to preserve it.
                render_context.fill_preserve()
            else:
                render_context.fill()
        
        if do_stroke:
            render_context.set_source_rgba(*self.stroke_colour.rgb, self.opacity * self.stroke_opacity)
            render_context.set_line_width(self.stroke_width)
            render_context.stroke()
