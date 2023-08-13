from flask import Flask, jsonify, request
from flask_cors import CORS 
from supabase_py import create_client

app = Flask(__name__)
CORS(app)

url = 'https://kcsglpfknijpobwqtemd.supabase.co'
key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imtjc2dscGZrbmlqcG9id3F0ZW1kIiwicm9sZSI6ImFub24iLCJpYXQiOjE2OTE4ODEzNzksImV4cCI6MjAwNzQ1NzM3OX0.vqeqORS-CxkbRPQz9mIe4962XoewNLlhX63CZkdH2mE'
sp = create_client(url, key)

@app.route('/', methods=['GET'])
def index():
    
    return jsonify({
        'payload': 'welcome'
    })


@app.route('/list', methods=['GET'])
def get_users():
    rs = sp.table('usuarios').select('*').execute()

    return jsonify(rs)


@app.route('/user/<id>', methods=['GET'])
def get_user(id):
    rs = sp.table('usuarios').select('*').filter('id','eq', id).execute()
    user = rs['data']
    
    if user: 
        return jsonify(user), 200
    else :
        return jsonify({'message': 'user not found'}), 404


@app.route('/create', methods=['POST'])
def create_user():
    user = request.get_json()
    id = user['id']
    nombre = user['nombre']
    correo = user['correo']
    edad = user['edad']

    data, count= sp.table('usuarios').insert({
        'id': id,
        'nombre': nombre,
        'correo': correo,
        'edad': edad
    }).execute()

    return jsonify(data)


@app.route('/delete/<id>', methods=['DELETE'])
def delete_user(id):
    rs = sp.table('usuarios').delete().filter('id', 'eq', id).execute()

    if rs['status_code'] == 200: 
        return jsonify({'message': 'user deleted'}), 200
    
    return jsonify ({
        'message' : 'User not found'
    }), 404


@app.route('/update/<id>', methods=['PUT'])
def update_user(id):

    user = request.get_json()
    id = user['id']
    nombre = user['nombre']
    correo = user['correo']
    edad = user['edad']
    
    rs1 = sp.table('usuairios').select('*')
    
    rs = sp.table('usuarios').update(
        }, {
            'id': id,
            'nombre': nombre,
            'correo': correo,
            'edad': edad
        }).execute()

    return rs

if __name__ == '__main__':
    app.run(debug=True)