from meccano.pieces.l_shaped import Hinge
import FreeCAD as App 

from meccano.sketch_geometry import Measurements as M

def test_hinge(app):

    _hinge = Hinge(n_rows_x=2, n_columns=2, n_rows_z=2).build(app)

def test_small_hinge(app):

    _hinge = Hinge(n_rows_x=1, n_rows_z=1).build(app)

