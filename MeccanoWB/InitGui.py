import os
import FreeCAD as App


import sys

sys.path.append(os.path.join(App.getHomePath(), "Mod", "MeccanoWB"))


class MeccanoWorkbench(Gui.Workbench):
    """Meccano workbench"""

    def __init__(self):
        self.__class__.Icon = os.path.join(
            App.getHomePath(), "Mod", "MeccanoWB", "icons", "Meccano_logo.svg"
        )
        self.__class__.MenuText = "Meccano"
        self.__class__.ToolTip = "Meccano pieces and utilities"

    def Initialize(self):
        """This function is executed when the workbench is first activated.
        It is executed once in a FreeCAD session followed by the Activated function.
        """

        self.list = [
            "Plate",
            "Hinge",
        ]  # a list of command names created in the line above
        self.appendToolbar(
            "Meccano", self.list
        )  # creates a new toolbar with your commands
        self.appendMenu("Meccano", self.list)  # creates a new menu
        # self.appendMenu(["Meccano", "Planar"], self.list) # appends a submenu to an existing menu

    def Activated(self):
        Msg("MeccanoWorkbench::Activated()\n")

    def Deactivated(self):
        Msg("MeccanoWorkbench::Deactivated()\n")

    def ContextMenu(self, recipient):
        """This function is executed whenever the user right-clicks on screen"""
        # "recipient" will be either "view" or "tree"
        # self.appendContextMenu(
        #     "My commands", self.list
        # )  # add commands to the context menu

    def GetClassName(self):
        return "Gui::PythonWorkbench"


try:
    Gui.addWorkbench(MeccanoWorkbench())
except Exception as e:
    FreeCAD.Console.PrintError(
        "Error adding MeccanoWorkbench: {err}\n".format(err=str(e))
    )
