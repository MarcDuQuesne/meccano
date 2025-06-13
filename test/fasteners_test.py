from meccano.pieces.fasteners import Nut, Washer
import FreeCAD as App 

from meccano.sketch_geometry import Measurements as M

def test_nut(app):

    _hinge = Nut().build(app)

def test_washer(app):

    _hinge = Washer().build(app)