from flask import Flask, render_template
from flask_restful import Api, Resource, reqparse, abort
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
api = Api(app)


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

parser = reqparse.RequestParser()
parser.add_argument("fname", type=str, required=True, help='Primeiro Nome do aluno')
parser.add_argument("lname", type=str, required=True, help='Último Nome do aluno')


class Alunos(Resource):
    def get(self):
        alunos = [PEOPLE[key] for key in sorted(PEOPLE.keys())]
        return alunos
        
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
            abort(
                406,
                "Pessoa com sobrenome {lname} ja existe".format(lname=lname),
            )

class Aluno(Resource):
    ## Metodos específico que recebem parametro    
    def get(self, lname):
        if lname in PEOPLE:
            person = PEOPLE.get(lname)
        else:
            abort(
                404, "Pessoa com sobrenome {lname} nao encontrada".format(lname=lname)
            )
        return person

    def delete(self, lname):
        if lname in PEOPLE:
            del PEOPLE[lname]
            return "{lname} deletado com sucesso".format(lname=lname), 204
        else:
            abort(
                404, "Pessoa com sobrenome {lname} nao encontrada".format(lname=lname)
            )

    def put(self, lname):
        person = parser.parse_args()
        lname = person.get("lname", None)
        fname = person.get("fname", None)
        
        if lname in PEOPLE:
            PEOPLE[lname]["fname"] = person.get("fname")
            PEOPLE[lname]["timestamp"] = get_timestamp()
    
            return PEOPLE[lname]
        else:
            abort(
                404, "Pessoa com sobrenome {lname} nao encontrada".format(lname=lname)
            )

api.add_resource(Alunos, '/alunos')
api.add_resource(Aluno, '/alunos/<lname>')


@app.route('/')
def home(): 
    return render_template('alunos.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)
