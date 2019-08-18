from app.dice import Dice


def test_init():
    dice0 = Dice(nrSides=6)
    assert dice0.dice == [1, 2, 3, 4, 5, 6]

    dice1 = Dice(actualSides=[1, 2, 2, 4])
    assert dice1.dice == [1, 2, 2, 4]
