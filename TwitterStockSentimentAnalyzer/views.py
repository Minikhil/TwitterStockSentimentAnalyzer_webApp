"""
Routes and views for the flask application.
"""

from datetime import datetime
from datetime import date
from flask import render_template
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField, validators
from wtforms.validators import DataRequired
from TwitterStockSentimentAnalyzer import app
from TwitterStockSentimentAnalyzer.TwitterAnalyzer import TwitterAnalyzer
import os

app.config['SECRET_KEY'] = "tothemoon"
class TickerInput(FlaskForm):
  ticker = StringField('ticker', validators=[DataRequired()])

@app.route('/', methods =['GET', 'POST'])
@app.route('/home', methods =['GET', 'POST'])
def home():
    """Renders the home page."""
    ticker = None
    today = datetime.today(),
    form = TickerInput()
    form.validate()
    #if form.is_submitted():
    #    ticker = form.ticker.data
    #    return render_template(
    #        'contact.html',
    #        title= ticker,
    #        today = today,
    #        message='Analysis:'
    #)
    if form.validate_on_submit():
      ticker = form.ticker.data
      data = TwitterAnalyzer(ticker)
      path = os.path.dirname(os.path.realpath(__file__))
      imagedir = '/'.join([path,'static/images/plotGraph.png'])
      return render_template(
            'contact.html',
            title= ticker,
            today = today,
            message='Analysis:',
            url = imagedir
    )
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year, form = form
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )
