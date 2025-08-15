import FreeCAD as App
import FreeCADGui as Gui

from meccano.pieces import Plate

class PlateCommand:
    """Adds a plate with holes to the FreeCAD document."""

    def __init__(self):
        self.app = App.activeDocument()

    def GetResources(self):
        return {
            "Pixmap": "actions/TechDraw_AxoLengthDimension.svg",
            "Accel": "Shift+S",  # a default shortcut (optional)
            "MenuText": "Plate with holes",
            "ToolTip": "What my new command does",
        }

    def Activated(self):
        """Do something here"""
        self.app = App.activeDocument()

        Plate(n_columns=2, n_rows=1, extrude_height=0.2).build(self.app)

    def IsActive(self):
        """Here you can define if the command must be active or not (greyed) if certain conditions
        are met or not. This function is optional."""
        return True

Gui.addCommand("Plate", PlateCommand())
