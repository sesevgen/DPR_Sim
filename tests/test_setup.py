from app.dice import Dice
from test_setup import setup


def setup():
    dice0 = Dice(nrSides=6)
    dice1 = Dice(actualSides=[1, 2, 2, 4])

    return dice0, dice1
