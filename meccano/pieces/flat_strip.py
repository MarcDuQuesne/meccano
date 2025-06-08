from meccano import Piece

from meccano.sketch_geometry import Line, Vector, LineSubParts
import Sketcher

class FlatStrip(Piece):

    def build(self, n_holes):

        self.geometries[0] = Line(Vector(0, 0, 0), Vector(1,0,0) )
        self.geometries[1]= Line(Vector(1, 1, 0), Vector(1,2,0) )

        self.constraints[0] = Sketcher.Constraint("Coincident", self.geometries[0].id, self.geometries[1].id, LineSubParts.END_POINT, LineSubParts.END_POINT)

