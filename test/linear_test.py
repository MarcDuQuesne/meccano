from meccano import FlatStrip


def test_linear(app, sketch):

    sketch = FlatStrip().add_to_sketch(1, sketch)

    app.recompute()