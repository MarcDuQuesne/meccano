from meccano.pieces.fasteners import Nut, Washer

from meccano.sketch_geometry import Measurements as M

def test_nut(app):
    """Test building a Nut in a FreeCAD app.

    Args:
        app: The FreeCAD application or document object.
    """
    _hinge = Nut().build(app)

def test_washer(app):
    """Test building a Washer in a FreeCAD app.

    Args:
        app: The FreeCAD application or document object.
    """
    _hinge = Washer().build(app)