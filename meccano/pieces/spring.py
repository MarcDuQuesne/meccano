from meccano import Piece
import Part

from meccano.sketch_geometry import Line, Circle, LineSubParts, Geometry, Constraints, Arc, X,Y, Measurements as M
from FreeCAD import Vector
from typing import Tuple
from itertools import tee
import FreeCAD as App

import math 

tolerance = 0.1
hole_radius = 2
linear_height = 0.75 

class Spring(Piece):

    def __init__(self, height, coil_radius, pitch, section_radius, angle=0):
        super().__init__()
        self.height = height
        self.coil_radius = coil_radius
        self.section_radius = section_radius
        self.pitch = pitch
        self.angle = angle

    def draw_sketch(self, sketch):

        section = Circle(Vector(self.coil_radius, 0, 0), radius=self.section_radius)
        Geometry.add_all_to_sketch(sketch)
        
        Constraints.radius(section, self.section_radius)
        # Constraints.coincident((section, LineSubParts.CENTER_POINT))
        
        Constraints.add_all_constraints(sketch)
        

        return sketch

    def helix(self, app, sketch):
        helix = app.addObject('PartDesign::AdditiveHelix','AdditiveHelix')
        helix.Profile = (sketch, ['',])
        app.recompute()
        helix.ReferenceAxis = (sketch,['V_Axis'])
        helix.Mode = 0 # Pitch-Height-Angle
        helix.Pitch = self.pitch
        helix.Height = self.height
        helix.Turns = self.height/self.pitch
        helix.Angle = self.angle # default 0
        helix.Growth = 0
        helix.LeftHanded = 0
        helix.Reversed = 0

        sketch.Visibility = False

        app.recompute()

    def build(self, app):
        self.sketch = app.addObject("Sketcher::SketchObject", "SpringSection")
        sketch = self.draw_sketch(self.sketch)
        spring = self.helix(app, sketch)
        app.recompute()

        return spring