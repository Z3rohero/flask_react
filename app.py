from flask import Flask,request,jsonify,Response
from flask_pymongo import PyMongo,ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS


app = Flask(__name__)


config = {
    "username": "root",
    "password": "password",
    "server": "mongo",
}
connector = "mongodb://{}:{}@{}".format(config["username"], config["password"], config["server"])

app.config['MONGO_URI'] =connector

client=PyMongo(app)
cors = CORS(app, resources={r"/usuarios/*": {"origins": "*"}})


@app.route('/usuarios', methods=["post"])
def crear():
      nombre = request.json['nombre']
      password = request.json['password']
      email = request.json['email']
      if nombre  and password and email:
        cifrado = generate_password_hash(password)
        id = client.db.usuarios.insert_one({
            'nombre': nombre,     
            'password': cifrado,
            'email': email
            })
        response = {
            'id': str(id),
            'nombre': nombre,
            'email': email,    
            'password': cifrado,
                }
        return response
      else:
            {'message': 'No recibido'}
      return {'message': 'recibido'}

@app.route('/usuarios', methods=["GET"])
def usuarios():
    user=[]
    db= client.db.usuarios
    for doc in db.find():
        user.append({
            '_id':str(ObjectId(doc['_id'])),
            'nombre': doc['nombre'],
            'email': doc['email'],
            'password': doc['password']
        })
    
    return jsonify(user)
   

@app.route('/usuarios/<id>', methods=["GET"])
def getUser(id):
    user=client.db.usuarios.find_one({'_id':ObjectId(id)}) 
    return  jsonify({
        "encontrado usuario":str(ObjectId(user['_id'])),
         'nombre': user['nombre'],
          'email': user['email'],
        'password': user['password']
        })
   

@app.route('/usuarios/<id>', methods=["DELETE"])
def delUser(id):
     user=client.db.usuarios.delete_one({'_id':ObjectId(id)})
     return  jsonify({
        "Usuario eliminado":"usuario eliminado",
        })

@app.route('/usuarios/<id>', methods=["PUT"])
def setUser(id):
    password=request.json["password"]
    cifrado = generate_password_hash(password)
    ser=client.db.usuarios.update_one({'_id':ObjectId(id)},{
        '$set':{
            'nombre': request.json["nombre"],
             'email':request.json["email"],
             'password':cifrado
        }
    })
    return  jsonify({
        "message":"usuario añadido",
        })
   
@app.errorhandler(404)
def not_encontrado(error=None):
  message = jsonify({
    'message': 'Pagina no encontrada' + request.url,
    'status': 404
  })
  message.status_code = 404
  return message

if __name__=="__main__":
    app.run(debug=True)