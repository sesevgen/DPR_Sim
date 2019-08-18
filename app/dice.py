import random


class Dice:
    def __init__(nrSides=None, actualSides=None):
        """
        Small class that allows custom dice
        """
        self.dice = []
        if nrSides is not None:
            assert isinstance(nrSides, int)
            self.dice = range((1, nrSides+1))
        elif actualSides is not None:
            self.dice = actualSides
        else:
            print("Please define dice either through nr of sides " +
                  "or by explicitly passing a list of sides.")

    def roll(self, number=1):
        """
        Rolls the dice 'number' of times and returns the results as list.

        :param number: number of times to roll, defaults to 1
        :type number: int, optional
        :return: results of roll
        :rtype: list of ints
        """
        return random.choice(self.dice)
