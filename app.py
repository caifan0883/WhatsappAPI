from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

app = Flask(__name__)

#Configuración de la base de datos SQLITE
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///metapython.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

#Modelo de la tabla
class Log(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    fecha_y_hora = db.Column(db.DateTime, default=datetime.utcnow)
    texto = db.Column(db.TEXT)

#Crear una table si no existe
with app.app_context():
    db.create_all()



#Funcion para ordenar los registros por Fecha y Hora
def ordenar_por_fecha_y_hora(registros):
    return sorted(registros, key=lambda x: x.fecha_y_hora, reverse=True)

@app.route('/')

def index():
    #obtener todos los registros de la base de datos
    registros = Log.query.all()
    registros_ordenados = ordenar_por_fecha_y_hora(registros)
    return render_template('index.html', registros=registros_ordenados)


#Funcion para agregar mensajes y guardar en la base de datos
mesajes_log = []
def agregar_mensajes_log(texto):
    mesajes_log.append(texto)

    #Guardar mensajes en la BD
    nuevo_registro = Log(texto=texto)
    db.session.add(nuevo_registro)
    db.session.commit

#Token de configuracion para la verificacion
TOKE_WHATSAPP_API = "PCU"

@app.route('/webhook', methods=['GET','POST'])
def webhook():
    if request.method == 'GET':
        challenge = verificar_token(request)
        return challenge
    elif request.method == 'POST':
        response = recibir_mensajes(request)
        return response


def verificar_token(req):
    token = req.args.get('hub.verify_token')
    challenge = req.args.get('hub.challenge')

    if challenge and token == TOKE_WHATSAPP_API:
        return challenge
    else:
        return jsonify({'error' :'token invalido '}),401

def recibir_mensajes(req):
    #req = request.get_json()
    #agregar_mensajes_log(req)

    try:
        req = request.get_json()
        entry = req['entry'][0]
        changes = entry['changes'][0]
        value = changes['value'][0]
        objeto_mensaje = value['messages']

        agregar_mensajes_log(json.dumps(objeto_mensaje))
        
        return jsonify({'message': 'EVENT_RECEIVED'})
    except Exception as e:
        return jsonify({'message': 'EVENT_RECEIVED'})


    


if (__name__)=='__main__':
    app.run(host='0.0.0.0',port=80,debug=True)