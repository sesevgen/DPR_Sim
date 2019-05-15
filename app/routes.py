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

    return render_template('home.html', imagepath='static/img/placeholder.png', stats=stats.report_statistics())
    
  
@app.route('/about')
def about():
    return render_template('about.html')
    

@app.route('/calculate',methods=['POST'])
def calculate():
    dice1 = int(request.form.get('dice1'))
    dice2 = int(request.form.get('dice2'))
    d20 = d20Set(1)
    diceset= Diceset([(dice1,dice2)])
    action = Action(d20,0,diceset,crit_numbers=[],fail_dmg_scale=0.5)
    stats = Statistics(action)
    stats.collect_statistics()
    stats.plot_histogram()
    plotname = 'static/img/'+str(dice1)+str(dice2)+'.png'
    plt.savefig(plotname)
    plt.clf()

    return render_template('home.html', imagepath=plotname, stats=stats.report_statistics())
    
    
if __name__ == '__main__':
  app.run(debug=True)