
from meccano.sketch_geometry import Measurements as M, Square, Geometry, Constraints, Circle
from FreeCAD import Vector

from meccano import Piece

class Nut(Piece):

    def __init__(self):
        super().__init__()

    def draw_xy_sketch(self, sketch):
        square = Square(topright_vertix=Vector(0,0,0), side=M.nut_side)
        circle = Circle(radius=M.nut_radius, center=Vector(M.nut_side/2, M.nut_side/2, 0))
        Geometry.add_all_to_sketch(sketch)
        square.constraints()
        Constraints.add_all_constraints(sketch)


    def build(self, app):
        self.xy_sketch = app.addObject("Sketcher::SketchObject", "NutXYSketch")
        self.draw_xy_sketch(self.xy_sketch)
        self.xy_extruded = self.extrude(app, self.xy_sketch, length_forward=M.thick_extrude_height)

        return self.xy_extruded

class Washer(Piece):

    def __init__(self, thichness=M.thick_extrude_height):
        super().__init__()

        self.thickness = thichness

    def draw_xy_sketch(self, sketch):
        Circle(radius=M.nut_radius, center=Vector(0,0,0))
        Circle(radius=3*M.nut_radius, center=Vector(0,0,0))
        Geometry.add_all_to_sketch(sketch)
        Constraints.add_all_constraints(sketch)


    def build(self, app):
        self.xy_sketch = app.addObject("Sketcher::SketchObject", "NutXYSketch")
        self.draw_xy_sketch(self.xy_sketch)
        self.xy_extruded = self.extrude(app, self.xy_sketch, length_forward=self.thickness)

        return self.xy_extruded