
from meccano.sketch_geometry import Measurements as M, Square, Geometry, Constraints, Circle
from FreeCAD import Vector

from meccano import Piece


class Nut(Piece):
    """A nut fastener piece for Meccano-like construction."""

    def __init__(self):
        """Initializes a Nut object."""
        super().__init__()

    def draw_xy_sketch(self, sketch):
        """Draws the nut sketch in the XY plane.

        Args:
            sketch: The FreeCAD sketch object to draw on.
        """
        square = Square(topright_vertix=Vector(0,0,0), side=M.nut_side)
        circle = Circle(radius=M.nut_radius, center=Vector(M.nut_side/2, M.nut_side/2, 0))
        Geometry.add_all_to_sketch(sketch)
        square.constraints()
        Constraints.add_all_constraints(sketch)


    def build(self, app):
        """Builds the 3D extruded nut in the given FreeCAD document.

        Args:
            app: The FreeCAD document or application object.

        Returns:
            The extruded 3D object.
        """
        self.xy_sketch = app.addObject("Sketcher::SketchObject", "NutXYSketch")
        self.draw_xy_sketch(self.xy_sketch)
        self.xy_extruded = self.extrude(app, self.xy_sketch, length_forward=M.thick_extrude_height)

        return self.xy_extruded


class Washer(Piece):
    """A washer fastener piece for Meccano-like construction."""

    def __init__(self, thichness=M.thick_extrude_height):
        """Initializes a Washer object.

        Args:
            thichness (float): The thickness of the washer.
        """
        super().__init__()

        self.thickness = thichness

    def draw_xy_sketch(self, sketch):
        """Draws the washer sketch in the XY plane.

        Args:
            sketch: The FreeCAD sketch object to draw on.
        """
        Circle(radius=M.nut_radius, center=Vector(0,0,0))
        Circle(radius=3*M.nut_radius, center=Vector(0,0,0))
        Geometry.add_all_to_sketch(sketch)
        Constraints.add_all_constraints(sketch)


    def build(self, app):
        """Builds the 3D extruded washer in the given FreeCAD document.

        Args:
            app: The FreeCAD document or application object.

        Returns:
            The extruded 3D object.
        """
        self.xy_sketch = app.addObject("Sketcher::SketchObject", "NutXYSketch")
        self.draw_xy_sketch(self.xy_sketch)
        self.xy_extruded = self.extrude(app, self.xy_sketch, length_forward=self.thickness)

        return self.xy_extruded