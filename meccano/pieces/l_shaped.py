from meccano import Piece
import Part

from meccano.sketch_geometry import Line, Circle, LineSubParts, Geometry, Constraints, Arc, X,Y, Measurements as M
from FreeCAD import Vector
from itertools import tee
import FreeCAD as App

import math 
from BOPTools import BOPFeatures


class Hinge(Piece):

    def __init__(self, n_rows_x, n_rows_z, n_columns=1,extrude_height=M.medium_extrude_height):
        super().__init__()

        assert n_columns > 0, "n_columns must be > 0"
        assert n_rows_x > 0, "n_rows_x must be > 1"
        assert n_rows_z > 0, "n_rows_z must be > 1"
        self.n_columns = n_columns
        self.n_rows_x = n_rows_x
        self.n_rows_z = n_rows_z
        
        self.extrude_height = extrude_height

    def draw_hinge(self, sketch, columns, rows):

        holes = []

        line1 = Line(Vector(6*M.hole_radius*(columns-0.5), 3*M.hole_radius+self.extrude_height, 0), Vector(-3*M.hole_radius, 3*M.hole_radius + self.extrude_height, 0), )

        sx_lower = Arc(Vector(0,-6*M.hole_radius*(rows-1),0), radius=M.hole_radius * 3, angle1=math.pi, angle2=math.pi*3/2)
        dx_lower = Arc(Vector(6*M.hole_radius*(columns-1), -6*M.hole_radius*(rows-1),0), radius=M.hole_radius * 3, angle1=math.pi/2*3, angle2=0)

        for i in range(columns):
            for j in range(rows):
                holes.append(Circle(Vector(6*M.hole_radius*i,-6*M.hole_radius*j,0), radius=M.hole_radius + 2 * M.tolerance))

        if columns > 1: 
            line2 = Line(Vector(0, -3*M.hole_radius*(rows+1), 0), Vector(6*M.hole_radius*(columns-1), -3*M.hole_radius*(rows+1), 0))
        else:
            line2 = sx_lower

        line3 = Line(Vector(-3*M.hole_radius, 3*M.hole_radius + self.extrude_height, 0), Vector(-3*M.hole_radius, -3*M.hole_radius*(rows-1), 0))
        line4 = Line(Vector(6*M.hole_radius*(columns -0.5), -6*M.hole_radius*(rows-1), 0), Vector(6*M.hole_radius*(columns -0.5), 3*M.hole_radius+self.extrude_height, 0))

        Geometry.add_all_to_sketch(sketch)

        Constraints.coincident((line1, LineSubParts.START_POINT), (line4, LineSubParts.END_POINT))
        Constraints.coincident((line1, LineSubParts.END_POINT), (line3, LineSubParts.START_POINT))
        Constraints.tangent((sx_lower, LineSubParts.START_POINT), (line3, LineSubParts.END_POINT))
        Constraints.tangent((dx_lower, LineSubParts.END_POINT), (line4, LineSubParts.START_POINT))

        if columns > 1:
            Constraints.tangent((sx_lower, LineSubParts.END_POINT), (line2, LineSubParts.START_POINT))
            Constraints.tangent((dx_lower, LineSubParts.START_POINT), (line2, LineSubParts.END_POINT))
        else:
            Constraints.tangent((sx_lower, LineSubParts.END_POINT), (dx_lower, LineSubParts.START_POINT))
        
        Constraints.equals(sx_lower, dx_lower)

        Constraints.coincident((holes[columns*(rows-1)], LineSubParts.CENTER_POINT), (sx_lower, LineSubParts.CENTER_POINT))

        Constraints.horizontal(line1)
        Constraints.distance((line1,LineSubParts.START_POINT), (line1, LineSubParts.END_POINT),6*M.hole_radius*(columns) )
        if columns > 1:
            Constraints.distance((line2,LineSubParts.START_POINT), (line2, LineSubParts.END_POINT),6*M.hole_radius*(columns-1) )
            Constraints.horizontal(line2)

        # Constraints.distance((line3   ,LineSubParts.START_POINT), (line3, LineSubParts.END_POINT),6*M.hole_radius*(rows-1) )
        Constraints.distance((line4,LineSubParts.START_POINT), (line4, LineSubParts.END_POINT),6*M.hole_radius*(rows-0.5) + M.medium_extrude_height )
        Constraints.vertical(line4)
        Constraints.vertical(line3)

        for hole in holes:
            Constraints.radius(hole, M.hole_radius+M.tolerance*2)

        for i in range(rows):
            for j in range(columns):

                hole = holes[j+i*columns]
                Constraints.distance_horizontal((hole,LineSubParts.CENTER_POINT), (Y, LineSubParts.START_POINT),-6*M.hole_radius*j)
                Constraints.distance_vertical((hole,LineSubParts.CENTER_POINT), (X, LineSubParts.START_POINT),6*M.hole_radius*i)

        Constraints.add_all_constraints(sketch)

    def draw_xy_sketch(self, sketch):
        return self.draw_hinge(sketch, self.n_columns, self.n_rows_x)
        return 
    
    def draw_xz_sketch(self, sketch):
        return self.draw_hinge(sketch, self.n_columns, self.n_rows_z)

    
    def build(self, app):

        self.xy_sketch = app.addObject("Sketcher::SketchObject", "HingeXYSketch")
        self.xz_sketch = app.addObject("Sketcher::SketchObject", "HingeXZSketch")

        self.draw_xy_sketch(self.xy_sketch)
        self.draw_xz_sketch(self.xz_sketch)
        self.xy_extruded = self.extrude(app, self.xy_sketch, length_forward=self.extrude_height)
        self.xz_extruded = self.extrude(app, self.xz_sketch, length_forward=self.extrude_height)

        self.xz_sketch.MapMode = "FlatFace"
        self.xz_sketch.AttachmentSupport = [(self.xy_extruded,'Face1')]
        self.xz_extruded.Placement = App.Placement(App.Vector(0,M.hole_radius*6 + 2*self.extrude_height,-M.hole_radius*3),App.Rotation(App.Vector(0,0,1),180))

        bp = BOPFeatures.BOPFeatures(App.activeDocument())
        fused = bp.make_multi_fuse([self.xz_extruded.Name, self.xy_extruded.Name, ])

        app.recompute()        

        return fused