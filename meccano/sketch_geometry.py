from enum import Enum


class Geometry:
    global_id_counter = 0
    global_registry = {}

    def __init__(self):
        Geometry._global_id_counter += 1
        self.id = Geometry._global_id_counter
        Geometry._global_registry[self.id] = self

class LineSubParts(Enum):
    WHOLE_OBJECT = 0
    START_POINT = 1 
    END_POINT = 2
    CENTER_POINT = 3

class Line(Geometry):

    def __init__(self, PointA, PointB):
        self.PointA = PointA
        self.PointB = PointB

    def add_to_sketch(self, sketch):
        sketch.addGeometry(Part.LineSegment(App.Vector(1.2, 1.8, 0)), False)