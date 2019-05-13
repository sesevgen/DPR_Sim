from utils import Action, Statistics
import matplotlib.pyplot as plt

action = Action([(3,6)],10)
stats = Statistics(action)

plt.ion()
plt.show()
plt.rcParams["figure.figsize"] = [16,9]

while True:
    stats.collect_statistics(1000,True)
    plt.clf()
    stats.plot_histogram()
    plt.draw()
    plt.pause(0.02)
    


