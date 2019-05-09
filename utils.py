import random

def roll_with_adjustments(dice,adjustments={}):
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

	if 'min_roll' in adjustments.keys():
		min = adjustments['min_roll']
	else:
		min = 1
	
	sum = 0
	
	for d in dice:
		for i in range(d[0]):
			roll = random.randint(min,d[1])
		