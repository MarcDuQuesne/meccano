from enum import Enum
import FreeCAD as App


class ObjectType(Enum):
    GEOMETRY = "Geometry"
    CONSTRAINT = "Constraint"

class Piece:
    
    def __init__(self):
        self.geometries = {}
        self.constraints = {}


    def extrude(self, app, sketch, length_forward, length_reversed=0):

        app.addObject('Part::Extrusion','Extrude')
        extruder = app.getObject('Extrude')
        extruder.Base = sketch
        extruder.DirMode = "Normal"
        extruder.DirLink = None
        extruder.LengthFwd = length_forward
        extruder.LengthRev = length_reversed
        extruder.Solid = True
        extruder.Reversed = False
        extruder.Symmetric = False
        extruder.TaperAngle = 0.000000000000000
        extruder.TaperAngleRev = 0.000000000000000
        # App.getDocument('test').getObject('Extrude').ViewObject.ShapeAppearance=getattr(App.getDocument('test').getObject('Sketch').getLinkedObject(True).ViewObject,'ShapeAppearance',App.getDocument('test').getObject('Extrude').ViewObject.ShapeAppearance)
        # App.getDocument('test').getObject('Extrude').ViewObject.LineColor=getattr(App.getDocument('test').getObject('Sketch').getLinkedObject(True).ViewObject,'LineColor',App.getDocument('test').getObject('Extrude').ViewObject.LineColor)
        # App.getDocument('test').getObject('Extrude').ViewObject.PointColor=getattr(App.getDocument('test').getObject('Sketch').getLinkedObject(True).ViewObject,'PointColor',App.getDocument('test').getObject('Extrude').ViewObject.PointColor)
        sketch.Visibility = False
        extruder.Visibility = True
        App.ActiveDocument.recompute()