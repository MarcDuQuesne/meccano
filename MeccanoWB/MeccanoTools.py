import FreeCAD as App
import FreeCADGui as Gui

class My_Command_Class:
    """My new command"""

    def GetResources(self):
        return {
            "Pixmap": "actions/TechDraw_AxoLengthDimension.svg",
            "Accel": "Shift+S",  # a default shortcut (optional)
            "MenuText": "My New Command",
            "ToolTip": "What my new command does",
        }

    def Activated(self):
        """Do something here"""
        return

    def IsActive(self):
        """Here you can define if the command must be active or not (greyed) if certain conditions
        are met or not. This function is optional."""
        return True

Gui.addCommand("My_Command", My_Command_Class())
