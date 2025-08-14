class MeccanoWorkbench(Workbench):
    """Meccano workbench"""

    def __init__(self):
        self.__class__.Icon = (
            FreeCAD.getResourceDir() + "Mod/MeccanoWB/icons/Meccano_logo.svg"
        )
        self.__class__.MenuText = "Meccano"
        self.__class__.ToolTip = "Meccano pieces and utilities"

    def Initialize(self):
        """This function is executed when the workbench is first activated.
        It is executed once in a FreeCAD session followed by the Activated function.
        """

        try:
            import MeccanoTools
        except ImportError as err:
            FreeCAD.Console.PrintError(
                "Features from MeccanoTools package cannot be loaded. {err}\n".format(
                    err=str(err)
                )
            )

        # Here you can import your commands, or any other module you need
        FreeCADGui.addCommand("Stripe", MeccanoTools.My_Command_Class())
        # FreeCADGui.addCommand("My_Other_Command", commands.My_Other_Command_Class())
        self.list = ["Stripe"]  # a list of command names created in the line above
        self.appendToolbar(
            "My Commands", self.list
        )  # creates a new toolbar with your commands
        self.appendMenu("My New Menu", self.list)  # creates a new menu
        # self.appendMenu(
        #     ["An existing Menu", "My submenu"], self.list
        # )  # appends a submenu to an existing menu

    def Activated(self):
        """This function is executed whenever the workbench is activated"""
        return

    def Deactivated(self):
        """This function is executed whenever the workbench is deactivated"""
        return

    def ContextMenu(self, recipient):
        """This function is executed whenever the user right-clicks on screen"""
        # "recipient" will be either "view" or "tree"
        # self.appendContextMenu(
        #     "My commands", self.list
        # )  # add commands to the context menu

    def GetClassName(self):
        # This function is mandatory if this is a full Python workbench
        # This is not a template, the returned string should be exactly "Gui::PythonWorkbench"
        return "Gui::PythonWorkbench"

    def GetClassName(self):
        return "TechDrawGui::Workbench"


try:
    Gui.addWorkbench(MeccanoWorkbench)
except Exception as e:
    FreeCAD.Console.PrintError(
        "Error adding MeccanoWorkbench: {err}\n".format(err=str(e))
    )
