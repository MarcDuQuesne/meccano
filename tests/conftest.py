import pytest


import FreeCAD as App


@pytest.fixture
def app():
    # Create a new document
    doc = App.newDocument()
    yield doc
    doc.saveAs("test")


@pytest.fixture
def sketch(app):
    sketch = app.addObject("Sketcher::SketchObject", "Sketch")
    return sketch
