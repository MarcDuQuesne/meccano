from meccano.pieces.planar import FlatStrip, Plate
import FreeCAD as App 

def test_linear(app):
    FlatStrip(n_holes=2).build(app)


def test_plate(app):
    Plate(n_rows=2, n_columns=4).build(app)

