from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

#Configuración de la base de datos SQLITE
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///metapython.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

#Modelo de la tabla
class Log(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    fecha_y_hora = db.Column(db.DateTime, default=datetime.timezone.utc)
    texto = db.Column(db.TEXT)

#Crear una table si no existe
with app.app_context():
    db.create_all()

@app.route('/')

def index():
    #obtener todos los registros de la base de datos
    registros = Log.query.all()
    return render_template('index.html', registros=registros)


if (__name__)=='__main__':
    app.run(host='0.0.0.0',port=80,debug=True)