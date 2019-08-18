from app.dice import Dice

dice0 = Dice(nrSides=6)
dice1 = Dice(actualSides=[1, 2, 2, 4])


def test_init():
    assert dice0.dice == [1, 2, 3, 4, 5, 6]
    assert dice1.dice == [1, 2, 2, 4]


def test_roll():
    print(dice1.roll(100))
    assert False
