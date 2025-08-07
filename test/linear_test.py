from meccano.pieces.planar import FlatStrip, Plate
import FreeCAD as App 

def test_linear(app):
    """Test building a FlatStrip in a FreeCAD app.

    Args:
        app: The FreeCAD application or document object.
    """
    FlatStrip(n_holes=2).build(app)


def test_plate(app):
    """Test building a Plate in a FreeCAD app.

    Args:
        app: The FreeCAD application or document object.
    """
    Plate(n_rows=2, n_columns=4).build(app)

