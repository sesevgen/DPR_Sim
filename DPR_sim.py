#!/usr/bin/python

import numpy as np
import sys
import random
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import argparse


def rolldice(list,reroll,min):
	sum = 0
	d = 4
	for dice in list:
		for i in range(0,dice):
			roll = random.randint(1,d)
			if roll <= reroll:
				roll = random.randint(1,d)
			if roll < min:
				roll = min
			sum += roll
		d += 2
	return sum
	

	
#-----------#
#Define output file name  					"output" : "..."
#-----------#
#Define number of rounds to simulate 		"Ntotal" : int
#-----------#
#Attacks:
#for each, define:
	#Define AC 									"AC" : int
	#Define crit range							"CritRange": int (the min, leave at 20 for normal. 19 = crit on 19-20 etc.)
	#Define total +to hit 						"ToHitBonus" : int
	#Define advantage 							"Advantage": -1, 0 or 1
	#Define resistance							"Resistance" : -1, 0, or 1
	#Define number and type of dice to roll		"NrDice" : [int,int,int,int,int] - d4,d6,d8,d10,d12 Ex: [0,2,1,0,0] is 2d6 + 1d8
	#Define static damage bonus					"DamageBonus" : int - per attack, not per action
	#Define what dice to reroll					"Reroll" : int - reroll anything lower or equal. Ex: 2 means reroll 1s and 2s as in Great Weapon Fighting
	#Define minimum for dicerolls				"DiceMin": int - anything lower becomes this value - Elemental Adept set this to 1
#-----------#
#Spells:
#for each, define:
	#Define Net Save DC							"DC" : int (this is the final number a d20 roll needs to beat to save)
	#Define FailDMG								"FailDMG" : float (0.5 or 0, save for half or no damage)
	#Define Advantage							"Advantage" : -1, 0 or 1
	#Define resistance							"Resistance" : -1, 0, or 1
	#Define number and type of dice to roll		"NrDice" : [int,int,int,int,int] - d4,d6,d8,d10,d12 Ex: [0,2,1,0,0] is 2d6 + 1d8
	#Define static damage bonus					"DamageBonus" : int - per attack, not per action
	#Define what dice to reroll					"Reroll" : int - reroll anything lower or equal.
	#Define minimum for dicerolls				"DiceMin": int - anything lower becomes this value - Elemental Adept set this to 1
#-----------#

filename = 'nofile'

parser = argparse.ArgumentParser(description='Load a .json for simulation.')
parser.add_argument('-i',nargs='?',dest='filename',default='nofile',type=str)

args = vars(parser.parse_args())
filename = args['filename']

if(filename is 'nofile'):
	filename = raw_input('Enter .json file to simulate ' )

try:
	with open(filename) as data_file:
			data = json.load(data_file)
except IOError as e:
	print("File not found.")


output 	= data['output']
ntotal 	= data['Ntotal']

atk=False
spl=False

AC		=[]
crit	=[]
tohit	=[]
adv		=[]
res		=[]
nrdice	=[]
bonus	=[]
reroll	=[]
dicemin =[]

if data.get('Attacks'):
	atk = True
	for attack in data['Attacks']:
		AC.append(attack['AC'])
		crit.append(attack['CritRange'])
		tohit.append(attack['ToHitBonus'])
		adv.append(attack['Advantage'])
		if(attack['Resistance']==-1):
			res.append(-2)
		else:
			res.append(attack['Resistance'])
		nrdice.append(attack['NrDice'])
		bonus.append(attack['DamageBonus'])
		reroll.append(attack['Reroll'])
		dicemin.append(attack['DiceMin'])

	
netdc 		=[]
faildmg 	=[]
spadv		=[]
spres		=[]
spnrdice 	=[]
spbonus 	=[]
spreroll	=[]
spdicemin	=[]

if data.get('Spells'):
	spl = True
	for spell in data['Spells']:
		netdc.append(spell['NetDC'])
		faildmg.append(spell['FailDMG'])
		spadv.append(spell['Advantage'])
		if(spell['Resistance']==-1):
			spres.append(-2)
		else:
			spres.append(spell['Resistance'])
		spnrdice.append(spell['NrDice'])
		spbonus.append(spell['DamageBonus'])
		spreroll.append(spell['Reroll'])
		spdicemin.append(spell['DiceMin'])
	
	
	
