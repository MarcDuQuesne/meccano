from meccano.pieces.planar import FlatStrip, Plate
import FreeCAD as App 

def test_linear(app, sketch):

    flat = FlatStrip(n_holes=2)
    flat.draw_sketch(sketch)
    flat.extrude(app, sketch, length_forward=1)

    app.recompute()

def test_plate(app, sketch):

    flat = Plate(n_rows=8, n_columns=16)
    flat.draw_sketch(sketch)
    flat.extrude(app, sketch, length_forward=1)

    app.recompute()