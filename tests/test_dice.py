from app.dice import Dice
from test_setup import setup


def test_init():
    dice0, dice1 = setup()
    assert dice0.dice == [1, 2, 3, 4, 5, 6]
    assert dice1.dice == [1, 2, 2, 4]


def test_roll():
    dice0, dice1 = setup()
    assert len(dice1.roll(100)) == 100
    assert 3 not in dice1.roll(100)
