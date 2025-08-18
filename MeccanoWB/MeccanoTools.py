import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtGui
import os

from meccano.pieces import Plate

# from TaskPanel import createTask


class PlateForm(QtGui.QDialog):
    def __init__(self, parent=None, app=None):
        super(PlateForm, self).__init__(parent)
        self.setWindowTitle("Plate Form")

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
        rows, cols = self.rows_spin.value(), self.cols_spin.value()
        if self.temp is not None:
            self.app.removeObject(self.temp.extruded.Name)
            self.app.removeObject(self.temp.sketch.Name)
        self.temp = Plate(n_columns=rows, n_rows=cols, extrude_height=0.2)
        self.temp.build(self.app)

    def _handle_accept(self):
        if self.temp is not None:
            self.app.recompute()
            self.temp = None
        self.accept()
        Gui.Control.closeDialog()

    def _handle_reject(self):
        if self.temp is not None:
            self.app.removeObject(self.temp.extruded.Name)
            self.app.removeObject(self.temp.sketch.Name)
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
            "ToolTip": "What my new command does",
        }

    def Activated(self):
        """Do something here"""
        self.app = App.activeDocument()
        self.form = PlateForm(app=self.app)
        Gui.Control.showDialog(self)

    def IsActive(self):
        if App.ActiveDocument is None:
            return False
        else:
            return True


Gui.addCommand("Plate", PlateCommand())
