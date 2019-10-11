"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from models import db, User, Task
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/hello', methods=['POST', 'GET'])
def handle_person():

    response_body = {
        "hello": "world"
    }

    return jsonify(response_body), 200


@app.route('/users', methods=['POST', 'GET'])
@app.route('/users/<int:id>', methods=['PUT', 'GET', 'DELETE'])
def users(id=None):

    if request.method == 'GET':
        if id is not None:
            user = User.query.get(id)
            return jsonify(user.serialize()), 200
        else:
            users = User.query.all()
            users = list(map(lambda x: x.serialize(), users))
            return jsonify(users), 200

    if request.method == 'POST':
        user = User()
        user.name = "Alguien"
        db.session.add(user)
        db.session.commit()
        return jsonify(user.serialize()), 200
    if request.method == 'PUT':
        user = User.query.get(id)
        user.name = "Monica Geller"
        db.session.commit()
        return jsonify(user.serialize()), 200
    if request.method == 'DELETE':
        user = User.query.get(id)
        user.delete()
        db.session.commit()

'''@app.route('/users/<username>', methods=['POST', 'GET', 'PUT', 'DELETE'])
def todolist(username):

   if request.method == 'GET':
        todo = Tasks.query.filter_by(username=username)
        return jsonify(todo.serialize()), 200
'''

# this only runs if `$ python src/main.py` is exercuted
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
