class Diceset:
    '''
    A class that holds a set of dice and modifications and allows rolling
    subject to modifications

    Inputs:
    dice: List[Dice]

    nr_dice_reroll: Reroll the smallest X results, where X is this number
    Ex: Empower X = 5 for Cha = 5

    drop_lowest: Drop the lowest X number of dice, where this is X
    Ex: 4d6 drop lowest for stats
    '''

    def __init__(self,
                 dice=[],
                 nr_dice_reroll=0,
                 drop_lowest=0):

        self.dice = dice
        self.nr_dice_reroll = nr_dice_reroll
        self.drop_lowest = drop_lowest

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
