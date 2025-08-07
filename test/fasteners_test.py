from meccano.pieces.fasteners import Nut, Washer


def test_nut(app):
    _hinge = Nut().build(app)


def test_washer(app):
    _hinge = Washer().build(app)
