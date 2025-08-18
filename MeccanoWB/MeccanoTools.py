import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtGui
import os

from meccano.pieces import Plate, Hinge


class PlateForm(QtGui.QDialog):
    """A dialog form for creating a Plate object in FreeCAD."""

    def __init__(self, parent=None, app=None):
        super(PlateForm, self).__init__(parent)
        self.setWindowTitle("Plate Shape")

        self.app = app

        layout = QtGui.QVBoxLayout()

        self.rows_label = QtGui.QLabel("Number of rows:")
        self.rows_spin = QtGui.QSpinBox()
        self.rows_spin.setRange(2, 20)  # adjust as needed
        self.rows_spin.setValue(2)

        self.cols_label = QtGui.QLabel("Number of columns:")
        self.cols_spin = QtGui.QSpinBox()
        self.cols_spin.setRange(1, 20)
        self.cols_spin.setValue(1)

        layout.addWidget(self.rows_label)
        layout.addWidget(self.rows_spin)
        layout.addWidget(self.cols_label)
        layout.addWidget(self.cols_spin)

        # I currently have no idea how to use the default buttons, adding an extra two.
        self.btns = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel, parent=self
        )

        layout.addWidget(self.btns)

        # Assign layout to the dialog
        self.setLayout(layout)

        self.temp = None
        self.rows_spin.valueChanged.connect(self._handle_change)
        self.cols_spin.valueChanged.connect(self._handle_change)
        self._handle_change()

        self.btns.accepted.connect(self._handle_accept)
        self.btns.rejected.connect(self._handle_reject)

    def _handle_change(self):
        """When the number of rows or columns changes, update the Plate object displayed."""
        rows, cols = self.rows_spin.value(), self.cols_spin.value()
        if self.temp is not None:
            self.app.removeObject(self.temp.extruded.Name)
            self.app.removeObject(self.temp.sketch.Name)
        self.temp = Plate(n_columns=rows, n_rows=cols, extrude_height=0.2)
        self.temp.build(self.app)

    def _handle_accept(self):
        """When the user accepts the dialog, leave the latest Plate object in the FreeCAD document."""
        if self.temp is not None:
            self.app.recompute()
            self.temp = None
        self.accept()
        Gui.Control.closeDialog()

    def _handle_reject(self):
        """When the user rejects the dialog, remove the latest Plate object from the FreeCAD document."""
        if self.temp is not None:
            self.app.removeObject(self.temp.extruded.Name)
            self.app.removeObject(self.temp.sketch.Name)
        self.reject()
        Gui.Control.closeDialog()


class HingeForm(QtGui.QDialog):
    """A dialog form for creating a Hinge object in FreeCAD."""

    def __init__(self, parent=None, app=None):
        super(HingeForm, self).__init__(parent)
        self.setWindowTitle("Hinge Shape")

        self.app = app

        layout = QtGui.QVBoxLayout()

        self.rows_x_label = QtGui.QLabel("Number of rows (x):")
        self.rows_spin_x = QtGui.QSpinBox()
        self.rows_spin_x.setRange(2, 20)  # adjust as needed
        self.rows_spin_x.setValue(2)

        self.rows_z_label = QtGui.QLabel("Number of rows (z):")
        self.rows_spin_z = QtGui.QSpinBox()
        self.rows_spin_z.setRange(1, 20)
        self.rows_spin_z.setValue(1)

        self.cols_label = QtGui.QLabel("Number of columns:")
        self.cols_spin = QtGui.QSpinBox()
        self.cols_spin.setRange(1, 20)
        self.cols_spin.setValue(1)

        layout.addWidget(self.rows_x_label)
        layout.addWidget(self.rows_spin_x)
        layout.addWidget(self.rows_z_label)
        layout.addWidget(self.rows_spin_z)
        layout.addWidget(self.cols_label)
        layout.addWidget(self.cols_spin)

        # I currently have no idea how to use the default buttons, adding an extra two.
        self.btns = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel, parent=self
        )

        layout.addWidget(self.btns)

        # Assign layout to the dialog
        self.setLayout(layout)

        self.temp = None
        self.rows_spin_x.valueChanged.connect(self._handle_change)
        self.cols_spin.valueChanged.connect(self._handle_change)
        self._handle_change()

        self.btns.accepted.connect(self._handle_accept)
        self.btns.rejected.connect(self._handle_reject)

    def _handle_change(self):
        """When the number of rows or columns changes, update the Hinge object displayed."""
        rows_x, rows_z, cols = (
            self.rows_spin_x.value(),
            self.rows_spin_z.value(),
            self.cols_spin.value(),
        )
        if self.temp is not None:
            self.app.removeObject(self.temp.xz_extruded.Name)
            self.app.removeObject(self.temp.xy_extruded.Name)
            self.app.removeObject(self.temp.xy_sketch.Name)
            self.app.removeObject(self.temp.xz_sketch.Name)
        self.temp = Hinge(
            n_rows_x=rows_x, n_rows_z=rows_z, n_columns=cols, extrude_height=0.2
        )
        self.temp.build(self.app)

    def _handle_accept(self):
        """When the user accepts the dialog, leave the latest Plate object in the FreeCAD document."""
        if self.temp is not None:
            self.app.recompute()
            self.temp = None
        self.accept()
        Gui.Control.closeDialog()

    def _handle_reject(self):
        """When the user rejects the dialog, remove the latest Plate object from the FreeCAD document."""
        if self.temp is not None:
            self.app.removeObject(self.temp.xz_extruded.Name)
            self.app.removeObject(self.temp.xy_extruded.Name)
            self.app.removeObject(self.temp.xy_sketch.Name)
            self.app.removeObject(self.temp.xz_sketch.Name)
        self.reject()
        Gui.Control.closeDialog()


class PlateCommand:
    """Adds a plate with holes to the FreeCAD document."""

    def __init__(self):
        self.app = App.activeDocument()
        self.piece = None

    def GetResources(self):
        return {
            "Pixmap": os.path.join(
                App.getHomePath(), "Mod", "MeccanoWB", "icons", "actions", "planar.svg"
            ),
            "Accel": "Shift+S",  # a default shortcut (optional)
            "MenuText": "Plate with holes",
            "ToolTip": "Add a plate with holes to the document",
        }

    def Activated(self):
        """Display the PlateForm dialog to create a plate."""
        self.app = App.activeDocument()
        self.form = PlateForm(app=self.app)
        Gui.Control.showDialog(self)

    def IsActive(self):
        """Check if the FreeCAD document is active."""
        if App.ActiveDocument is None:
            return False
        else:
            return True


class HingeCommand:
    """Adds a hinge with holes to the FreeCAD document."""

    def __init__(self):
        self.app = App.activeDocument()
        self.piece = None

    def GetResources(self):
        return {
            "Pixmap": os.path.join(
                App.getHomePath(), "Mod", "MeccanoWB", "icons", "actions", "hinge.svg"
            ),
            "Accel": "Shift+S",  # a default shortcut (optional)
            "MenuText": "Hinge with holes",
            "ToolTip": "Add a hinge with holes to the document",
        }

    def Activated(self):
        """Display the PlateForm dialog to create a plate."""
        self.app = App.activeDocument()
        self.form = HingeForm(app=self.app)
        Gui.Control.showDialog(self)

    def IsActive(self):
        """Check if the FreeCAD document is active."""
        if App.ActiveDocument is None:
            return False
        else:
            return True


Gui.addCommand("Plate", PlateCommand())
Gui.addCommand("Hinge", HingeCommand())
