from utils import Action, Statistics
from plotting import *

dummy_action = Action([(1,6),(1,4),(1,8)],per_instance_modifier=4,reroll_equal_to=[1,2])
statistics = Statistics(dummy_action,5)

statistics.collect_statistics(100000)

statistics.plot_histogram()
plt.savefig('hist')


