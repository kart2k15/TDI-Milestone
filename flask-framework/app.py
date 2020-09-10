import requests
import pandas as pd
import datetime
import quandl
from bokeh.plotting import figure, show
from bokeh.embed import components

from flask import Flask, render_template, request, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Email

app = Flask(__name__)
app.debug = True
# app.config['SECRET KEY']= 'secret key'

def getData(year,ticker):
    startDate='%d-01-01' % year
    endDate='%d-12-30' % year
    ticker_url="WIKI/"+ticker
    data = quandl.get(ticker_url, start_date=startDate, end_date=endDate, collapse='daily', api_key="CG2953NKQSkyP-g1Guwv")
    return data

def makePlot(df, ticker, year, cp, acp, op, aop):
    plot = figure(x_axis_type="datetime", title="Quandl WIKI Stock Data - %d" %year)
    plot.grid.grid_line_alpha=2.0
    plot.xaxis.axis_label = 'Date'
    plot.yaxis.axis_label = 'Price (USD)'
    
    if op=='on':
      plot.line(df.index, df['Open'], color='#fc9003', legend='%s: %s' %(ticker,'Open'))
    if cp=='on':
      plot.line(df.index, df['Close'], color='#fc0303', legend='%s: %s' %(ticker,'Close'))
    if aop=='on':
      plot.line(df.index, df['Adj. Open'], color='#03fc3d', legend='%s: %s' %(ticker,'Adjusted Open'))
    if acp=='on':
      plot.line(df.index, df['Adj. Close'], color='#0318fc', legend='%s: %s' %(ticker,'Adjusted Close'))
    #show(plot)
    script, div = components(plot)
    return script, div

@app.route('/', methods=['GET','POST'])
def index():
  return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
  ticker_input = request.form['tickerInput']
  year_input = request.form['yearInput']

  closing_price = request.form.get('closingPrice')
  adjusted_cp = request.form.get('adjustedCP')
  opening_price = request.form.get('openingPrice')
  adjusted_op = request.form.get('adjustedOP')

  df=getData(int(year_input), ticker_input)
  script, div = makePlot(df, ticker_input, int(year_input), closing_price, adjusted_cp, opening_price, adjusted_op)
  ticker_str = "https://www.google.com/finance?q="+ticker_input

  return  render_template('plot.html', div=div, script=script, ticker=ticker_str)

if __name__ == '__main__':
  app.run(port=33507)
