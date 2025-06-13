from enum import Enum

import Part
from abc import ABC, abstractmethod
import Sketcher
from typing import Tuple 
from FreeCAD import Vector 

class Measurements:

    tolerance = 0.1
    hole_radius = 2
    medium_extrude_height = 0.75 
    thick_extrude_height = 1.5
    thin_extrude_height = 0.5

    nut_side = 3.5
    nut_radius=1.5

class Geometry(ABC):

    global_id_counter = 0
    global_registry = {}

    def __init__(self):
        self.id = Geometry.global_id_counter
        Geometry.global_id_counter += 1
        Geometry.global_registry[self.id] = self

    @classmethod
    def add_all_to_sketch(cls, sketch):
        for geometry in cls.global_registry.values():
            geometry.add_to_sketch(sketch)
        cls.global_registry = {}
        cls.global_id_counter = 0

    @abstractmethod
    def add_to_sketch(self, sketch):
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

    def __init__(self, PointA, PointB):
        super().__init__()
        self.geometry = Part.LineSegment(PointA, PointB)
        self.PointA = PointA
        self.PointB = PointB

    def add_to_sketch(self, sketch):
        sketch.addGeometry(self.geometry)

class Circle(Geometry):

    def __init__(self, center, radius, normal=Vector(0.0, 0.0, 1.0)):
        super().__init__()
        self.geometry = Part.Circle(center, normal, radius)
        # Constraints.radius(self, radius)  # Doubt

    def add_to_sketch(self, sketch):
        sketch.addGeometry(self.geometry)

class Square(Geometry):

    def __init__(self, topright_vertix, side):
        super().__init__()
        self.line1 = Line(topright_vertix, topright_vertix + Vector(0,side,0))
        self.line2 = Line(topright_vertix, topright_vertix + Vector(side,0,0))
        self.line3 = Line(topright_vertix + Vector(side,side,0), topright_vertix + Vector(0,side,0))
        self.line4 = Line(topright_vertix + Vector(side,side,0), topright_vertix + Vector(side,0,0))


    def constraints(self):
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
        pass


class Arc(Geometry):

    def __init__(self, center, radius, angle1, angle2, normal=Vector(0.0, 0.0, 1.0)):
        super().__init__()
        self.geometry = Part.ArcOfCircle(Part.Circle(center, normal, radius), angle1, angle2)

    def add_to_sketch(self, sketch):
        sketch.addGeometry(self.geometry)


class Constraints:

    global_registry = {}
    global_id_counter = 0

    @classmethod
    def add_all_constraints(cls, sketch):
        for constraint in cls.global_registry.values():
            sketch.addConstraint(constraint)

        cls.global_registry = {}
        cls.global_id_counter = 0

    @classmethod
    def coincident(cls, first: Tuple, second: Tuple):
        cls.global_registry[cls.global_id_counter] = Sketcher.Constraint("Coincident", first[0].id, first[1].value, second[0].id, second[1].value)        
        cls.global_id_counter += 1
    
    @classmethod
    def tangent(cls, first: Tuple, second: Tuple):
        cls.global_registry[cls.global_id_counter] = Sketcher.Constraint("Tangent", first[0].id, first[1].value, second[0].id, second[1].value)        
        cls.global_id_counter += 1

    @classmethod
    def line_horizontal(cls, line):
        cls.global_registry[cls.global_id_counter] = Sketcher.Constraint('Horizontal', line.id)
        cls.global_id_counter += 1

    @classmethod
    def points_horizontal(cls, first: Tuple, second: Tuple):
        cls.global_registry[cls.global_id_counter] = Sketcher.Constraint('Horizontal', first[0].id, first[1].value, second[0].id, second[1].value)
        cls.global_id_counter += 1

    @classmethod
    def points_vertical(cls, first: Tuple, second: Tuple):
        cls.global_registry[cls.global_id_counter] = Sketcher.Constraint('Vertical', first[0].id, first[1].value, second[0].id, second[1].value)
        cls.global_id_counter += 1

    @classmethod
    def line_vertical(cls, line):
        cls.global_registry[cls.global_id_counter] = Sketcher.Constraint('Vertical', line.id)
        cls.global_id_counter += 1

    @classmethod
    def radius(cls, circle, radius):
        cls.global_registry[cls.global_id_counter] = Sketcher.Constraint('Radius', circle.id, radius)
        cls.global_id_counter += 1

    @classmethod
    def on_object(cls, object, onobject):
        cls.global_registry[cls.global_id_counter] = Sketcher.Constraint('PointOnObject', object[0].id, object[1].value, onobject.id)
        cls.global_id_counter += 1

    @classmethod
    def distance_horizontal(cls, first, second, distance):
        cls.global_registry[cls.global_id_counter] = Sketcher.Constraint('DistanceX', first[0].id, first[1].value, second[0].id, second[1].value, distance)
        cls.global_id_counter += 1

    @classmethod
    def distance_point_to_line(cls, point, line, distance):
        cls.global_registry[cls.global_id_counter] = Sketcher.Constraint('Distance', point[0].id, point[1].value, line.id, distance)
        cls.global_id_counter += 1

    @classmethod
    def distance_vertical(cls, first, second, distance):
        cls.global_registry[cls.global_id_counter] = Sketcher.Constraint('DistanceY', first[0].id, first[1].value, second[0].id, second[1].value, distance)
        cls.global_id_counter += 1        

    @classmethod
    def distance(cls, first, second, distance):
        cls.global_registry[cls.global_id_counter] = Sketcher.Constraint('Distance', first[0].id, first[1].value, second[0].id, second[1].value, distance)
        cls.global_id_counter += 1             

    @classmethod
    def equals(cls, first, second):
        cls.global_registry[cls.global_id_counter] = Sketcher.Constraint('Equal', first.id, second.id)
        cls.global_id_counter += 1             

    @classmethod
    def angle(cls, arc, angle):
        cls.global_registry[cls.global_id_counter] = Sketcher.Constraint('Angle', arc.id, angle)
        cls.global_id_counter += 1             

    @classmethod
    def points_symmetric(cls, point1, point2, center):
        cls.global_registry[cls.global_id_counter] = Sketcher.Constraint('Symmetric', point1[0].id, point1[1].value, point2[0].id, point2[1].value, center[0].id, center[1].value)
        cls.global_id_counter += 1             

    @classmethod
    def on_object(cls, point, obj):
        cls.global_registry[cls.global_id_counter] = Sketcher.Constraint('PointOnObject', point[0].id, point[1].value, obj.id)
        cls.global_id_counter += 1    

    @classmethod
    def parallel(cls, first, second):
        cls.global_registry[cls.global_id_counter] = Sketcher.Constraint('Parallel', first.id, second.id)
        cls.global_id_counter += 1    
