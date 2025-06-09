import FreeCAD as App 
from meccano.sketch_geometry import Measurements
from meccano.pieces import Hinge, FlatStrip, Plate

def test_all_pieces(app):

    hinge = Hinge(n_rows_x=1, n_rows_z=1).build(app)
    hinge2 = Hinge(n_rows_x=3, n_rows_z=2).build(app)
    flat = FlatStrip(n_holes=5, extrude_height=Measurements.thick_extrude_height).build(app)
    plate = Plate(n_columns=2, n_rows=5).build(app)

    hinge2.Placement = App.Placement(App.Vector(Measurements.hole_radius*40,0,0),App.Rotation(App.Vector(0,0,1),0))
    flat.Placement = App.Placement(App.Vector(-Measurements.hole_radius*40,0,0),App.Rotation(App.Vector(0,0,1),0))
    plate.Placement = App.Placement(App.Vector(-Measurements.hole_radius*60,0,0),App.Rotation(App.Vector(0,0,1),0))

    app.recompute()