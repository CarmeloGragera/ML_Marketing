from pandas.tseries.holiday import *
from pandas.tseries.offsets import CustomBusinessDay
import pandas as pd
import pymysql
import datetime 
import pickle
from sklearn.metrics import mean_absolute_error, mean_squared_error, mean_absolute_percentage_error
from sklearn.linear_model import LinearRegression
import os

os.chdir(os.path.dirname(__file__))




class calendario_fiestas_espana(AbstractHolidayCalendar):
   
   """
      Esta clase se utiliza dentro de la función 'limpiar_csv()' 
   para agregar la columna de días festivos.
   """
   
   rules = [
     Holiday('Año Nuevo', month=1, day=1, observance=sunday_to_monday),
     Holiday('Epifanía del Señor', month=1, day=6, observance=sunday_to_monday),
     Holiday('Viernes Santo', month=1, day=1, offset=[Easter(), Day(-2)]),
     Holiday('Día del Trabajador', month=5, day=1, observance=sunday_to_monday),
     Holiday('Asunción de la Virgen', month=8, day=15, observance=sunday_to_monday),
     Holiday('Día de la Hispanidad', month=10, day=12, observance=sunday_to_monday),
     Holiday('Todos los Santos', month=11, day=1, observance=sunday_to_monday),
     Holiday('Día Constitución', month=12, day=6, observance=sunday_to_monday),
     Holiday('Inmaculada Concepción', month=12, day=8, observance=sunday_to_monday),	    
     Holiday('Navidad', month=12, day=25, observance=sunday_to_monday)
   ]

# Función para crear el dataframe con las nuevas columnas a partir
# de los datos de la página:
def limpiar_csv(df):
    
    """
        Librerías necesarias para poder ejecutar esta función.
    """
    
    from pandas import DatetimeIndex
    from pandas import to_datetime
    from pandas import date_range
    
    """
        Recibe un dataframe como parámetro y 
    lo devuelve con las nuevas columnas añadidas
    
        Esta función requiere la clase 'calendario_fiestas_espana' para
    poder hacer uso de ella.
    """

    df['Date'] = to_datetime(df['Date'], format="%d/%m/%Y")
    df['year'] = DatetimeIndex(df['Date']).year 
    df['month'] = DatetimeIndex(df['Date']).month
    df['day'] = DatetimeIndex(df['Date']).day
    df['day of week'] = df['Date'].dt.dayofweek
    df["weekend"] = df["day of week"] > 4
    
    def season_of_date(date):
        """
            Esta función añade la columna de las estaciones del año
        acorde a las fechas que encuentre en la columna de 'Date'.
        
        """
    
        year = str(date.year)
        
        seasons = {'spring': date_range(start='21/03/'+year, end='20/06/'+year),
                'summer': date_range(start='21/06/'+year, end='22/09/'+year),
                'autumn': date_range(start='23/09/'+year, end='20/12/'+year)}
        
        """
            Las estaciones del año estan ponderadas en función de la media de
        usuarios que visitan la página en dichas estaciones:
        
            1 - spring: 33.93181818181818
            2 - autumn: 36.91525423728814        
            3 - winter: 38.43700787401575
            4 - summer: 41.42702702702703
        """
        if date in seasons['spring']:
            return 1
        
        if date in seasons['summer']:
            return 4
        
        if date in seasons['autumn']:
            return 2
        
        else:
            return 3
        
    df['season'] = df["Date"].map(season_of_date)
    df["weekend"] = df["weekend"].replace(True,1)
    df["weekend"] = df["weekend"].replace(False,0)
    
    cal = calendario_fiestas_espana()
    holidays = cal.holidays(start=df["Date"].min(), end=df["Date"].max())
    
    df["festivo"] = df["Date"].isin(holidays)
    df["festivo"] = df["festivo"].replace(True,1)
    df["festivo"] = df["festivo"].replace(False,0)

    """
        eliminar la primera columna ya no necesaria
    """

    df = df.iloc[:,1:] 



    return df


# Función para eliminar outliers:
def remove_outliers(df, limit):
    
    """
        Recibe como primer parámetro el dataframe y como segundo el límite
    de usuarios máximos que quieres filtrar para la columna de 'Users',
    para evitar los outliers. 
    """
    
    df = df.drop(df[df['Users']>limit].index)
    return df

## Cómo usar:

"""

from pandas import read_csv

df = read_csv("users_web.csv")

df = limpiar_csv(df)

remove_outliers(df,100)

"""

def data_aws(sqr):
    username = "admin"
    password = "Engamu1991"
    host = "database-1.c8psbqlfu9e7.us-east-1.rds.amazonaws.com"

    db = pymysql.connect(host = host,
                        user = username,
                        password = password,
                        cursorclass = pymysql.cursors.DictCursor
    )

    # El objeto cursor es el que ejecutará las queries y devolverá los resultados
    cursor = db.cursor()

    cursor.connection.commit()
    use_db = ''' USE user_web'''
    cursor.execute(use_db)


    # insertamos todo el dataframe

    cursor.execute(sqr)
    mi_tabla = cursor.fetchall()

    data = pd.DataFrame(mi_tabla)

    db.close()

    return data


def db_actualization():
    today = datetime.date.today () #Obtener la fecha de hoy
    data = data_aws('''SELECT * FROM user_web''')
    data['Date'] = pd.to_datetime(data['Date'], format="%Y-%m-%d")
    df = pd.read_csv("data/user_web_final.csv", index_col=0)
    df['Date'] = pd.to_datetime(df['Date'], format="%Y-%m-%d")

    fecha = str(data['Date'].max())
    fecha_df = str(df['Date'].max())
    mes_max = int(fecha_df[5:7])
    anio_max = int(fecha_df[0:4])
    primero_mes = '01/'+str(today.month)+'/'+str(today.year)
    # # Convertimos un string con formato <día>/<mes>/<año> en datetime
    fecha_dt = str(datetime.datetime.strptime(primero_mes, '%d/%m/%Y'))


    if (anio_max<=today.year and today.month-mes_max>=2) or (anio_max<today.year and mes_max != 12):

        new_data = data_aws("SELECT * FROM user_web WHERE Date between "+ "'" + fecha_df[0:10] + "'" + " AND " + "'" + fecha_dt[0:10] + "'")
        df = pd.read_csv("data/user_web_final.csv", index_col=0)
        season_dict = {"spring": 1, "summer": 4, "autumn": 2, "winter": 3}
        new_data["season"] = new_data["season"].replace(season_dict)
        df["season"] = df["season"].replace(season_dict)


        df_2 = pd.concat([df, new_data], axis=0)

        X = df_2.drop(columns=["Users","Date"])
        Y = df_2["Users"]

        X_train = X[:-140]
        X_test = X[-140:]

        Y_train = Y[:-140]
        Y_test = Y[-140:]

        model_2 = LinearRegression()
        model_2.fit(X_train, Y_train)

        prediction = model_2.predict(X_test)

        new_mape = mean_absolute_percentage_error(Y_test, prediction)

        if new_mape <= 0.25:

            pickle.dump(model_2, open('ad_model.pkl', 'wb'))
            return print("Tu modelo ha sido actualizado")

        else:
            return print("Tu modelo antiguo ofrece mejores resultados.")

    else:
        print('Tu modelo actualizado a la última')