from meccano.pieces.l_shaped import Hinge, TriangleHinge
import FreeCAD as App 

from meccano.sketch_geometry import Measurements as M

def test_hinge(app):

    _hinge = Hinge(n_rows_x=2, n_columns=2, n_rows_z=2).build(app)

def test_small_hinge(app):

    _hinge = Hinge(n_rows_x=1, n_rows_z=1).build(app)

def test_small_t_hinge(app):

    _thinge = TriangleHinge(n_rows_x=1, n_rows_z=2).build(app)

def test_large_t_hinge(app):

    _thinge = TriangleHinge(n_rows_x=3, n_rows_z=4, edge_size=6, n_columns=5).build(app)