#Define round variables
damage=[]

atkperrnd = len(AC)
ntotattacks = ntotal*atkperrnd
miss = 0
totmiss = 0
atleastonemiss = 0
crits = 0
atleastonecrit = 0

spperrnd = len(netdc)
ntotalsp = ntotal*spperrnd
faileddc = 0
totfail = 0
atleastonefail = 0

#Total rounds
for i in range(0,ntotal):

	sum = 0
	
	#Attacks
	didImiss=False
	didIcrit=False
	
	#Nr of attacks per round
	for j in range(0,atkperrnd):
	
		#Roll attack
		if(adv[j]==2):
			roll = max(random.randint(1,20),random.randint(1,20),random.randint(1,20))
		elif(adv[j]==1):
			roll = max(random.randint(1,20),random.randint(1,20))
		elif(adv[j]==-1):
			roll = min(random.randint(1,20),random.randint(1,20))
		else:
			roll = random.randint(1,20)
			
		#Check if attack hits, crits or misses
		if(roll >= crit[j]):
			sum += int((rolldice(2*nrdice[j],reroll[j],dicemin[j]) + bonus[j])*(-res[j]/2.0+1))
			crits+=1
			didIcrit=True
		elif(roll == 1):
			miss+=1
			didImiss=True
		elif(roll + tohit[j] >= AC[j]):
			sum += int((rolldice(nrdice[j],reroll[j],dicemin[j]) + bonus[j])*(-res[j]/2.0+1))
		else:
			miss+=1
			didImiss=True
			
	if(sum==0):
		totmiss+=1
	if(didImiss):
		atleastonemiss+=1
	if(didIcrit):
		atleastonecrit+=1		
		
	#Spells
	didIfail=False
	
	#Nr of spells per round
	for j in range(0,spperrnd):
		
		#Roll save
		if(spadv[j]==1):
			roll = max(random.randint(1,20),random.randint(1,20))
		elif(spadv[j]==-1):
			roll = min(random.randint(1,20),random.randint(1,20))
		else:
			roll = random.randint(1,20)
	
		#Check if saved
		if(roll >= netdc[j]):
			sum += int((rolldice(spnrdice[j],spreroll[j],spdicemin[j])+spbonus[j])*(-spres[j]/2.0+1))
		else:
			sum += int(((rolldice(spnrdice[j],spreroll[j],spdicemin[j])+spbonus[j])*faildmg[j])*(-spres[j]/2.0+1))
			faileddc+=1
			didIfail = True

	if(didIfail):
		atleastonefail+=1
	
	damage.append(sum)

f = open(output+'.txt','w')
maxdmg = np.amax(damage)
weights = np.ones_like(damage)/float(len(damage))
plot0=plt.figure()
plt.hist(damage,bins=maxdmg+1,range=[-0.5,maxdmg+0.5],weights=weights)
plt.savefig(output+'.png')

plot1=plt.figure()
#invdmg = [-x for x in damage]
#invdmg = [x+maxdmg for x in invdmg]
#weights = np.ones_like(invdmg)/float(len(invdmg))
plt.hist(damage,bins=maxdmg+1,range=[-0.5,maxdmg+0.5],weights=weights,cumulative=-1,histtype='step')
plt.savefig(output+'_cum.png')


f.write("Average DPR: "+str(np.mean(damage)))
f.write("\r\nMax Damage Recorded: "+str(maxdmg))
if(atk):
	f.write("\r\n\r\nMiss Percentage per Attack: "+str(float(miss)/ntotattacks*100))
	f.write("\r\nChance to Miss at Least Once Per Round: "+str(float(atleastonemiss)/ntotal*100))
	f.write("\r\nComplete miss percentage (no attacks connect in a round): "+str(float(totmiss)/ntotal*100))
	f.write("\r\nCritical Hits :"+str(float(crits)/ntotattacks*100))
	f.write("\r\nChance to Score at Least One Crit Per Round :"+str(float(atleastonecrit)/ntotal*100))
if(spl):
	f.write("\r\n\r\nFail Percentage per Spell: "+str(float(faileddc)/ntotalsp*100))
	f.write("\r\nChance to Fail a Spell DC at Least Once Per Round: "+str(float(atleastonefail)/ntotal*100))

f.close()
