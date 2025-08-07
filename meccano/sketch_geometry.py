from abc import ABC, abstractmethod
from enum import Enum
from typing import Tuple

import Part
import Sketcher
from FreeCAD import Vector



class Measurements:
    """Holds common measurement constants for Meccano pieces."""

    tolerance = 0.1
    hole_radius = 2
    medium_extrude_height = 0.75
    thick_extrude_height = 1.5
    thin_extrude_height = 0.5

    nut_side = 3.5
    nut_radius = 1.5



class Geometry(ABC):
    """Abstract base class for geometric objects that can be added to a FreeCAD sketch."""

    global_id_counter = 0
    global_registry = {}

    def __init__(self):
        """Initializes a Geometry object and registers it globally."""
        self.id = Geometry.global_id_counter
        Geometry.global_id_counter += 1
        Geometry.global_registry[self.id] = self

    @classmethod
    def add_all_to_sketch(cls, sketch):
        """Adds all registered geometry objects to the given sketch and resets the registry.

        Args:
            sketch: The FreeCAD sketch object to add geometry to.
        """
        for geometry in cls.global_registry.values():
            geometry.add_to_sketch(sketch)
        cls.global_registry = {}
        cls.global_id_counter = 0

    @abstractmethod
    def add_to_sketch(self, sketch):
        """Adds this geometry object to the given sketch.

        Args:
            sketch: The FreeCAD sketch object to add geometry to.
        """
        pass


class LineSubParts(Enum):
    WHOLE_OBJECT = 0
    START_POINT = 1
    END_POINT = 2
    CENTER_POINT = 3


class X:
    id = -1


class Y:
    id = -2


class Line(Geometry):
    """A line segment geometry object."""

class Line(Geometry):
    def __init__(self, PointA, PointB):
        """Initializes a Line object.

        Args:
            PointA: The start point (FreeCAD.Vector).
            PointB: The end point (FreeCAD.Vector).
        """
        super().__init__()
        self.geometry = Part.LineSegment(PointA, PointB)
        self.PointA = PointA
        self.PointB = PointB

    def add_to_sketch(self, sketch):
        """Adds the line segment to the given sketch.

        Args:
            sketch: The FreeCAD sketch object to add geometry to.
        """
        sketch.addGeometry(self.geometry)

<<<<<<< HEAD

class Circle(Geometry):
    """A circle geometry object."""
=======
>>>>>>> master

class Circle(Geometry):
    def __init__(self, center, radius, normal=Vector(0.0, 0.0, 1.0)):
        """Initializes a Circle object.

        Args:
            center: The center point (FreeCAD.Vector).
            radius (float): The radius of the circle.
            normal: The normal vector (FreeCAD.Vector), default (0,0,1).
        """
        super().__init__()
        self.geometry = Part.Circle(center, normal, radius)
        # Constraints.radius(self, radius)  # Doubt

    def add_to_sketch(self, sketch):
        """Adds the circle to the given sketch.

        Args:
            sketch: The FreeCAD sketch object to add geometry to.
        """
        sketch.addGeometry(self.geometry)

<<<<<<< HEAD

class Square(Geometry):
    """A square geometry object, composed of four lines."""
=======
>>>>>>> master

class Square(Geometry):
    def __init__(self, topright_vertix, side):
        """Initializes a Square object.

        Args:
            topright_vertix: The top right vertex (FreeCAD.Vector).
            side (float): The length of the square's side.
        """
        super().__init__()
        self.line1 = Line(topright_vertix, topright_vertix + Vector(0, side, 0))
        self.line2 = Line(topright_vertix, topright_vertix + Vector(side, 0, 0))
        self.line3 = Line(
            topright_vertix + Vector(side, side, 0),
            topright_vertix + Vector(0, side, 0),
        )
        self.line4 = Line(
            topright_vertix + Vector(side, side, 0),
            topright_vertix + Vector(side, 0, 0),
        )

    def constraints(self):
        """(Stub) Add constraints for the square geometry."""
        pass
        # Constraints.coincident((self.line1, LineSubParts.START_POINT), (self.line2, LineSubParts.START_POINT) )
        # Constraints.coincident((self.line1, LineSubParts.END_POINT), (self.line3, LineSubParts.END_POINT) )
        # Constraints.coincident((self.line3, LineSubParts.START_POINT), (self.line2, LineSubParts.END_POINT) )
        # Constraints.coincident((self.line2, LineSubParts._POINT), (self.line2, LineSubParts.START_POINT) )

        # Constraints.horizontal(self.line1)
        # Constraints.horizontal(self.line)
        # Constraints.vertical(self.line2)
        # Constraints.vertical(self.line4)

        # Constraints.distance((self.line1, LineSubParts.START_POINT), (self.line1, LineSubParts.END_POINT), side)
        # Constraints.equals(self.line1, self.line2)
        # Constraints.equals(self.line1, self.line3)
        # Constraints.equals(self.line1, self.line4)

    def add_to_sketch(self, sketch):
        """(Stub) Add the square to the given sketch."""
        pass



