class Action:
    '''
    A class that holds details and methods relating to a DnD action
    Here, an action is defined as a spell or weapon attack.

    Inputs:
    dice: List of tuples (Nr of dice, sides of dice)
    that the action causes in damage

    instances: Number of times the action is performed per round.
    This can be number of targets of fireball, number of magic missiles,
    or number of attacks from Extra Attack

    per_instance_modifier: Amount of flat damage to add to each instance.

    per_round_modifier: Amount of flat damage to add once.

    reroll_equal_to: Reroll dice that are equal to numbers in this list.

    nr_dice_reroll: Reroll the smallest X results, where X is this number.
    Ex: Empower: 5
    '''

    def __init__(self,
                 d20_diceset,
                 d20_target,
                 per_instance_diceset,
                 instances=1,
                 per_instance_modifier=0,
                 per_round_diceset=Diceset(),
                 per_round_modifier=0,
                 dmg_scale=1.0,
                 fail_dmg_scale=0.0,
                 crit_numbers=[20],
                 crit_scale=2.0,
                 per_crit_diceset=Diceset()):

        self.d20_diceset = d20_diceset
        self.d20_target = d20_target
        self.per_instance_diceset = per_instance_diceset
        self.instances = instances
        self.per_instance_modifier = per_instance_modifier
        self.per_round_diceset = per_round_diceset
        self.per_round_modifier = per_round_modifier
        self.dmg_scale = dmg_scale
        self.fail_dmg_scale = fail_dmg_scale
        self.crit_numbers = crit_numbers
        self.crit_scale = crit_scale
        self.per_crit_diceset = per_crit_diceset

    def perform(self):
        '''
        Performs the action once and returns the damage

        Returns:
        Total damage rolled after adjustments.

        '''

        total = 0
        at_least_one_success = False

        # For each instance
        for i in range(self.instances):

            success = False
            crit = False

            d20 = self.d20_diceset.outcome()
            if d20 in self.crit_numbers:
                crit = True
                success = True
                at_least_one_success = True

            elif d20 >= self.d20_target:
                success = True
                at_least_one_success = True

            if crit:
                total += (
                    self.per_instance_diceset.sum_dice()*self.crit_scale +
                    self.per_crit_diceset.sum_dice() +
                    self.per_instance_modifier)
            elif success:
                total += (self.per_instance_diceset.sum_dice() +
                          self.per_instance_modifier)
            else:
                total += (self.per_instance_diceset.sum_dice() +
                          self.per_instance_modifier)*self.fail_dmg_scale

        if at_least_one_success:
            return int(total + self.per_round_modifier +
                       self.per_round_diceset.sum_dice())
        else:
            return int(total)
