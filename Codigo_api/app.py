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

class DBController(): #Clase para controlar DB
    def __init__(self, database_route):
        self.database_route = database_route

    def querySQL(self, query, parameters=[]):
        con = sql.connect(self.database_route)
        cur = con.cursor()
        cur.execute(query, parameters)

        keys = []
        for item in cur.description:
            keys.append(item[0])

        responses = []
        for response in cur.fetchall():
            ix_clave = 0
            d = {}
            for column in keys:
                d[column] = response[ix_clave]
                ix_clave += 1
            responses.append(d)

        con.close()
        return responses
    
    def changeSQL(self, query, parameters):
        con = sql.connect(self.database_route)
        cur = con.cursor()
        cur.execute(query, parameters) 
        con.commit()
        con.close()

os.chdir(os.path.dirname(__file__))
database_sql = DBController()
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
    data = pd.read_csv('data/Users_web.csv')
    

    fecha = str(data['Date'].max())
    mes_max = int(fecha[5:7])
    anio_max = int(fecha[0:4])
    primero_mes = '01/'+str(today.month)+'/'+str(today.year)
    # Convertimos un string con formato <día>/<mes>/<año> en datetime
    fecha_dt = datetime.datetime.strptime(primero_mes, '%d/%m/%Y')


    if (anio_max<=today.year and today.month-mes_max>=2) or (anio_max<today.year and mes_max != 12):
        print('Este modelo no está actualizado')
    
        #Query
        fecha_query = "%" + fecha + "%"
        query = "SELECT * FROM database_sql WHERE Date >"+ str(fecha) + "AND Date < " +str(fecha_dt) 
        #Revisar, también puede ser 
        #"SELECT * FROM database_sql WHERE Date >" + str(fecha)
        database_sql.querySQL(query)                                

        #Reentrenar modelo

        new_data = pd.DataFrame(responses)

        ##Aqui van transformaciones de new data para luego concatenar con data(Llamar funciones de Antonio)
        # Habría que ver que nos devuelve el modelo para ver las transformaciones que debemos a hacer.

        data_concat = pd.concat([data, new_data], axis=0)
        X = data_concat["Data"]
        Y = data_concat["Otras columnas"]

        #Split de la nuestro dataset

        X_train, X_test, y_train, y_test = train_test_split(data.drop(columns=['sales']),
                                                        data['sales'],
                                                        test_size = 0.05,
                                                        random_state=42)
        
        #Reentrenar modelo 
        model.fit(X_train, y_train)

        #Calcular MAPE
        MAPE_nuevo_resultado = mean_absolute_percentage_error(y_test, model.predict(X_test))
        
        if MAPE_nuevo_resultado <= 0.20:
            pickle.dump(model, open('ad_model.pkl', 'wb'))
        
        else:
        # Nos falta el GridSearch.
        

        
        #Pasos:
        #Hacer query a Amazon y traer valores del último mes (Listo)
        # Añaadir a data las últimas filas solicitadas (Listo)
        # Reentrenar modelo con fichero csv actualizado
        # Calcular MAPE.
        # if MAPE < 0.20:
            # PERFECT
        # ELSE:
            #GRIDSEARCH.


    elif today.month-mes_max<2:
            print('Este modelo está actualizado')



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

=======
from flask import Flask, jsonify, request
import os
import pickle
from sklearn.linear_model import Lasso
import pandas as pd
from sklearn.model_selection import train_test_split

os.chdir(os.path.dirname(__file__))


app = Flask(__name__)
app.config['DEBUG'] = True

model = pickle.load(open('ad_model.pkl','rb'))

@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"


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
#app.run()