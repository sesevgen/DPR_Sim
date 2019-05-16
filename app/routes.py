#!/usr/bin/env python3

from flask import Flask, render_template, request
from utils import Diceset, d20Set, Action, Statistics
from io import BytesIO

import matplotlib.pyplot as plt

app = Flask(__name__, static_url_path='/static')      
 
@app.route('/')
def home():
    dice1 = 8
    dice2 = 6
    d20 = d20Set(1)
    diceset= Diceset([(dice1,dice2)])
    action = Action(d20,0,diceset,crit_numbers=[],fail_dmg_scale=0.5)
    stats = Statistics(action)
    stats.collect_statistics()

    return render_template('home.html') #, imagepath='static/img/placeholder.png', stats=stats.report_statistics())
    
  
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/distributions')    
def distributions():
    dice1 = 8
    dice2 = 6
    reroll_equal_to = []
    reroll_lowest = 0
    roll_min = 0
    drop_lowest = 0
    
    details = [dice1,dice2,reroll_equal_to,reroll_lowest,roll_min,drop_lowest]
    
    d20 = d20Set(1)
    diceset= Diceset([(dice1,dice2)])
    action = Action(d20,0,diceset,crit_numbers=[],fail_dmg_scale=0.5)
    stats = Statistics(action)
    stats.collect_statistics()

    return render_template('distributions.html', imagepath='static/img/placeholder.png', stats=stats.report_statistics(), details=details)
    
    
@app.route('/calculate',methods=['POST'])
def calculate():
    dice1 = int(request.form.get('dice1'))
    dice2 = int(request.form.get('dice2'))
    try:
        reroll_equal_to = request.form.get('reroll_equal_to')
        reroll_equal_to = reroll_equal_to.split(',')
        reroll_equal_to = [int(roll) for roll in reroll_equal_to]
    except:
        reroll_equal_to = []
    try:
        reroll_lowest = int(request.form.get('reroll_lowest'))
    except:
        reroll_lowest = 0
    try:
        roll_min = int(request.form.get('roll_min'))
    except:
        roll_min = 0
    try:
        drop_lowest = int(request.form.get('drop_lowest'))
    except:
        drop_lowest = 0
    
    details = [dice1,dice2,reroll_equal_to,reroll_lowest,roll_min,drop_lowest]
    
    d20 = d20Set(1)
    diceset= Diceset([(dice1,dice2)],reroll_equal_to,roll_min,reroll_lowest,drop_lowest)
    action = Action(d20,0,diceset,crit_numbers=[],fail_dmg_scale=0.0)
    stats = Statistics(action)
    stats.collect_statistics()
    stats.plot_histogram()
    
    plotname = 'static/img/'
    for detail in details:
        plotname = plotname + str(detail)
    plotname = plotname + '.png'

    plt.savefig(plotname)
    plt.clf()

    return render_template('distributions.html', imagepath=plotname, stats=stats.report_statistics(),details=details)
    
    
if __name__ == '__main__':
  app.run(debug=True)