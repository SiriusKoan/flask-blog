from flask import Flask, render_template, request
from flask_cors import CORS
import importlib
import functions
from models import *

app = Flask(__name__, template_folder = './templates/themes/%s'%(get_theme()))
CORS(app)



@app.route('/', methods = ['GET', 'POST'])
def index():
    return render_template('index.html', IMPORT = importlib.import_module)

if __name__ == '__main__':
    app.run(host = '127.0.0.1', port = 8080, debug = True)