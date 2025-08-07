import math

import FreeCAD as App
from BOPTools import BOPFeatures
from FreeCAD import Vector

from meccano import Piece
from meccano.sketch_geometry import (Arc, Circle, Constraints, Geometry, Line,
                                     LineSubParts)
from meccano.sketch_geometry import Measurements as M
from meccano.sketch_geometry import X, Y

D = 3 * M.hole_radius


class Hinge(Piece):
    """A hinge piece with a grid of holes, for Meccano-like construction."""

    def __init__(
        self, n_rows_x, n_rows_z, n_columns=1, extrude_height=M.medium_extrude_height
    ):
        """Initializes a Hinge object.

        Args:
            n_rows_x (int): Number of rows in the x direction (>0).
            n_rows_z (int): Number of rows in the z direction (>0).
            n_columns (int): Number of columns (>0).
            extrude_height (float): Height to extrude the hinge.
        """
        super().__init__()

        assert n_columns > 0, "n_columns must be > 0"
        assert n_rows_x > 0, "n_rows_x must be > 1"
        assert n_rows_z > 0, "n_rows_z must be > 1"
        self.n_columns = n_columns
        self.n_rows_x = n_rows_x
        self.n_rows_z = n_rows_z

        self.extrude_height = extrude_height

    def draw_hinge(self, sketch, columns, rows):
        """Draws the hinge sketch with holes and boundary geometry.

        Args:
            sketch: The FreeCAD sketch object to draw on.
            columns (int): Number of columns.
            rows (int): Number of rows.

        Returns:
            The modified sketch object.
        """

        holes = []

        line1 = Line(
            Vector(2 * D * (columns - 0.5), D + self.extrude_height, 0),
            Vector(-D, D + self.extrude_height, 0),
        )

        sx_lower = Arc(
            Vector(0, -2 * D * (rows - 1), 0),
            radius=M.hole_radius * 3,
            angle1=math.pi,
            angle2=math.pi * 3 / 2,
        )
        dx_lower = Arc(
            Vector(2 * D * (columns - 1), -2 * D * (rows - 1), 0),
            radius=M.hole_radius * 3,
            angle1=math.pi / 2 * 3,
            angle2=0,
        )

        for i in range(columns):
            for j in range(rows):
                holes.append(
                    Circle(
                        Vector(2 * D * i, -2 * D * j, 0),
                        radius=M.hole_radius + 2 * M.tolerance,
                    )
                )

        if columns > 1:
            line2 = Line(
                Vector(0, -D * (rows + 1), 0),
                Vector(2 * D * (columns - 1), -D * (rows + 1), 0),
            )
        else:
            line2 = sx_lower

        line3 = Line(
            Vector(-D, D + self.extrude_height, 0), Vector(-D, -D * (rows - 1), 0)
        )
        line4 = Line(
            Vector(2 * D * (columns - 0.5), -2 * D * (rows - 1), 0),
            Vector(2 * D * (columns - 0.5), D + self.extrude_height, 0),
        )

        Geometry.add_all_to_sketch(sketch)

        Constraints.coincident(
            (line1, LineSubParts.START_POINT), (line4, LineSubParts.END_POINT)
        )
        Constraints.coincident(
            (line1, LineSubParts.END_POINT), (line3, LineSubParts.START_POINT)
        )
        Constraints.tangent(
            (sx_lower, LineSubParts.START_POINT), (line3, LineSubParts.END_POINT)
        )
        Constraints.tangent(
            (dx_lower, LineSubParts.END_POINT), (line4, LineSubParts.START_POINT)
        )

        if columns > 1:
            Constraints.tangent(
                (sx_lower, LineSubParts.END_POINT), (line2, LineSubParts.START_POINT)
            )
            Constraints.tangent(
                (dx_lower, LineSubParts.START_POINT), (line2, LineSubParts.END_POINT)
            )
        else:
            Constraints.tangent(
                (sx_lower, LineSubParts.END_POINT), (dx_lower, LineSubParts.START_POINT)
            )

        Constraints.equals(sx_lower, dx_lower)

        Constraints.coincident(
            (holes[columns * (rows - 1)], LineSubParts.CENTER_POINT),
            (sx_lower, LineSubParts.CENTER_POINT),
        )

        Constraints.line_horizontal(line1)
        Constraints.distance(
            (line1, LineSubParts.START_POINT),
            (line1, LineSubParts.END_POINT),
            2 * D * (columns),
        )
        if columns > 1:
            Constraints.distance(
                (line2, LineSubParts.START_POINT),
                (line2, LineSubParts.END_POINT),
                2 * D * (columns - 1),
            )
            Constraints.line_horizontal(line2)

        # Constraints.distance((line3   ,LineSubParts.START_POINT), (line3, LineSubParts.END_POINT),2*D*(rows-1) )
        Constraints.distance(
            (line4, LineSubParts.START_POINT),
            (line4, LineSubParts.END_POINT),
            2 * D * (rows - 0.5) + M.medium_extrude_height,
        )
        Constraints.line_vertical(line4)
        Constraints.line_vertical(line3)

        for hole in holes:
            Constraints.radius(hole, M.hole_radius + M.tolerance * 2)

        for i in range(rows):
            for j in range(columns):
                hole = holes[j + i * columns]
                Constraints.distance_horizontal(
                    (hole, LineSubParts.CENTER_POINT),
                    (Y, LineSubParts.START_POINT),
                    -2 * D * j,
                )
                Constraints.distance_vertical(
                    (hole, LineSubParts.CENTER_POINT),
                    (X, LineSubParts.START_POINT),
                    2 * D * i,
                )

        Constraints.add_all_constraints(sketch)

    def draw_xy_sketch(self, sketch):
        """Draws the hinge in the XY plane.

        Args:
            sketch: The FreeCAD sketch object to draw on.

        Returns:
            The modified sketch object.
        """
        return self.draw_hinge(sketch, self.n_columns, self.n_rows_x)
        return

    def draw_xz_sketch(self, sketch):
        """Draws the hinge in the XZ plane.

        Args:
            sketch: The FreeCAD sketch object to draw on.

        Returns:
            The modified sketch object.
        """
        return self.draw_hinge(sketch, self.n_columns, self.n_rows_z)

    def build(self, app):
        """Builds the 3D extruded hinge in the given FreeCAD document.

        Args:
            app: The FreeCAD document or application object.

        Returns:
            The fused 3D object.
        """

        self.xy_sketch = app.addObject("Sketcher::SketchObject", "HingeXYSketch")
        self.xz_sketch = app.addObject("Sketcher::SketchObject", "HingeXZSketch")

        self.draw_xy_sketch(self.xy_sketch)
        self.draw_xz_sketch(self.xz_sketch)
        self.xy_extruded = self.extrude(
            app, self.xy_sketch, length_forward=self.extrude_height
        )
        self.xz_extruded = self.extrude(
            app, self.xz_sketch, length_forward=self.extrude_height
        )

        self.xz_sketch.MapMode = "FlatFace"
        self.xz_sketch.AttachmentSupport = [(self.xy_extruded, "Face1")]
        self.xz_extruded.Placement = App.Placement(
            App.Vector(
                0, M.hole_radius * 6 + 2 * self.extrude_height, -M.hole_radius * 3
            ),
            App.Rotation(App.Vector(0, 0, 1), 180),
        )

        bp = BOPFeatures.BOPFeatures(App.activeDocument())
        fused = bp.make_multi_fuse(
            [
                self.xz_extruded.Name,
                self.xy_extruded.Name,
            ]
        )

        app.recompute()

        return fused


