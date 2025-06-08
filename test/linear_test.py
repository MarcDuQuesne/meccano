from meccano.pieces.flat_strip import FlatStrip
import FreeCAD as App 

def test_linear(app, sketch):

    flat = FlatStrip(n_holes=2)
    flat.draw_sketch(sketch)
    flat.extrude(app, sketch, length_forward=1)

    app.recompute()