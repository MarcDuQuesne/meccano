from enum import Enum


class ObjectType(Enum):
    GEOMETRY = "Geometry"
    CONSTRAINT = "Constraint"

class Piece:
    
    geometries: {}
    constraints: {}

    def add_to_sketch(self, sketch):

        for geometry in self.geometries.keys():
            sketch.addGeometry(geometry)

        for constraint in self.constraints.keys():
            sketch.addGeometry(geometry)

        return sketch

