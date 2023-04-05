from flask import Flask, current_app, render_template
from flask import request, Blueprint

from flask_cors import CORS
from flask_restful.reqparse import RequestParser

# https://pypi.org/project/flask-restful-swagger-3/
from flask_restful_swagger_3 import swagger, get_swagger_blueprint
from flask_restful_swagger_3 import Api, swagger, Resource, abort
from flask_restful_swagger_3 import Schema

from datetime import datetime

######
# Segurança e Autenticação

app = Flask(__name__)
CORS(app, resources={"/api/*": {"origins": "*"}})


def auth(api_key, endpoint, method):
    # Space for your fancy authentication. Return True if access is granted, otherwise False
    return True

swagger.auth = auth

######
# Modelo de Entidade com suas propriedades

class AlunoModel(Schema):
    properties = {
        'fname': {
            'type': 'string'
        },
        'lname': {
            'type': 'string'
        },
    }
    required = ['lname']

class ErrorModel(Schema):
    type = 'object'
    properties = {
        'message': {
            'type': 'string'
        }
    }

#####
# Rotas e Endpoints

def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

PEOPLE = {
    "Jones": {
        "fname": "Indiana",
        "lname": "Jones",
        "timestamp": get_timestamp(),
    },
    "Sparrow": {
        "fname": "Jack",
        "lname": "Sparrow",
        "timestamp": get_timestamp(),
    },
    "Snow": {
        "fname": "John",
        "lname": "Snow",
        "timestamp": get_timestamp(),
    },
}

class Alunos(Resource):
    
    # Get:
    @swagger.tags('alunos')
    @swagger.response(response_code=200)
    def get(self):
        """
        Returns all users.
        """
        alunos = [PEOPLE[key] for key in sorted(PEOPLE.keys())]
        return alunos, 200
    
    # Post:    
    @swagger.tags('alunos')
    @swagger.reorder_with(AlunoModel, response_code=200, summary="Adicionar Aluno")
    @swagger.parameter(_in='query', name='query', schema=AlunoModel, required=True, description='query')
    def post(self, _parser):
        """
        Adds a user
        """
        # Validate request body with schema model:
        try:
            data = AlunoModel(**_parser.parse_args())

        except ValueError as e:
            return ErrorModel(**{'message': e.args[0]}), 400
        
        # Inserir o item:
        lname = data.get("lname", None)
        fname = data.get("fname", None)
        if lname not in PEOPLE and lname is not None:
            PEOPLE[lname] = {
                "lname": lname,
                "fname": fname,
                "timestamp": get_timestamp(),
            }
            return "{lname} criado com sucesso".format(lname=lname), 201
        else:
            abort(406, message="Pessoa com sobrenome {lname} ja existe".format(lname))



class Aluno(Resource):
    # Get:
    @swagger.tags('alunos')
    @swagger.response(response_code=200)
    def get(self, lname):
        """
        Returns a specific user.
        :param user_id: The user identifier
        """
        if lname in PEOPLE:
            person = PEOPLE.get(lname)
        else:
            abort(404, message="Pessoa com sobrenome "+lname+ " nao encontrada")
        return person, 200
    
    # Put:
    @swagger.tags('alunos')
    @swagger.response(response_code=200)
    def put(self, lname):
        """
        Returns a specific user.
        :param user_id: The user identifier
        """
        if lname in PEOPLE:
            person = PEOPLE.get(lname)
            PEOPLE[lname]["fname"] = person.get("fname")
            PEOPLE[lname]["timestamp"] = get_timestamp()
            return PEOPLE[lname]
        else:
            abort(404, message="Pessoa com sobrenome "+lname+ " nao encontrada")
        return person, 200
        
    # Delete:
    @swagger.tags('alunos')
    @swagger.response(response_code=200)
    def delete(self, lname):
        """
        Returns a specific user.
        :param user_id: The user identifier
        """
        if lname in PEOPLE:
            del PEOPLE[lname]
            return "{lname} deletado com sucesso".format(lname=lname), 204
        else:
            abort(404, message="Pessoa com sobrenome "+lname+ " nao encontrada")


#####
# https://realpython.com/flask-blueprint/
# Instead of coding your application from scratch, you may consider searching for an existing Flask Blueprint or Extension that you can reuse.

def get_resources():
    """
    Returns resources.
    :param app: The Flask instance
    :return: User resources
    """
    
    blueprint = Blueprint('api', __name__)

    api = Api(blueprint)

    #api.add_resource(UserResource, '/api/users')
    #api.add_resource(UserItemResource, '/api/users/<int:user_id>')

    api.add_resource(Alunos, '/api/alunos')
    api.add_resource(Aluno, '/api/users/<string:lname>')

    return api

# Get resources
api_resources = get_resources()

# Register the blueprint for user resources
app.register_blueprint(api_resources.blueprint)

# Prepare a blueprint to server the combined list of swagger document objects and register it
#servers = [{"url": "http://localhost:5000"}]

SWAGGER_URL = '/api/doc'  # URL for exposing Swagger UI (without trailing '/')
API_URL = 'swagger.json'  # Our API url (can of course be a local resource)

app.config.setdefault('SWAGGER_BLUEPRINT_URL_PREFIX', '/swagger')

with app.app_context():
    swagger_blueprint = get_swagger_blueprint(
        api_resources.open_api_object,
        swagger_prefix_url=SWAGGER_URL,
        swagger_url=API_URL,
        title='Alunos Microservice', version='1')#, servers=servers)


app.register_blueprint(swagger_blueprint, url_prefix='/swagger')

@app.route('/')
def home(): 
    return render_template('alunos.html')
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
