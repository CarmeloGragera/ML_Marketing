import os
from pandas.tseries.holiday import *
from pandas.tseries.offsets import CustomBusinessDay
from Funciones_y_clases import limpiar_csv, remove_outliers
import pandas as pd

data = pd.read_csv(os.path.join(os.path.dirname(__file__), 'users_web.csv')) 

data = limpiar_csv(data)
data = remove_outliers(data, 100)

data_prepared = data.to_csv(os.path.join(os.path.dirname(__file__),"users_web_TheBridge.csv"), index = False)
print(data.head())