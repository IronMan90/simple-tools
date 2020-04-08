from flask import render_template, url_for, redirect
from main import app


@app.route('/')
def home():
    return render_template('home.html')
