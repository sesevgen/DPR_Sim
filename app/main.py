from utils import Diceset, d20Set, Action, Statistics
import matplotlib.pyplot as plt


from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

#d20 = d20Set(1)
#diceset = Diceset([(8,6)])
#action = Action(d20,10,diceset,crit_numbers=[],fail_dmg_scale=0.5)  
#stats = Statistics(action)
#stats.collect_statistics()

#stats.plot_histogram()
#plt.savefig('plot')


