<<<<<<< HEAD
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
from Funciones_y_clases import data_aws


os.chdir(os.path.dirname(__file__))
today = datetime.date.today () #Obtener la fecha de hoy
=======
from flask import Flask, jsonify, request
import os
import pickle
from sklearn.linear_model import Lasso
import pandas as pd
from sklearn.model_selection import train_test_split

os.chdir(os.path.dirname(__file__))

>>>>>>> eb52142d20121edf74c6d2212d34b78babaab57f

app = Flask(__name__)
app.config['DEBUG'] = True

model = pickle.load(open('ad_model.pkl','rb'))

<<<<<<< HEAD
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
=======
@app.route('/', methods=['GET'])
def home():
    return "<h1>Grupo 3 THE BRIDGE</h1><p>Home Link.</p>"


@app.route('/api/v1/predict', methods=['GET'])
def predict():

    tv = request.args.get('tv', None)
    radio = request.args.get('radio', None)
    newspaper = request.args.get('newspaper', None)

    if tv is None or radio is None or newspaper is None:
        return "Args empty, the data are not enough to predict"
    else:
        prediction = model.predict([[tv,radio,newspaper]])

    return jsonify({'predictions': prediction[0]})

@app.route('/api/v1/retrain', methods=['GET'])
def train():
    data = pd.read_csv('data/Advertising.csv', index_col=0)

    X_train, X_test, y_train, y_test = train_test_split(data.drop(columns=['sales']),
                                                        data['sales'],
                                                        test_size = 0.05,
                                                        random_state=42)

    model = Lasso(alpha=6000)
    model.fit(X_train, y_train)

    pickle.dump(model, open('ad_model.pkl', 'wb'))

    return "model trained and saved"
>>>>>>> eb52142d20121edf74c6d2212d34b78babaab57f
