import random


def roll_with_adjustments(dice_max, min_roll = 1, reroll_equal_to = []):
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
    if roll in reroll_equal_to:
        roll = random.randint(1,dice_max)
	
	# Check if it's more than the min
    roll = max(roll,min_roll)

    return roll

def action_with_adjustments(dice, adjustments={'min_roll':1, 'reroll_equal_to': [],'reroll_number': 0}):
    '''
    Rolls dice for a single attack or spell, subject to adjustments.

    Adjustments are provided as a dict and are used to add effects like GWM, GWF, Elemental Adept, Critical Hits etc.

    Inputs:
    dice: List of tuples (Nr of dice, sides of dice)
    adjustments: Dict with adjustment keywords and values.

    List of adjustments:
    reroll_equal_to: Reroll dice that are equal to numbers in this list. Ex: Great Weapon Fighting [1,2]
    min_roll: Rolls less than this number are set to this number. Ex: Elemental Adept 2
    reroll_number: Reroll the smallest X number of dice, where X is this number. Ex: Empower: 5

    Returns:
    Total damage rolled after adjustments.

    '''
    min_roll = adjustments['min_roll']
    reroll_equal_to = adjustments['reroll_equal_to']
    reroll_number = adjustments['reroll_number']

    total = 0
    # For each dice type
    for d in dice:
	
        # Initialize rolls list for rerolling lowest
        rolls = []

        # Roll the number of requested dice for the dice type
        for i in range(d[0]):
            roll = roll_with_adjustments(d[1],min_roll,reroll_equal_to)
            rolls.append(roll)
            
        # Sort lowest to highest
        rolls.sort()

        # Reroll the lowest X
        for i in range(reroll_number):
            rolls[i] = roll_with_adjustments(d[1],min_roll,reroll_equal_to)
            
        total += sum(rolls)
    
    return total

def rolld20s(advantage=1, disadvantage=False):
    '''
    Rolls d20s subject to advantage or disadvantage or elven accuracy
    '''
    
    d20s = []
    for i in range(advantage)
        d20s.append(random.randint(1,20))
    
    if disadvantage:
        return min(d20s)
    else:
        return max(d20s)

def collect_statistics_on_action(N,target,action,
                                   details={'modifier': 0, 'advantage':0,'fail':0.0, 'resistance': 1.0}):                                   )
    '''
    Performs a single attack or spell N times, collecting statistics on the damage
    
    Takes into account to-hit or resist DC and the fail outcome, advantage or disadvantage, and resistance
    
    Inputs:
    N: Number of times to perform action
    target: Adjusted d20 target to meet or exceed for a success
    details: Dict with details on adv, resistance and fail condition
    
    Output:
    Array of length N with damage outputs per trial
    
    '''
    disadvantage = False
    
    modifier = details['modifier']
    if advantage < 0:
        disadvantage = True
        advantage = -details['advantage']
    else:
        advantage = details['advantage']
    fail = details['fail']
    resistance = details['resistance']
    
    
    outcomes = []
    for i in range(N):
        d20 = rolld20s(advantage,disadvantage)
        if d20 >= target:
            outcomes.append(action)
        else:
            outcomes.append(action*fail)
    
    
    
    