class TriangleHinge(Hinge):
    """A triangular hinge piece for Meccano-like construction."""

    def __init__(
        self,
        n_rows_x,
        n_rows_z,
        n_columns=3,
        extrude_height=M.medium_extrude_height,
        edge_size=3 * M.hole_radius,
    ):
        """Initializes a TriangleHinge object.

        Args:
            n_rows_x (int): Number of rows in the x direction (>0).
            n_rows_z (int): Number of rows in the z direction (>0).
            n_columns (int): Number of columns (>0).
            extrude_height (float): Height to extrude the hinge.
            edge_size (float): Size of the triangle edge.
        """
        super().__init__(n_rows_x, n_rows_z, n_columns, extrude_height=extrude_height)

        assert n_columns > 0, "n_columns must be > 0"
        assert n_rows_x > 0, "n_rows_x must be > 1"
        assert n_rows_z > 0, "n_rows_z must be > 1"
        self.columns = n_columns
        self.n_rows_x = n_rows_x
        self.n_rows_z = n_rows_z
        self.edge_size = edge_size

        self.extrude_height = extrude_height

    def draw_xz_sketch(self, sketch):
        """Draws the triangular hinge in the XZ plane.

        Args:
            sketch: The FreeCAD sketch object to draw on.

        Returns:
            The modified sketch object.
        """

        #          4
        #     e___________d
        #      /           \
        #   5 /             \ 3
        #  f|   /|     |\    | c
        # 6 |--|-|-----|-|---| 2
        #   a    1          b

        # a = Vector(-D, self.extrude_height, 0)
        a = Vector(0, 0, 0)
        b = a + Vector(2 * D * (self.columns), 0, 0)
        c = b + Vector(0, D, 0)
        f = a + Vector(0, D, 0)
        e = f + Vector(8 * M.hole_radius, 0, 0)
        d = e + Vector(
            2 * D * (self.columns - 0.5) / 2 - 2 * D, 2 * D * (self.n_rows_z - 0.5)
        )

        f1 = a + Vector(D, 0, 0)
        f2 = f1 + Vector(D, 0, 0)
        f3 = f2 + Vector(0, 2 * D * (self.n_columns - 1) + M.hole_radius, 0)
        f4 = f3 - Vector(D, D, 0)

        fline1 = Line(f1, f2)
        fline2 = Line(f2, f3)
        fline3 = Line(f3, f4)
        fline4 = Line(f4, f1)

        g1 = b - Vector(D, 0, 0)
        g2 = g1 - Vector(D, 0, 0)
        g3 = g2 + Vector(0, 2 * D * (self.n_columns - 1) + M.hole_radius, 0)
        g4 = g3 + Vector(D, -D, 0)

        gline1 = Line(g1, g2)
        gline2 = Line(g2, g3)
        gline3 = Line(g3, g4)
        gline4 = Line(g4, g1)

        holes = []
        center = Vector(2 * D * (self.columns - 0.5) / 2, D, 0)
        for j in range(self.n_rows_z):
            holes.append(
                Circle(
                    center + j * Vector(0, D, 0), radius=M.hole_radius + 2 * M.tolerance
                )
            )

        line1 = Line(a, b)
        line2 = Line(b, c)
        line3 = Line(c, d)
        line4 = Arc(
            center=Vector(
                2 * D * (self.columns - 0.5) / 2, 2 * D * (self.n_rows_z - 0.5), 0
            ),
            radius=2 * D,
            angle1=0,
            angle2=math.pi,
        )
        line5 = Line(e, f)
        line6 = Line(f, a)

        Geometry.add_all_to_sketch(sketch)

        # tangent points are.. complicated.
        Constraints.tangent(
            (line3, LineSubParts.END_POINT), (line4, LineSubParts.START_POINT)
        )
        # Constraints.tangent((line4, LineSubParts.END_POINT), (line5, LineSubParts.START_POINT))
        Constraints.coincident(
            (line4, LineSubParts.END_POINT), (line5, LineSubParts.START_POINT)
        )

        Constraints.points_horizontal(
            (line4, LineSubParts.START_POINT), (line4, LineSubParts.END_POINT)
        )

        Constraints.coincident(
            (line1, LineSubParts.END_POINT), (line2, LineSubParts.START_POINT)
        )
        Constraints.coincident(
            (line2, LineSubParts.END_POINT), (line3, LineSubParts.START_POINT)
        )
        # Constraints.coincident((line3, LineSubParts.END_POINT), (line4, LineSubParts.START_POINT))
        Constraints.coincident(
            (line5, LineSubParts.END_POINT), (line6, LineSubParts.START_POINT)
        )
        Constraints.coincident(
            (line6, LineSubParts.END_POINT), (line1, LineSubParts.START_POINT)
        )

        Constraints.coincident(
            (fline1, LineSubParts.END_POINT), (fline2, LineSubParts.START_POINT)
        )
        Constraints.coincident(
            (fline2, LineSubParts.END_POINT), (fline3, LineSubParts.START_POINT)
        )
        Constraints.coincident(
            (fline3, LineSubParts.END_POINT), (fline4, LineSubParts.START_POINT)
        )
        Constraints.coincident(
            (fline4, LineSubParts.END_POINT), (fline1, LineSubParts.START_POINT)
        )

        Constraints.coincident(
            (gline1, LineSubParts.END_POINT), (gline2, LineSubParts.START_POINT)
        )
        Constraints.coincident(
            (gline2, LineSubParts.END_POINT), (gline3, LineSubParts.START_POINT)
        )
        Constraints.coincident(
            (gline3, LineSubParts.END_POINT), (gline4, LineSubParts.START_POINT)
        )
        Constraints.coincident(
            (gline4, LineSubParts.END_POINT), (gline1, LineSubParts.START_POINT)
        )

        Constraints.coincident(
            (line1, LineSubParts.START_POINT), (X, LineSubParts.START_POINT)
        )
        Constraints.distance(
            (line1, LineSubParts.START_POINT),
            (line1, LineSubParts.END_POINT),
            2 * D * (self.columns),
        )
        Constraints.distance(
            (line2, LineSubParts.START_POINT),
            (line2, LineSubParts.END_POINT),
            self.edge_size,
        )

        Constraints.line_vertical(line2)
        Constraints.line_vertical(line6)
        Constraints.line_horizontal(line1)

        Constraints.line_vertical(fline2)
        Constraints.line_vertical(fline4)

        Constraints.line_vertical(gline2)
        Constraints.line_vertical(gline4)

        Constraints.equals(line2, line6)
        Constraints.equals(line3, line5)

        Constraints.radius(line4, D)

        Constraints.coincident(
            (holes[-1], LineSubParts.CENTER_POINT), (line4, LineSubParts.CENTER_POINT)
        )

        for hole in holes[:-1]:
            Constraints.points_vertical(
                (hole, LineSubParts.CENTER_POINT),
                (holes[-1], LineSubParts.CENTER_POINT),
            )

        for i, hole in enumerate(holes):
            # Constraints.points_vertical((hole, LineSubParts.CENTER_POINT), (line4, LineSubParts.CENTER_POINT))
            Constraints.radius(hole, M.hole_radius + M.tolerance)
            Constraints.distance_point_to_line(
                (hole, LineSubParts.CENTER_POINT),
                X,
                (2 * i + 1) * D + self.extrude_height,
            )

        # Constraints.distance((holes[0], LineSubParts.CENTER_POINT), (line4, LineSubParts.CENTER_POINT), D)

        Constraints.on_object((fline1, LineSubParts.START_POINT), X)
        Constraints.on_object((fline1, LineSubParts.END_POINT), X)
        Constraints.distance(
            (fline1, LineSubParts.START_POINT), (X, LineSubParts.START_POINT), D
        )
        Constraints.distance(
            (fline1, LineSubParts.START_POINT), (fline1, LineSubParts.END_POINT), D
        )
        # Constraints.distance((gline1, LineSubParts.START_POINT), (gline1, LineSubParts.END_POINT), self.edge_size)
        Constraints.parallel(fline3, line5)

        Constraints.on_object((gline1, LineSubParts.START_POINT), X)
        Constraints.on_object((gline1, LineSubParts.END_POINT), X)
        Constraints.distance(
            (gline1, LineSubParts.START_POINT), (line2, LineSubParts.START_POINT), D
        )
        Constraints.distance(
            (gline1, LineSubParts.START_POINT), (gline1, LineSubParts.END_POINT), D
        )
        Constraints.parallel(gline3, line3)

        Constraints.points_horizontal(
            (line5, LineSubParts.END_POINT), (fline4, LineSubParts.START_POINT)
        )

        # Constraints.equals(fline1,gline1)
        Constraints.equals(fline2, gline2)
        # Constraints.equals(fline3,gline3)
        # Constraints.equals(fline4,gline4)

        # for hole in holes[1:]:
        #     Constraints.points_vertical((holes[0], LineSubParts.CENTER_POINT), (hole, LineSubParts.CENTER_POINT))

        # for i, hole in enumerate(holes):
        # Constraints.radius(hole, M.hole_radius+M.tolerance*2)
        # Constraints.points_symmetric((line1, LineSubParts.START_POINT), (line1, LineSubParts.END_POINT), (hole, LineSubParts.CENTER_POINT))
        # Constraints.coincident((hole, LineSubParts.CENTER_POINT), center + j*Vector(0, D, 0))

        Constraints.add_all_constraints(sketch)

        return self.xz_sketch

    def build(self, app):
        """Builds the 3D extruded triangular hinge in the given FreeCAD document.

        Args:
            app: The FreeCAD document or application object.

        Returns:
            The fused 3D object.
        """

        self.xy_sketch = app.addObject("Sketcher::SketchObject", "HingeXYSketch")
        self.xz_sketch = app.addObject("Sketcher::SketchObject", "HingeXZSketch")

        self.draw_xy_sketch(self.xy_sketch)
        self.draw_xz_sketch(self.xz_sketch)
        self.xy_extruded = self.extrude(
            app, self.xy_sketch, length_forward=self.extrude_height
        )
        self.xz_extruded = self.extrude(
            app, self.xz_sketch, length_forward=self.extrude_height
        )

        self.xz_sketch.MapMode = "FlatFace"
        self.xz_sketch.AttachmentSupport = [(self.xy_extruded, "Face1")]
        self.xz_extruded.Placement = App.Placement(
            App.Vector(-D, M.hole_radius * 6 + 2 * self.extrude_height),
            App.Rotation(App.Vector(0, 0, 1), 180),
        )

        bp = BOPFeatures.BOPFeatures(App.activeDocument())
        fused = bp.make_multi_fuse(
            [
                self.xz_extruded.Name,
                self.xy_extruded.Name,
            ]
        )

        app.recompute()

        return fused
