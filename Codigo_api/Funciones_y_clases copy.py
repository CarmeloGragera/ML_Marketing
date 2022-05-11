from pandas.tseries.holiday import *
from pandas.tseries.offsets import CustomBusinessDay
import pandas as pd
import pymysql


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

def data_aws():
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

    sql = '''SELECT * FROM users_web'''
    cursor.execute(sql)
    mi_tabla = cursor.fetchall()

    data = pd.DataFrame(mi_tabla)

    db.close()

    return data

def equipo2_aws():
    username = "admin"
    password = "Grupo2AWS"
    host = "web-users.czjoi0srhr5i.eu-west-3.rds.amazonaws.com"
        
    db = pymysql.connect(host = host,
                        user = username,
                        password = password,
                        cursorclass = pymysql.cursors.DictCursor
    )

    # El objeto cursor es el que ejecutará las queries y devolverá los resultados
    cursor = db.cursor()

    cursor.connection.commit()
    use_db = ''' USE users_web_db'''
    cursor.execute(use_db)

    sql = '''SELECT * FROM users_web'''
    cursor.execute(sql)
    mi_tabla = cursor.fetchall()

    data = pd.DataFrame(mi_tabla)

    db.close()

    return data