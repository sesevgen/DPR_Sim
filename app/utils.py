import random
import os
have_display = bool(os.environ.get('DISPLAY', None))
if not have_display:
    import matplotlib
    matplotlib.use('Agg')
    
import matplotlib.pyplot as plt
import numpy as np

class Dice:
    def __init__(nrSides=None, actualSides=None):
    """
    Small class that allows custom dice
    """
    self.dice = []
    if nrSides is not None:
        assert isinstance(nrSides, int)
        self.dice = range(nrSides)
    elif actualSides is not None:
        self.dice = actualSides
    else:
        print("Please define dice either through nr of sides or by explicitly passing a list of sides.")

class Diceset:
    '''
    A class that holds a set of dice and modifications and allows rolling subject to modifications
    
    Inputs:
    dice: List of tuples (Nr of dice, sides of dice) to roll
    reroll_equal_to: Reroll dice that are equal to numbers in this list. Ex: Great Weapon Fighting [1,2]
    min_roll: Rolls less than this number are set to this number. Ex: Elemental Adept 2
    nr_dice_reroll: Reroll the smallest X number of dice, where X is this number. Ex: Empower X = 5 for Cha = 5
    drop_lowest: Drop the lowest X number of dice, where this is X. Ex: 4d6 drop lowest for stats
    '''
    
    
    def __init__( self,
                dice=[],
                reroll_equal_to = [],
                roll_min = 0,
                nr_dice_reroll = 0,
                drop_lowest = 0):
                
        self.dice = dice
        self.reroll_equal_to = reroll_equal_to
        self.roll_min = roll_min
        self.nr_dice_reroll = nr_dice_reroll
        self.drop_lowest = drop_lowest
        
    def roll_one_dice(self,dice_max):

        # Roll one of the dice
        roll = random.randint(1,dice_max)
        
        # Reroll if in reroll list
        if roll in self.reroll_equal_to:
            roll = random.randint(1,dice_max)
        
        # Check if it's more than the min
        roll = max(roll,self.roll_min)
        
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
            
class d20Set(Diceset):
    '''
    Handles advantage and disadvantage
    '''
    def __init__(self,
                 nr_dice,
                 adv = True,
                 reroll_equal_to=[],
                 roll_min = 0,
                 nr_dice_reroll = 0):
                 
        super().__init__([(nr_dice,20)],reroll_equal_to,roll_min,nr_dice_reroll)
        self.adv = adv

    def outcome(self):
        if self.adv:
            return max(self.roll_all_dice())
        else:
            return min(self.roll_all_dice())
            

class Action:
    '''
    A class that holds details and methods relating to a DnD action
    Here, an action is defined as a spell or weapon attack.
    
    Inputs:
    dice: List of tuples (Nr of dice, sides of dice) that the action causes in damage
    instances: Number of times the action is performed per round. This can be number of targets of fireball, number of magic missiles, or number of attacks from Extra Attack
    per_instance_modifier: Amount of flat damage to add to each instance.
    per_round_modifier: Amount of flat damage to add once.
    reroll_equal_to: Reroll dice that are equal to numbers in this list. 

    nr_dice_reroll: Reroll the smallest X number of dice, where X is this number. Ex: Empower: 5
    '''
    
    def __init__(self,
                 d20_diceset,
                 d20_target,
                 per_instance_diceset,
                 instances = 1,
                 per_instance_modifier = 0,
                 per_round_diceset = Diceset(),
                 per_round_modifier = 0,
                 dmg_scale = 1.0,
                 fail_dmg_scale = 0.0,
                 crit_numbers = [20],
                 crit_scale = 2.0,
                 per_crit_diceset = Diceset()):
                 
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
                
            elif d20 >=  self.d20_target:
                success = True
                at_least_one_success = True
                
            if crit:
                total += self.per_instance_diceset.sum_dice()*self.crit_scale + self.per_crit_diceset.sum_dice() + self.per_instance_modifier
            elif success:    
                total += self.per_instance_diceset.sum_dice() + self.per_instance_modifier
            else:
                total += (self.per_instance_diceset.sum_dice() + self.per_instance_modifier)*self.fail_dmg_scale
        
        if at_least_one_success:
            return int(total + self.per_round_modifier + self.per_round_diceset.sum_dice())
        else:
            return int(total)

class Statistics:
    '''
    Runs simulations, collects statistics and generates graphs on a given Action with provided conditions
    
    Inputs:
    Action: The Action to collect statistics on
    d20_success_target: Adjusted (post modifiers) number on the d20 to meet or exceed for a success
    nr_d20s: Number of d20s to roll to determine success. 1 is regular, 2 is for advantage or disadvantage, 3 is elven accuracy
    fail_dmg_scale: Damage of a failed Action. Attacks usually deal no damage (0.0), but some spells fail for half (0.5)
    dmg_scale: Overall damage scale. Resistance = 0.5, Vulnerability = 2.0
    disadvantage: Whether multiple d20s are rolled with advantage or disadvantage    
    '''
    
    def __init__(self,action):        
        self.statistics = []

        self.action = action

        self.max_damage = 0
        self.min_damage = 0
        self.avg_damage = 0
        self.percentiles=[0,0,0,0,0] #90, 75, 50, 25, 10
        
    def reset_statistics(self):
        self.statistics = []
        
    def plot_histogram(self,alpha=1.0,label='0'):    
        #plot = plt.figure()
        plt.hist(self.statistics,bins = self.max_damage+1,range = [-0.5,self.max_damage+0.5],density=True,alpha=alpha,label=label)
        #return plot

    def plot_cumulative(self):        
        #plot = plt.figure()
        plt.hist(self.statistics,bins = self.max_damage+1,range = [-0.5,self.max_damage+0.5],cumulative = -1,histtype = 'step')
        #return plot    
        
    def collect_statistics(self,N=100000,append = False):
        if not append:
            self.reset_statistics()

        for i in range(N):               
            self.statistics.append(self.action.perform())
            
        self.max_damage = max(self.statistics)
        self.min_damage = min(self.statistics)
        self.avg_damage = sum(self.statistics)/len(self.statistics)

        self.statistics.sort()

        self.percentiles[0] = np.percentile(self.statistics,10)
        self.percentiles[1] = np.percentile(self.statistics,25)
        self.percentiles[2] = np.percentile(self.statistics,50)
        self.percentiles[3] = np.percentile(self.statistics,75)
        self.percentiles[4] = np.percentile(self.statistics,90)

    def report_statistics(self):
        return {'Min':self.min_damage,'Max':self.max_damage,'Avg':self.avg_damage,'Percentiles':self.percentiles}

    
if __name__ ==  '__main__':
    print("hey")
    
