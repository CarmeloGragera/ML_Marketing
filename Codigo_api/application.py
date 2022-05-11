from flask import Flask, jsonify, request
import os
import pickle
from sklearn.linear_model import Lasso
import pandas as pd
from sklearn.model_selection import train_test_split
from Funciones_y_clases import db_actualization

os.chdir(os.path.dirname(__file__))


app = Flask(__name__)
app.config['DEBUG'] = True

#model = pickle.load(open('ad_model.pkl','rb'))


@app.route('/', methods=['GET'])
def home():
    return """<html>

<head>
    <meta charset="utf-8" />
    <title>jQuery UI Datepicker - Uso básico</title>
    <link rel="stylesheet" href="css/style.css" />
    <script src="http://code.jquery.com/jquery-1.9.1.js"></script>
    <script src="http://code.jquery.com/ui/1.10.1/jquery-ui.js"></script>
    <script>
    $(function () {
        $("#datepicker").datepicker();
        });
    </script>
    </head>

<body>
    <h1>The Bridge Predicts</h1>
    <div>
        <h3>¿Quienes somos?</h3>
        <p>The Bridge Predicts somos un equipo de Data Scientist que trabajamos para hacer las mejores predicciones en el mercado.</p>
        <p>Trabajamos conlas mejores tecnicas y tecnologias del momento, ya que estamos en continua actualización, para dar el mejor servicio al cliente.</p>
    </div>
    <div>
        <button>Home</button>
        <button>Predict</button>
        <button>Retrain</button>
    </div>
    <div>
        <h3>Nuestro equipo:</h3>
        <p>Antonio, Carmelo, Enrique, Gretel, Lorenzo, Lucy, Miguel y Hector</p>
    </div>

<div id="datepicker">
    <p>Seleccione una fecha a predecir:</p>
</div>
</body>

<footer>
    <div>
        <h2>Contactanos</h2>
        <p>Perfil Github: https://github.com/CarmeloGragera/ML_Marketing_grupo_3</p>
    </div>
</footer>

</html>"""

# 1.Ruta para obtener todos los libros
@app.route('/api/database_update', methods=['GET'])
def get_all():
    action = db_actualization()
    return action


if __name__ == "__main__":
    app.debug = True
    app.run()