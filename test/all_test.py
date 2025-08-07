import FreeCAD as App 
from meccano.sketch_geometry import Measurements
from meccano.pieces import Hinge, FlatStrip, Plate, TriangleHinge

def test_all_pieces(app):

    """Test building all major Meccano pieces in a FreeCAD app.

    Args:
        app: The FreeCAD application or document object.
    """
    hinge = Hinge(n_rows_x=1, n_rows_z=1).build(app)
    hinge2 = Hinge(n_rows_x=3, n_rows_z=4, n_columns=2).build(app)
    flat = FlatStrip(n_holes=5, extrude_height=Measurements.thick_extrude_height).build(app)
    plate = Plate(n_columns=2, n_rows=5).build(app)
    
    small_thinge = TriangleHinge(n_rows_x=1, n_rows_z=2).build(app)
    big_thinge = TriangleHinge(n_rows_x=3, n_rows_z=4, edge_size=6, n_columns=5).build(app)

    hinge = Hinge(n_rows_x=1, n_rows_z=1).build(app)
    hinge2.Placement = App.Placement(App.Vector(Measurements.hole_radius*20,0,0),App.Rotation(App.Vector(0,0,1),0))
    flat.Placement = App.Placement(App.Vector(-Measurements.hole_radius*40,0,0),App.Rotation(App.Vector(0,0,1),0))
    plate.Placement = App.Placement(App.Vector(-Measurements.hole_radius*60,0,0),App.Rotation(App.Vector(0,0,1),0))
    small_thinge.Placement = App.Placement(App.Vector(-Measurements.hole_radius*100,0,0),App.Rotation(App.Vector(0,0,1),0))
    big_thinge.Placement = App.Placement(App.Vector(-Measurements.hole_radius*140,0,0),App.Rotation(App.Vector(0,0,1),0))

    app.recompute()