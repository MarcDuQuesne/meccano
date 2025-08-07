from meccano import Piece
import Part

from meccano.sketch_geometry import Line, Circle, LineSubParts, Geometry, Constraints, Arc, X,Y, Measurements as M
from FreeCAD import Vector
from typing import Tuple
from itertools import tee
import FreeCAD as App

import math 

tolerance = 0.1
hole_radius = 2
linear_height = 0.75 


def pairwise(iterable):
    """Iterate over pairs of consecutive elements in an iterable.

    Args:
        iterable (Iterable): The input iterable.

    Returns:
        Iterator[Tuple[Any, Any]]: An iterator of tuple pairs.
    """
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


class Plate(Piece):
    """A rectangular plate with a grid of holes, for Meccano-like construction.

    Attributes:
        n_columns (int): Number of columns of holes.
        n_rows (int): Number of rows of holes.
        extrude_height (float): Height to extrude the plate.
    """

    def __init__(self, n_columns:int, n_rows:int, extrude_height=M.medium_extrude_height):
        """Initializes a Plate object.

        Args:
            n_columns (int): Number of columns of holes (>=0).
            n_rows (int): Number of rows of holes (>=0).
            extrude_height (float): Height to extrude the plate.
        """
        super(Plate).__init__()
        assert n_columns >= 0, "n_holes must be >=0"
        assert n_rows >= 0, "n_holes must be >=0"
        self.n_columns = n_columns
        self.n_rows = n_rows
        self.extrude_height = extrude_height

    def draw_sketch(self, sketch):
        """Draws the plate sketch with holes and boundary geometry.

        Args:
            sketch: The FreeCAD sketch object to draw on.

        Returns:
            The modified sketch object.
        """

        holes = []
        sx_upper = Arc(Vector(0,0,0), radius=hole_radius * 3, angle1=math.pi/2, angle2=math.pi)        
        sx_lower = Arc(Vector(0,-6*hole_radius*(self.n_rows-1),0), radius=hole_radius * 3, angle1=math.pi, angle2=math.pi*3/2)

        dx_upper = Arc(Vector(6*hole_radius*(self.n_columns-1),0,0), radius=hole_radius * 3, angle1=0, angle2=math.pi/2)
        dx_lower = Arc(Vector(6*hole_radius*(self.n_columns-1), -6*hole_radius*(self.n_rows-1),0), radius=hole_radius * 3, angle1=math.pi/2*3, angle2=0)

        for i in range(self.n_columns):
            for j in range(self.n_rows):
                holes.append(Circle(Vector(6*hole_radius*i,-6*hole_radius*j,0), radius=hole_radius + 2 * tolerance))

        if self.n_columns > 1: 
            line1 = Line(Vector(6*hole_radius*(self.n_columns-1), 3*hole_radius, 0), Vector(0, 3*hole_radius, 0), )
            line2 = Line(Vector(0, -3*hole_radius, 0), Vector(6*hole_radius*(self.n_columns-1), -3*hole_radius, 0))
        else:
            line1 = dx_upper
            line2 = sx_lower

        if self.n_rows > 1:
            line3 = Line(Vector(-3*hole_radius, 0, 0), Vector(-3*hole_radius, -6*hole_radius*(self.n_rows-1), 0))
            line4 = Line(Vector(6*hole_radius*(self.n_rows-1), -6*hole_radius*(self.n_rows-1), 0), Vector(6*hole_radius*(self.n_rows-1), 0, 0))
        else:
            line3 = sx_lower
            line4 = dx_lower

        Geometry.add_all_to_sketch(sketch)

        Constraints.tangent((sx_upper, LineSubParts.START_POINT), (line1, LineSubParts.END_POINT))
        Constraints.tangent((sx_upper, LineSubParts.END_POINT), (line3, LineSubParts.START_POINT))
        Constraints.tangent((dx_lower, LineSubParts.START_POINT), (line2, LineSubParts.END_POINT))
        Constraints.tangent((dx_upper, LineSubParts.START_POINT), (line4, LineSubParts.END_POINT))
        
        Constraints.angle(dx_lower, math.pi/2)
        Constraints.angle(sx_lower, math.pi/2)

        Constraints.equals(dx_lower, dx_upper)
        Constraints.equals(dx_lower, sx_upper)
        Constraints.equals(dx_lower, sx_lower)


        if self.n_columns > 1:
            Constraints.tangent((dx_upper, LineSubParts.END_POINT), (line1, LineSubParts.START_POINT))
            Constraints.tangent((sx_lower, LineSubParts.END_POINT), (line2, LineSubParts.START_POINT))
        
        if self.n_rows > 1:
            Constraints.tangent((sx_lower, LineSubParts.START_POINT), (line3, LineSubParts.END_POINT))
            Constraints.tangent((dx_lower, LineSubParts.END_POINT), (line4, LineSubParts.START_POINT))

        Constraints.radius(sx_upper, hole_radius * 3)

        Constraints.coincident((sx_upper, LineSubParts.CENTER_POINT), (X, LineSubParts.START_POINT))

        if self.n_columns > 1:
            Constraints.distance((line1,LineSubParts.START_POINT), (line1, LineSubParts.END_POINT),6*hole_radius*(self.n_columns-1) )
            Constraints.line_horizontal(line1)

        if self.n_rows > 1:
            Constraints.distance((line3,LineSubParts.START_POINT), (line3, LineSubParts.END_POINT),6*hole_radius*(self.n_rows-1) )
            Constraints.line_vertical(line3)

        for hole in holes:
            Constraints.radius(hole, hole_radius+tolerance*2)

        for i in range(self.n_rows):
            for j in range(self.n_columns):

                hole = holes[j+i*self.n_columns]
                Constraints.distance_horizontal((hole,LineSubParts.CENTER_POINT), (Y, LineSubParts.START_POINT),-6*hole_radius*j)
                Constraints.distance_vertical((hole,LineSubParts.CENTER_POINT), (X, LineSubParts.START_POINT),6*hole_radius*i)

        Constraints.add_all_constraints(sketch)

        return sketch

    def build(self, app):
        """Builds the 3D extruded plate in the given FreeCAD document.

        Args:
            app: The FreeCAD document or application object.

        Returns:
            The extruded 3D object.
        """
        self.sketch = app.addObject("Sketcher::SketchObject", "FlatStrip")
        self.draw_sketch(self.sketch)
        extruded = self.extrude(app, self.sketch, length_forward=self.extrude_height)
        app.recompute()

        return extruded


class FlatStrip(Plate):
    """A flat strip (1-row plate) with a specified number of holes."""

    def __init__(self, n_holes, extrude_height=M.medium_extrude_height):
        """Initializes a FlatStrip object.

        Args:
            n_holes (int): Number of holes (>=2).
            extrude_height (float): Height to extrude the strip.
        """
        assert n_holes >=2, "n_holes must be >=2"
        super().__init__(n_rows=1, n_columns=n_holes, extrude_height=extrude_height)
        self.sketch = None