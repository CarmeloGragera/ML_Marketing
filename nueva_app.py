from http.client import responses
from re import X
from urllib import response
from flask import Flask, jsonify, request
import os
import pickle
from jsonschema import draft201909_format_checker
from sklearn.linear_model import Lasso
import pandas as pd
from sklearn.model_selection import train_test_split
import datetime #Importar módulo de fecha y hora
import sqlite3 as sql
from sklearn.metrics import mean_absolute_error, mean_squared_error, mean_absolute_percentage_error


os.chdir(os.path.dirname(__file__))
today = datetime.date.today () #Obtener la fecha de hoy

app = Flask(__name__)
app.config['DEBUG'] = True

model = pickle.load(open('ad_model.pkl','rb'))

@app.route('/estamosjodidos', methods=['GET'])
def home():
    return "<h1>GRUPO 3 THE BRIDGE</h1><p>This link is made to show our users predictions.</p>"

#@app.route('/api/v1/retrain', methods=['PUT'])
#def train():
#    data = data_aws()
#    data['Date'] = data['Date']
#    fecha = str(data['Date'].max())
#    mes_max = int(fecha[5:7])
#    anio_max = int(fecha[0:4])
#    primero_mes = '01/'+str(today.month)+'/'+str(today.year)
#    Convertimos un string con formato <día>/<mes>/<año> en datetime
#    fecha_dt = datetime.datetime.strptime(primero_mes, '%d/%m/%Y')
    

#app.run()