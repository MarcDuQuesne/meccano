from enum import Enum

import Part
from abc import ABC, abstractmethod
import Sketcher
from typing import Tuple 
from FreeCAD import Vector 


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

    def add_to_sketch(self, sketch):
        sketch.addGeometry(self.geometry)

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

    @classmethod
    def coincident(cls, first: Tuple, second: Tuple):
        cls.global_registry[cls.global_id_counter] = Sketcher.Constraint("Coincident", first[0].id, first[1].value, second[0].id, second[1].value)        
        cls.global_id_counter += 1
    
    @classmethod
    def tangent(cls, first: Tuple, second: Tuple):
        cls.global_registry[cls.global_id_counter] = Sketcher.Constraint("Tangent", first[0].id, first[1].value, second[0].id, second[1].value)        
        cls.global_id_counter += 1

    @classmethod
    def horizontal(cls, line):
        cls.global_registry[cls.global_id_counter] = Sketcher.Constraint('Horizontal', line.id)
        cls.global_id_counter += 1

    @classmethod
    def vertical(cls, line):
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
