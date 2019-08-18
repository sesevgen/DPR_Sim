import random
import os
import matplotlib.pyplot as plt
import numpy as np
have_display = bool(os.environ.get('DISPLAY', None))
if not have_display:
    import matplotlib
    matplotlib.use('Agg')


class d20Set(Diceset):
    '''
    Handles advantage and disadvantage
    '''
    def __init__(self,
                 nr_dice,
                 adv=True,
                 reroll_equal_to=[],
                 roll_min=0,
                 nr_dice_reroll=0):

        super().__init__(
            [(nr_dice, 20)], reroll_equal_to, roll_min, nr_dice_reroll)
        self.adv = adv

    def outcome(self):
        if self.adv:
            return max(self.roll_all_dice())
        else:
            return min(self.roll_all_dice())
