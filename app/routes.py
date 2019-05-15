#!/usr/bin/env python3

from flask import Flask, render_template
from utils import Diceset, d20Set, Action, Statistics
from io import BytesIO

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

app = Flask(__name__, static_url_path='/static')      
 
@app.route('/')
def home():
    return render_template('home.html')
    
  
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
    fig, ax = plt.subplots(1)
    stats.plot_histogram()
    canvas = FigureCanvas(fig)
    img = BytesIO()
    fig.savefig(img)
    img.seek(0)
    return send_file(img,mimetype='image/png') 
    
    
if __name__ == '__main__':
  app.run(debug=True)