class Arc(Geometry):
    """An arc geometry object."""

    def __init__(self, center, radius, angle1, angle2, normal=Vector(0.0, 0.0, 1.0)):
        """Initializes an Arc object.

        Args:
            center: The center point (FreeCAD.Vector).
            radius (float): The radius of the arc.
            angle1 (float): The start angle (radians).
            angle2 (float): The end angle (radians).
            normal: The normal vector (FreeCAD.Vector), default (0,0,1).
        """
        super().__init__()
        self.geometry = Part.ArcOfCircle(
            Part.Circle(center, normal, radius), angle1, angle2
        )

    def add_to_sketch(self, sketch):
        """Adds the arc to the given sketch.

        Args:
            sketch: The FreeCAD sketch object to add geometry to.
        """
        sketch.addGeometry(self.geometry)



class Constraints:
<<<<<<< HEAD
    """Utility class for managing and adding constraints to FreeCAD sketches."""

=======
>>>>>>> master
    global_registry = {}
    global_id_counter = 0

    @classmethod
    def add_all_constraints(cls, sketch):
        """Adds all registered constraints to the given sketch and resets the registry.

        Args:
            sketch: The FreeCAD sketch object to add constraints to.
        """
        for constraint in cls.global_registry.values():
            sketch.addConstraint(constraint)

        cls.global_registry = {}
        cls.global_id_counter = 0

    @classmethod
    def coincident(cls, first: Tuple, second: Tuple):
        """Adds a coincident constraint between two points or objects.

        Args:
            first (Tuple): The first object and subpart.
            second (Tuple): The second object and subpart.
        """
        cls.global_registry[cls.global_id_counter] = Sketcher.Constraint("Coincident", first[0].id, first[1].value, second[0].id, second[1].value)        
        cls.global_id_counter += 1

    @classmethod
    def tangent(cls, first: Tuple, second: Tuple):
        """Adds a tangent constraint between two objects.

        Args:
            first (Tuple): The first object and subpart.
            second (Tuple): The second object and subpart.
        """
        cls.global_registry[cls.global_id_counter] = Sketcher.Constraint("Tangent", first[0].id, first[1].value, second[0].id, second[1].value)        
        cls.global_id_counter += 1

    @classmethod
    def line_horizontal(cls, line):
        """Adds a horizontal constraint to a line.

        Args:
            line: The line geometry object.
        """
        cls.global_registry[cls.global_id_counter] = Sketcher.Constraint('Horizontal', line.id)
        cls.global_id_counter += 1

    @classmethod
    def points_horizontal(cls, first: Tuple, second: Tuple):
        """Adds a horizontal constraint between two points.

        Args:
            first (Tuple): The first object and subpart.
            second (Tuple): The second object and subpart.
        """
        cls.global_registry[cls.global_id_counter] = Sketcher.Constraint('Horizontal', first[0].id, first[1].value, second[0].id, second[1].value)
        cls.global_id_counter += 1

    @classmethod
    def points_vertical(cls, first: Tuple, second: Tuple):
        """Adds a vertical constraint between two points.

        Args:
            first (Tuple): The first object and subpart.
            second (Tuple): The second object and subpart.
        """
        cls.global_registry[cls.global_id_counter] = Sketcher.Constraint('Vertical', first[0].id, first[1].value, second[0].id, second[1].value)
        cls.global_id_counter += 1

    @classmethod
    def line_vertical(cls, line):
        """Adds a vertical constraint to a line.

        Args:
            line: The line geometry object.
        """
        cls.global_registry[cls.global_id_counter] = Sketcher.Constraint('Vertical', line.id)
        cls.global_id_counter += 1

    @classmethod
    def radius(cls, circle, radius):
        """Adds a radius constraint to a circle.

        Args:
            circle: The circle geometry object.
            radius (float): The radius value.
        """
        cls.global_registry[cls.global_id_counter] = Sketcher.Constraint('Radius', circle.id, radius)
        cls.global_id_counter += 1

    @classmethod
    def on_object(cls, object, onobject):
        """Adds a point-on-object constraint.

        Args:
            object: The object and subpart.
            onobject: The object to constrain to.
        """
        cls.global_registry[cls.global_id_counter] = Sketcher.Constraint('PointOnObject', object[0].id, object[1].value, onobject.id)
        cls.global_id_counter += 1

    @classmethod
    def distance_horizontal(cls, first, second, distance):
        """Adds a horizontal distance constraint between two points.

        Args:
            first: The first object and subpart.
            second: The second object and subpart.
            distance (float): The distance value.
        """
        cls.global_registry[cls.global_id_counter] = Sketcher.Constraint('DistanceX', first[0].id, first[1].value, second[0].id, second[1].value, distance)
        cls.global_id_counter += 1

    @classmethod
    def distance_point_to_line(cls, point, line, distance):
        """Adds a distance constraint from a point to a line.

        Args:
            point: The point and subpart.
            line: The line geometry object.
            distance (float): The distance value.
        """
        cls.global_registry[cls.global_id_counter] = Sketcher.Constraint('Distance', point[0].id, point[1].value, line.id, distance)
        cls.global_id_counter += 1

    @classmethod
    def distance_vertical(cls, first, second, distance):
        """Adds a vertical distance constraint between two points.

        Args:
            first: The first object and subpart.
            second: The second object and subpart.
            distance (float): The distance value.
        """
        cls.global_registry[cls.global_id_counter] = Sketcher.Constraint('DistanceY', first[0].id, first[1].value, second[0].id, second[1].value, distance)
        cls.global_id_counter += 1        

    @classmethod
    def distance(cls, first, second, distance):
        """Adds a distance constraint between two points.

        Args:
            first: The first object and subpart.
            second: The second object and subpart.
            distance (float): The distance value.
        """
        cls.global_registry[cls.global_id_counter] = Sketcher.Constraint('Distance', first[0].id, first[1].value, second[0].id, second[1].value, distance)
        cls.global_id_counter += 1             

    @classmethod
    def equals(cls, first, second):
        """Adds an equality constraint between two objects.

        Args:
            first: The first geometry object.
            second: The second geometry object.
        """
        cls.global_registry[cls.global_id_counter] = Sketcher.Constraint('Equal', first.id, second.id)
        cls.global_id_counter += 1             

    @classmethod
    def angle(cls, arc, angle):
        """Adds an angle constraint to an arc.

        Args:
            arc: The arc geometry object.
            angle (float): The angle value (radians).
        """
        cls.global_registry[cls.global_id_counter] = Sketcher.Constraint('Angle', arc.id, angle)
        cls.global_id_counter += 1             

    @classmethod
    def points_symmetric(cls, point1, point2, center):
        """Adds a symmetry constraint between two points about a center.

        Args:
            point1: The first point and subpart.
            point2: The second point and subpart.
            center: The center object and subpart.
        """
        cls.global_registry[cls.global_id_counter] = Sketcher.Constraint('Symmetric', point1[0].id, point1[1].value, point2[0].id, point2[1].value, center[0].id, center[1].value)
        cls.global_id_counter += 1             

    @classmethod
    def on_object(cls, point, obj):
        """Adds a point-on-object constraint for a point and an object.

        Args:
            point: The point and subpart.
            obj: The object to constrain to.
        """
        cls.global_registry[cls.global_id_counter] = Sketcher.Constraint('PointOnObject', point[0].id, point[1].value, obj.id)
        cls.global_id_counter += 1    

    @classmethod
    def parallel(cls, first, second):
        """Adds a parallel constraint between two lines.

        Args:
            first: The first line geometry object.
            second: The second line geometry object.
        """
        cls.global_registry[cls.global_id_counter] = Sketcher.Constraint('Parallel', first.id, second.id)
        cls.global_id_counter += 1    
