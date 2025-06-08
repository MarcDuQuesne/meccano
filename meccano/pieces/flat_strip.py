from meccano import Piece
import Part

from meccano.sketch_geometry import Line, Circle, LineSubParts, Geometry, Constraints, Arc, X,Y
from FreeCAD import Vector
from typing import Tuple
from itertools import tee
import FreeCAD as App

import math 

tolerance = 0.1
hole_radius = 2
linear_height = 0.75 


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)

class FlatStrip(Piece):

    def __init__(self, n_holes):
        super(FlatStrip).__init__()

        assert n_holes >=2, "n_holes must be >=2"
        self.n_holes = n_holes

    def draw_sketch(self, sketch):

        holes = []
        sx = Arc(Vector(0,0,0), radius=hole_radius * 3, angle1=math.pi/2, angle2=math.pi/2*3)
        dx = Arc(Vector(6*hole_radius*(self.n_holes-1),0,0), radius=hole_radius * 3, angle1=math.pi/2*3, angle2=math.pi/2)

        for i in range(self.n_holes):
            holes.append(Circle(Vector(0+6*hole_radius*i,0,0), radius=hole_radius + 2 * tolerance))

        line1 = Line(Vector(0, 3*hole_radius, 0), Vector(6*hole_radius*(self.n_holes-1), 3*hole_radius, 0))
        line2 = Line(Vector(0, -3*hole_radius, 0), Vector(6*hole_radius*(self.n_holes-1), -3*hole_radius, 0))

        Geometry.add_all_to_sketch(sketch)

        Constraints.tangent((sx, LineSubParts.START_POINT), (line1, LineSubParts.START_POINT))
        Constraints.tangent((sx, LineSubParts.END_POINT), (line2, LineSubParts.START_POINT))
        Constraints.tangent((dx, LineSubParts.END_POINT), (line1, LineSubParts.END_POINT))
        Constraints.tangent((dx, LineSubParts.START_POINT), (line2, LineSubParts.END_POINT))

        Constraints.horizontal(line1)
        Constraints.horizontal(line2)

        Constraints.coincident((holes[0], LineSubParts.CENTER_POINT), (X, LineSubParts.START_POINT))

        for hole in holes:
            Constraints.radius(hole, hole_radius+tolerance*2)

        Constraints.coincident((sx, LineSubParts.CENTER_POINT), (X, LineSubParts.START_POINT))
        Constraints.distance_horizontal((line1,LineSubParts.START_POINT), (line1, LineSubParts.END_POINT),6*hole_radius*(self.n_holes-1) )

        for hole1, hole2 in pairwise(holes):
            Constraints.distance_horizontal((hole1,LineSubParts.CENTER_POINT), (hole2, LineSubParts.CENTER_POINT),6*hole_radius)
            Constraints.on_object((hole2, LineSubParts.CENTER_POINT), X)

        Constraints.radius(sx, hole_radius * 3)
        # Constraints.radius(dx, hole_radius * 3) # redundant

        Constraints.add_all_constraints(sketch)

        return sketch

