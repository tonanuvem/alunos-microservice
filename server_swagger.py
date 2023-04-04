from flask import Flask, current_app, render_template
from flask import request, Blueprint

from flask_cors import CORS
from flask_restful.reqparse import RequestParser

from flask_restful_swagger_3 import swagger, get_swagger_blueprint
from flask_restful_swagger_3 import Api, swagger, Resource, abort
from flask_restful_swagger_3 import Schema

from datetime import datetime
#from views_blueprint import get_user_resources

######

app = Flask(__name__)
CORS(app, resources={"/api/*": {"origins": "*"}})


def auth(api_key, endpoint, method):
    # Space for your fancy authentication. Return True if access is granted, otherwise False
    return True

swagger.auth = auth

######

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

class SimpleEmailModel(Schema):
    type = 'string'
    
class EmailModel(Schema):
    type = 'string'
    format = 'email'

class SuperUserModel(Schema):
    type = 'object'
    properties = {
        'id': {
            'type': 'integer',
            'format': 'int64',
        },
        'mail': SimpleEmailModel,
    }
    required = ['id']

class KeysModel(Schema):
    type = 'string'
    
class UserModel(SuperUserModel):
    properties = {
        'name': {
            'type': 'string'
        },
        'mail': EmailModel,
        'keys': KeysModel.array(),
        'user_type': {
            'type': 'string',
            'enum': ['admin', 'regular'],
            'nullable': True
        },
        'password': {
            'type': 'string',
            'format': 'password',
            'load_only': True
        }
    }
    required = ['name']
    
#####

known_users = []


class UserResource(Resource):
    @swagger.tags('users')
    @swagger.reorder_with(UserModel, response_code=200, summary="Add User")
    @swagger.parameter(_in='query', name='query', schema=UserModel, required=True, description='query')
    def post(self, _parser):
        """
        Adds a user
        """
        # Validate request body with schema model
        try:
            data = UserModel(**_parser.parse_args())

        except ValueError as e:
            return ErrorModel(**{'message': e.args[0]}), 400

        data['id'] = len(known_users) + 1
        known_users.append(data)

        return data, 201, {'Location': request.path + '/' + str(data['id'])}

    @swagger.tags('users')
    @swagger.response(response_code=200)
    def get(self):
        """
        Returns all users.
        """
        users = ([u for u in known_users if u['name']])

        # Return data through schema model
        return list(map(lambda user: UserModel(**user), users)), 200
        # return "success"


class UserItemResource(Resource):
    @swagger.tags('user')
    @swagger.response(response_code=200)
    def get(self, user_id):
        """
        Returns a specific user.
        :param user_id: The user identifier
        """
        user = next((u for u in known_users if u['id'] == user_id), None)

        if user is None:
            return ErrorModel(**{'message': "User id {} not found".format(user_id)}), 404

        # Return data through schema model
        return UserModel(**user), 200

#####

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
    @swagger.tags('alunos')
    @swagger.response(response_code=200)
    def get(self):
        """
        Returns all users.
        """
        alunos = [PEOPLE[key] for key in sorted(PEOPLE.keys())]
        return alunos, 200
        #users = ([u for u in PEOPLE if u['lname']])
        # Return data through schema model
        #return list(map(lambda user: AlunoModel(**user), users)), 200
        # return "success"
        
    @swagger.tags('alunos')
    @swagger.reorder_with(AlunoModel, response_code=200, summary="Adicionar Aluno")
    @swagger.parameter(_in='query', name='query', schema=AlunoModel, required=True, description='query')
    def post(self, _parser):
        """
        Adds a user
        """
        # Validate request body with schema model
        try:
            data = AlunoModel(**_parser.parse_args())

        except ValueError as e:
            return ErrorModel(**{'message': e.args[0]}), 400

        #data['id'] = len(known_users) + 1
        #known_users.append(data)
        #return data, 201, {'Location': request.path + '/' + str(data['id'])}
        
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

