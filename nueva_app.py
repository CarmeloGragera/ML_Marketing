from re import X
from urllib import response
from flask import Flask, jsonify, request
import os
import pickle
from jsonschema import draft201909_format_checker
from sklearn.linear_model import Lasso
import pandas as pd
from sklearn.model_selection import train_test_split
import sqlite3 as sql
from sklearn.metrics import mean_absolute_error, mean_squared_error, mean_absolute_percentage_error


os.chdir(os.path.dirname(__file__))

app = Flask(__name__)
app.config['DEBUG'] = True

model = pickle.load(open('ad_model.pkl','rb'))

@app.route('/', methods=['GET'])
def home():
    return "<h1>GRUPO 3 THE BRIDGE</h1><p>Home Link.</p>"

@app.route('/estamosjodidos', methods=['GET'])
def home():
    return "<h1>GRUPO 3 THE BRIDGE</h1><p>This link is made to show our users predictions.</p>"


#app.run()