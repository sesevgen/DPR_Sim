from utils import Action, Statistics
from plotting import *

action = Action([(3,6)])
stats = Statistics(action,10)

stats.collect_statistics()
stats.plot_histogram()
