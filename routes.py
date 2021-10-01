from flask import Flask, render_template, url_for, flash, redirect, request, abort

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return render_template('layout.html', title='Home')
