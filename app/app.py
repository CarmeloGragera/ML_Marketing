from flask import Flask, jsonify, request
import os
import pickle
from sklearn.linear_model import Lasso
import pandas as pd
from sklearn.model_selection import train_test_split
import datetime #Importar módulo de fecha y hora

os.chdir(os.path.dirname(__file__))

today = datetime.date.today () #Obtener la fecha de hoy
yesterday = today - datetime.timedelta(days=1) #Restar la diferencia horaria con la fecha de hoy, el parámetro es 1 día, obtener la fecha de ayer
tomorrow = today + datetime.timedelta(days=1)

app = Flask(__name__)
app.config['DEBUG'] = True

model = pickle.load(open('ad_model.pkl','rb'))

@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"


@app.route('/api/v1/predict', methods=['GET'])
def predict():

    # En este caso, los argumentos lo introduce el usuario mediante un input. 
    tv = request.args.get('tv', None)
    radio = request.args.get('radio', None)
    newspaper = request.args.get('newspaper', None)

    if tv is None or radio is None or newspaper is None:
        return "Args empty, the data are not enough to predict"
    else:
        prediction = model.predict([[tv,radio,newspaper]])
    
    return jsonify({'predictions': prediction[0]})

@app.route('/api/v1/retrain', methods=['PUT'])
def train():

    primero_mes = '01/'+str(today.month)+'/'+str(today.year)
    fecha_dt = datetime.datetime.strptime(primero_mes, '%d/%m/%Y')

    # En este caso la obtención de datos sería con una query a AWS. 
    # data = pd.read_csv('data/Advertising.csv', index_col=0)


    data = data[data['fecha']<fecha_dt]

    # Aquí realizar transformaciones de datos para introducir en el modelo y entranarlo. 

    X_train, X_test, y_train, y_test = train_test_split(data.drop(columns=['sales']),
                                                        data['sales'],
                                                        test_size = 0.05,
                                                        random_state=42)

    model = Lasso(alpha=6000)
    model.fit(X_train, y_train)

    pickle.dump(model, open('ad_model.pkl', 'wb'))

    return "model trained and saved"


#app.run()