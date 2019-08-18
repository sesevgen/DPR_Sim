class Diceset:
    '''
    A class that holds a set of dice and modifications and allows rolling
    subject to modifications

    Inputs:
    dice: List of tuples (Nr of dice, sides of dice) to roll

    reroll_equal_to: Reroll dice that are equal to numbers in this list
    Ex: Great Weapon Fighting [1,2]

    min_roll: Rolls less than this number are set to this number
    Ex: Elemental Adept 2

    nr_dice_reroll: Reroll the smallest X results, where X is this number
    Ex: Empower X = 5 for Cha = 5

    drop_lowest: Drop the lowest X number of dice, where this is X
    Ex: 4d6 drop lowest for stats
    '''

    def __init__(self,
                 dice=[],
                 reroll_equal_to=[],
                 roll_min=0,
                 nr_dice_reroll=0,
                 drop_lowest=0):

        self.dice = dice
        self.reroll_equal_to = reroll_equal_to
        self.roll_min = roll_min
        self.nr_dice_reroll = nr_dice_reroll
        self.drop_lowest = drop_lowest

    def roll_one_dice(self, dice_max):

        # Roll one of the dice
        roll = random.randint(1, dice_max)

        # Reroll if in reroll list
        if roll in self.reroll_equal_to:
            roll = random.randint(1, dice_max)

        # Check if it's more than the min
        roll = max(roll, self.roll_min)

        return roll

    def roll_all_dice(self):
        if len(self.dice) == 0:
            return []

        else:
            # For each dice type
            for d in self.dice:

                # Initialize rolls list for rerolling lowest
                rolls = []

                # Roll the number of requested dice for the dice type
                for i in range(d[0]):
                    rolls.append(self.roll_one_dice(d[1]))

                # Sort lowest to highest
                rolls.sort()

                # Reroll the lowest requested
                for i in range(self.nr_dice_reroll):
                    rolls[i] = self.roll_one_dice(d[1])

            # Drop lowest reroll
            rolls = rolls[self.drop_lowest:]

            return rolls

    def sum_dice(self):
        return sum(self.roll_all_dice())
