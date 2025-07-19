from meccano.pieces.spring import Spring
import FreeCAD as App 

def test_spring(app):
    Spring(coil_radius=5, pitch = 2, height=20, section_radius=0.5).build(app)

def test_conic_spring(app):
    Spring(coil_radius=5, pitch = 2, height=20, section_radius=0.5, angle=10).build(app)    