'''        
class Alunos(Resource):
    @swagger.tags('alunos')
    @swagger.response(response_code=200)
    def get(self):
        alunos = [PEOPLE[key] for key in sorted(PEOPLE.keys())]
        return alunos, 200

    @swagger.tags('users')
    @swagger.reorder_with(AlunoModel, response_code=200, summary="Add User")
    @swagger.parameter(_in='query', name='query', schema=AlunoModel, required=True, description='query')
    def post(self):
        person = parser.parse_args()
        lname = person.get("lname", None)
        fname = person.get("fname", None)
    
        if lname not in PEOPLE and lname is not None:
            PEOPLE[lname] = {
                "lname": lname,
                "fname": fname,
                "timestamp": get_timestamp(),
            }
            return "{lname} criado com sucesso".format(lname=lname), 201
        else:
            abort(406, message="Pessoa com sobrenome {lname} ja existe".format(lname))
'''

class Aluno(Resource):
    @swagger.tags('alunos')
    @swagger.response(response_code=200)
    def get(self, lname):
        if lname in PEOPLE:
            person = PEOPLE.get(lname)
        else:
            abort(404, message="Pessoa com sobrenome {lname} nao encontrada".format(lname))
        return person
        """
        Returns a specific user.
        :param user_id: The user identifier
        """
        '''
        user = next((u for u in known_users if u['id'] == user_id), None)

        if user is None:
            return ErrorModel(**{'message': "User id {} not found".format(user_id)}), 404

        # Return data through schema model
        return UserModel(**user), 200
        '''

'''
class Aluno(Resource):
    ## Metodos específico que recebem parametro    
    @swagger.tags('aluno')
    @swagger.response(response_code=200)
    def get(self, lname):
        if lname in PEOPLE:
            person = PEOPLE.get(lname)
        else:
            abort(404, message="Pessoa com sobrenome {lname} nao encontrada".format(lname))
        return person

    def delete(self, lname):
        if lname in PEOPLE:
            del PEOPLE[lname]
            return "{lname} deletado com sucesso".format(lname=lname), 204
        else:
            abort(404, message="Pessoa com sobrenome {lname} nao encontrada".format(lname))

    def put(self, lname):
        person = parser.parse_args()
        lname = person.get("lname", None)
        fname = person.get("fname", None)
        
        if lname in PEOPLE:
            PEOPLE[lname]["fname"] = person.get("fname")
            PEOPLE[lname]["timestamp"] = get_timestamp()
    
            return PEOPLE[lname]
        else:
            abort(404, message="Pessoa com sobrenome {lname} nao encontrada".format(lname))
'''


#####


def get_user_resources():
    """
    Returns user resources.
    :param app: The Flask instance
    :return: User resources
    """
    
    #blueprint = Blueprint('user', __name__)
    blueprint = Blueprint('aluno', __name__)

    api = Api(blueprint)

    api.add_resource(UserResource, '/api/users')
    api.add_resource(UserItemResource, '/api/users/<int:user_id>')
    
    #api.add_resource(AlunosResource, '/api/alunos')

    api.add_resource(Alunos, '/api/alunos')
    #api.add_resource(Aluno, '/api/alunos/<str:lname>')

    return api

# Get user resources
user_resources = get_user_resources()

# Register the blueprint for user resources
app.register_blueprint(user_resources.blueprint)

# Prepare a blueprint to server the combined list of swagger document objects and register it
#servers = [{"url": "http://localhost:5000"}]

SWAGGER_URL = '/api/doc'  # URL for exposing Swagger UI (without trailing '/')
API_URL = 'swagger.json'  # Our API url (can of course be a local resource)

app.config.setdefault('SWAGGER_BLUEPRINT_URL_PREFIX', '/swagger')

with app.app_context():
    swagger_blueprint = get_swagger_blueprint(
        user_resources.open_api_object,
        swagger_prefix_url=SWAGGER_URL,
        swagger_url=API_URL,
        title='Alunos Microservice', version='1')#, servers=servers)


app.register_blueprint(swagger_blueprint, url_prefix='/swagger')

@app.route('/')
def home(): 
    return render_template('alunos.html')
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5007, debug=True)
