from flask import Flask, jsonify, request
import os
import pickle
from sklearn.linear_model import Lasso
import pandas as pd
from sklearn.model_selection import train_test_split

os.chdir(os.path.dirname(__file__))


app = Flask(__name__)