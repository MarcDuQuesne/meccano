import pytest

import sys 

sys.path.append('C:\\Users\\Matteo\\AppData\\Roaming\\FreeCAD\\Mod\\parts_library')
sys.path.append('C:\\Program Files\\FreeCAD 1.0\\bin\\lib\\site-packages\\git\\ext\\gitdb')
sys.path.append('C:\\Users\\Matteo\\AppData\\Roaming\\FreeCAD\\Mod\\freecad.gears\\.\\')
sys.path.append('C:\\Users\\Matteo\\AppData\\Roaming\\FreeCAD\\Mod\\freecad.gears')
sys.path.append('C:\\Users\\Matteo\\AppData\\Roaming\\FreeCAD\\Mod\\fasteners\\.\\')
sys.path.append('C:\\Users\\Matteo\\AppData\\Roaming\\FreeCAD\\Mod\\fasteners')
sys.path.append('C:\\Users\\Matteo\\AppData\\Roaming\\FreeCAD\\Mod\\3D_Printing_Tools')
sys.path.append('C:\\Program Files\\FreeCAD 1.0\\Mod\\Web')
sys.path.append('C:\\Program Files\\FreeCAD 1.0\\Mod\\Tux')
sys.path.append('C:\\Program Files\\FreeCAD 1.0\\Mod\\Test')
sys.path.append('C:\\Program Files\\FreeCAD 1.0\\Mod\\TechDraw')
sys.path.append('C:\\Program Files\\FreeCAD 1.0\\Mod\\Surface')
sys.path.append('C:\\Program Files\\FreeCAD 1.0\\Mod\\Start')
sys.path.append('C:\\Program Files\\FreeCAD 1.0\\Mod\\Spreadsheet')
sys.path.append('C:\\Program Files\\FreeCAD 1.0\\Mod\\Sketcher')
sys.path.append('C:\\Program Files\\FreeCAD 1.0\\Mod\\Show')
sys.path.append('C:\\Program Files\\FreeCAD 1.0\\Mod\\Robot')
sys.path.append('C:\\Program Files\\FreeCAD 1.0\\Mod\\ReverseEngineering')
sys.path.append('C:\\Program Files\\FreeCAD 1.0\\Mod\\Points')
sys.path.append('C:\\Program Files\\FreeCAD 1.0\\Mod\\Plot')
sys.path.append('C:\\Program Files\\FreeCAD 1.0\\Mod\\Path')
sys.path.append('C:\\Program Files\\FreeCAD 1.0\\Mod\\PartDesign')
sys.path.append('C:\\Program Files\\FreeCAD 1.0\\Mod\\Part')
sys.path.append('C:\\Program Files\\FreeCAD 1.0\\Mod\\OpenSCAD')
sys.path.append('C:\\Program Files\\FreeCAD 1.0\\Mod\\MeshPart')
sys.path.append('C:\\Program Files\\FreeCAD 1.0\\Mod\\Mesh')
sys.path.append('C:\\Program Files\\FreeCAD 1.0\\Mod\\Measure')
sys.path.append('C:\\Program Files\\FreeCAD 1.0\\Mod\\Material')
sys.path.append('C:\\Program Files\\FreeCAD 1.0\\Mod\\Inspection')
sys.path.append('C:\\Program Files\\FreeCAD 1.0\\Mod\\Import')
sys.path.append('C:\\Program Files\\FreeCAD 1.0\\Mod\\Idf')
sys.path.append('C:\\Program Files\\FreeCAD 1.0\\Mod\\Fem')
sys.path.append('C:\\Program Files\\FreeCAD 1.0\\Mod\\Draft')
sys.path.append('C:\\Program Files\\FreeCAD 1.0\\Mod\\Arch')
sys.path.append('C:\\Program Files\\FreeCAD 1.0\\Mod\\AddonManager')
sys.path.append('C:\\Program Files\\FreeCAD 1.0\\Mod')
sys.path.append('C:\\Program Files\\FreeCAD 1.0\\lib')
sys.path.append('C:\\Program Files\\FreeCAD 1.0\\Ext')
sys.path.append('C:\\Program Files\\FreeCAD 1.0\\bin')
sys.path.append('C:\\Program Files\\FreeCAD 1.0\\bin\\python38.zip')
sys.path.append('C:\\Program Files\\FreeCAD 1.0\\bin\\DLLs')
sys.path.append('C:\\Program Files\\FreeCAD 1.0\\bin\\lib')
sys.path.append('C:\\Program Files\\FreeCAD 1.0\\bin')
sys.path.append('C:\\Program Files\\FreeCAD 1.0\\bin\\lib\\site-packages')
sys.path.append('C:\\Users\\Matteo\\AppData\\Roaming\\FreeCAD\\Macro\\')
sys.path.append('C:/Users/Matteo/AppData/Roaming/FreeCAD/Macro')
sys.path.append('C:\\Program Files\\FreeCAD 1.0\\Macro')
sys.path.append('C:\\Program Files\\FreeCAD 1.0\\bin\\lib\\site-packages\\gitdb\\ext\\smmap')
sys.path.append('C:\\Users\\Matteo\\AppData\\Roaming\\FreeCAD\\Macro')
sys.path.append('C:\\Users\\Matteo\\Projects\\Meccano\\meccano\\pieces')
sys.path.append('C:\\Users\\Matteo\\Projects\\Meccano\\meccano')

import FreeCAD as App

@pytest.fixture
def app():
    # Create a new document
    doc = App.newDocument()
    yield doc   
    doc.saveAs('test')

@pytest.fixture
def sketch(app):
    sketch = app.addObject("Sketcher::SketchObject", "Sketch")
    return sketch