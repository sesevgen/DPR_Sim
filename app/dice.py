import random
import numpy as np


class Dice:
    '''
    reroll_equal_to: Reroll dice that are equal to numbers in this list
    Ex: Great Weapon Fighting [1,2]

    min_roll: Rolls less than this number are set to this number
    Ex: Elemental Adept 2
    '''
    def __init__(
            self,
            nrSides=None,
            actualSides=None,
            reroll_equal_to=0,
            min_roll=1):
        """
        Small class that allows custom dice
        """
        self.dice = []
        if nrSides is not None:
            assert isinstance(nrSides, int)
            self.dice = list(range(1, nrSides+1))
        elif actualSides is not None:
            self.dice = actualSides
        else:
            print("Please define dice either through nr of sides " +
                  "or by explicitly passing a list of sides.")

        self.reroll_equal_to = reroll_equal_to
        self.min_roll = min_roll
        self.avg = sum(self.dice)/len(self.dice)

    def roll(self, number=1):
        """
        Rolls the dice 'number' of times and returns the results as list.

        :param number: number of times to roll, defaults to 1
        :type number: int, optional
        :return: results of roll
        :rtype: list[int]
        """
        rolls = np.array([random.choice(self.dice) for i in range(number)])
        rolls.sort()
        for i in range(self.reroll_equal_to):
            if rolls[i] < self.avg:
                rolls[i] = roll()[0]
        rolls[rolls < self.min_roll] = self.min_roll
