import random
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

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
    
    def __init__(self,Action,d20_success_target,nr_d20s=1,fail_dmg_scale=0.0,dmg_scale=1.0,disadvantage=False,crit_scale=2.0):        
        self.statistics = []
        self.max_damage = 0
        self.min_damage = 0
        
    def reset_statistics(self):
        self.statistics = []

    def append(self,val):
        self.statistics.append(val)
        
    def plot_histogram(self):    
        plot=plt.figure()
        plt.hist(self.statistics,bins=self.max_damage+1,range=[-0.5,self.max_damage+0.5])
        return plot

    def plot_cumulative(self):        
        plot=plt.figure()
        plt.hist(self.statistics,bins=self.max_damage+1,range=[-0.5,self.max_damage+0.5],cumulative=-1,histtype='step')
        return plot
        

class Action:
    '''
    A class that holds details and methods relating to a DnD action
    Here, an action is defined as a spell or weapon attack.
    
    Inputs:
    dice: List of tuples (Nr of dice, sides of dice) that the action causes in damage
    instances: Number of times the action is performed per round. This can be number of targets of fireball, number of magic missiles, or number of attacks from Extra Attack
    per_instance_modifier: Amount of flat damage to add to each instance.
    per_round_modifier: Amount of flat damage to add once.
    reroll_equal_to: Reroll dice that are equal to numbers in this list. Ex: Great Weapon Fighting [1,2]
    min_roll: Rolls less than this number are set to this number. Ex: Elemental Adept 2
    nr_dice_reroll: Reroll the smallest X number of dice, where X is this number. Ex: Empower: 5
    '''
    
    def __init__(self,dice,instances=1,per_instance_modifier=0,per_round_modifier=0,reroll_equal_to=[],min_roll=1,nr_dice_reroll=0,d20_success_target,nr_d20s=1,fail_dmg_scale=0.0,dmg_scale=1.0,disadvantage=False,crit_numbers=[20],crit_scale=2.0,crit_extra_dice=[]):
        self.dice = dice
        self.instances=instances
        self.per_instance_modifier=per_instance_modifier
        self.per_round_modifier=per_round_modifier
        self.reroll_equal_to=reroll_equal_to
        self.min_roll=min_roll
        self.nr_dice_reroll=nr_dice_reroll
        self.d20_success_target=d20_success_target
        self.nr_d20s=nr_d20s
        self.fail_dmg_scale=fail_dmg_scale
        self.dmg_scale=dmg_scale
        self.disadvantage=disadvantage
        self.crit_numbers=crit_numbers
        self.crit_scale=crit_scale
        self.crit_extra_dice=crit_extra_dice
        
        self.statistics = Statistics()
    
    def rolld20s(self):
        '''
        Rolls d20s subject to advantage or disadvantage or elven accuracy
        '''
        
        d20s = []
        for i in range(self.nr_d20s):
            d20s.append(random.randint(1,20))
        
        if self.disadvantage:
            return min(d20s)
        else:
            return max(d20s)  
        
    def roll_with_adjustments(self,dice_max):
        '''
        Rolls a single dice and adjusts
        
        Inputs:
        dice_max: maximum number the dice can roll
        min_roll: numbers less than this number are set to this number
        reroll_equal_to: numbers equal to any number in this list are rerolled once
        
        Output:
        The outcome after adjustments
        '''
        
        # Roll one of the dice
        roll = random.randint(1,dice_max)
        
        # Reroll if in reroll list
        if roll in self.reroll_equal_to:
            roll = random.randint(1,dice_max)
        
        # Check if it's more than the min
        roll = max(roll,self.min_roll)
        
        return roll
        
    def roll_all(self,dice_set):
        # For each dice type
        for d in dice_set:
        
            # Initialize rolls list for rerolling lowest
            rolls = []

            # Roll the number of requested dice for the dice type
            for i in range(d[0]):
                roll = self.roll_with_adjustments(d[1])
                rolls.append(roll)
                
            # Sort lowest to highest
            rolls.sort()

            # Reroll the lowest X
            for i in range(self.nr_dice_reroll):
                rolls[i] = self.roll_with_adjustments(d[1])
                
        return sum(rolls)
    
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
        
            success=False
            crit=False
        
            d20 = self.rolld20s()
            if d20 in self.crit_numbers:
                crit=True
                success=True
                at_least_one_success=True
                
            elif d20 >= self.d20_success_target:
                success=True
                at_least_one_success=True
                
            if crit:
                    total += self.roll_all(self.dice)*self.crit_scale + self.roll_all(self.crit_extra_dice) + self.per_instance_modifier
            elif success:    
                total += self.roll_all(self.dice) + self.per_instance_modifier
        
        return total + self.per_round_modifier
        
    def collect_statistics(self,N,append=False):
        '''
        Performs a single attack or spell N times, collecting statistics on the damage
        
        Takes into account to-hit or resist DC and the fail outcome, advantage or disadvantage, and resistance
        
        Inputs:
        N: Number of times to perform action
        Action: The Action to perform
                
        '''
        
        if not append:
            self.statistics.reset_statistics()

        for i in range(N):
            
            if d20 >= self.d20_success_target:
                damage=self.Action.perform()
            else:
                damage=self.Action.perform()*self.fail_dmg_scale
               
            self.statistics.append(damage)
        
        self.max_damage=max(self.statistics)
        self.min_damage=min(self.statistics)
        
    def __str__(self):
        return 'Dice: {}\nInstances: {}\nPer Instance Modifier: {}\nPer Round Modifier: {}\nRerolling Dice Equal to: {}\nMinimum Roll: {}\nNumber of Dice Rerolled: {}'.format(
        self.dice, self.instances, self.per_instance_modifier, self.per_round_modifier, self.reroll_equal_to, self.min_roll, self.nr_dice_reroll)
        
    
if __name__ == '__main__':
    print("Testing functions")
    
    dummy_action = Action([(1,6),(1,4),(1,8)],per_instance_modifier=4,reroll_equal_to=[1,2])
    print(dummy_action)
    
    print('-----------------------------------------------------------------------------')
    print("Testing 'roll_with_adjustments'")
    for dice in dummy_action.dice:
        print('Rolling a d{}: '.format(dice[1]),dummy_action.roll_with_adjustments(dice[1]))
    
    print('-----------------------------------------------------------------------------')
    print("Testing 'perform'")
    print('Damage is: {}'.format(dummy_action.perform()))    
    
    print('-----------------------------------------------------------------------------')
    print("Testing 'roll_d20s'")
    print('One d20: {}'.format(rolld20s()))
    print('Elven accuracy d20s: {}'.format(rolld20s(3)))
    print('Disadvantage d20s: {}'.format(rolld20s(2,True)))
    
    print('-----------------------------------------------------------------------------')
    print("Testing 'collect_statistics_on_action'")
    print('N: 100, target:5')
    print(collect_statistics_on_action(100,5,dummy_action))
    