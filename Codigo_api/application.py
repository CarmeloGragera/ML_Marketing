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

model = pickle.load(open('ad_model.pkl','rb'))

@app.route('/')


@app.route('/', methods=['GET'])
def home():
    return """<html>

<head>

<script src="http://code.jquery.com/jquery-1.9.1.js"></script>
    <script src="http://code.jquery.com/ui/1.10.1/jquery-ui.js"></script>
    <script>
    $(function () {
        $("#datepicker").datepicker();
        });
    </script>

    <meta charset="utf-8" />
    <title>The Bridge Predicts</title>

    <style>
        *{
    background-image: url("img/Fondos-para-paginas-web-grandes.jpg");
    background-position-x: center;
    background-position-y: center;
}

body {
    width: 80%;
    margin: 0px auto;
    border: 1px solid black;
    height: auto;
    background:white;
    font-family: 'Trebuchet MS', 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Arial, sans-serif;
}

#container{
    width: 100%;
    margin: 0px auto;
    border: 1px solid black;
    background: rgb(48, 47, 73);
}

header{
    color: white;
    text-align: center;
    background: rgb(48, 47, 73);
}

h1{
    background: rgb(48, 47, 73);
}




nav ul li{
    float: left;
    list-style: none;
    margin: 20px;
    line-height: 15px;
    text-align: center;
    background: white;
}

a{
    background: white;
    outline: none;
    text-decoration: none;
    color: rgb(0, 0, 0);
    text-align: center;
    display: inline-block;
}

.clearfix{
    clear:both;
}


div{
    width: 90%;
    text-align: justify;
    background: white;
    margin: 0px auto;
}

p{
    width: 90%;
    text-align: justify;
    background: white;
    margin: 0px auto;
}

h2{
    width: 90%;
    text-align: justify;
    background: white;
    margin: 0px auto;
}

h3{
    width: 90%;
    text-align: justify;
    background: white;
    margin: 0px auto;
}

.about{
    color: black;
    width: 80%;
    margin: 0px auto;
    border: 1px solid black;
    height: auto;
    background:white;
}





footer{
    width: 100%;
    margin: 0px auto;
    border: 1px solid black;
    background: rgb(48, 47, 73);
    color: white;}

#footer{
    background: rgb(48, 47, 73);
    text-align: center;
}
.footer{
    background: rgb(48, 47, 73);


}
    </style>
</head>



<body>


    <div id="container">

        <header>
            <h1>The Bridge Predictions</h1>
        </header>
    </div>

    <div id="nav">
        <nav>
            <ul>
                <li>
                    <a href="">Home</a>
                </li>
                <li>
                    <a href="">Predictions</a>
                </li>
                <li>
                    <a href="">Contact</a>
                </li>
            </ul>
        </nav>
    </div>





    <div class="clearfix"></div>


    <div class="imagen"></div>

    <div id="datepicker">
        <br>
        <br>
    <p>Seleccione una fecha a predecir:</p>
    </div>

    <div class="clearfix"></div>
    <div>
        <br>
        <br>
        <h3>¿Quienes somos?</h3>
        <br>
        <p>The Bridge Predicts somos un equipo de Data Scientist que trabajamos para hacer las mejores predicciones en el mercado.</p>
        <p>Trabajamos conlas mejores tecnicas y tecnologias del momento, ya que estamos en continua actualización, para dar el mejor servicio al cliente.</p>
    </div>
    <div>
        <br>
        <br>
    </div>
    <br>
</body>

<footer>
    <div class="footer">
        <h2 id="footer">Contactanos</h2>
        <br>
        <p id="footer">LinkedIn: <a href="https://www.linkedin.com/in/ovivas/">OmarVivas</a></p>
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