from pandas.tseries.holiday import AbstractHolidayCalendar, Holiday, Easter, Day, sunday_to_monday

# Clase para añadir los días festivos a nuestro dataframe:
class calendario_fiestas_españa(AbstractHolidayCalendar):
    
    """
        Para usar esta clase primero tenemos que cargar 
    la librería de 'pandas.tseries.holiday'.
    
        Esta clase se utiliza dentro de la función 'limpiar_csv()'
    para poder sacar los días festivos.
    """
    
    dias = [
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
    
        Esta función requiere la clase 'calendario_fiestas_españa' para
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
        
        if date in seasons['spring']:
            return 'spring'
        
        if date in seasons['summer']:
            return 'summer'
        
        if date in seasons['autumn']:
            return 'autumn'
        
        else:
            return 'winter'
        
    df['season'] = df["Date"].map(season_of_date)
    df["weekend"] = df["weekend"].replace(True,1)
    df["weekend"] = df["weekend"].replace(False,0)
    
    cal = calendario_fiestas_españa()
    holidays = cal.holidays(start=df["Date"].min(), end=df["Date"].max())
    
    df["festivo"] = df["Date"].isin(holidays)
    df["festivo"] = df["festivo"].replace(True,1)
    df["festivo"] = df["festivo"].replace(False,0)
    
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