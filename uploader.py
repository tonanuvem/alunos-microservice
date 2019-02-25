# System modules
from datetime import datetime

# 3rd party modules
from flask import jsonify, make_response, abort


def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))


# Data to serve with our API
FILES = {
    "1": {
        "name": "exemplo.pdf",
        "timestamp": get_timestamp(),
    },
    "2": {
        "name": "outro-exemplo.pdf",
        "timestamp": get_timestamp(),
    },
}


def read_all():
    """
    This function responds to a request for /api/people
    with the complete lists of people
    :return:        json string of list of people
    """
    # Create the list of people from our data
    dict_files = [FILES[key] for key in sorted(FILES.keys())]
    arquivos = jsonify(dict_files)
    qtd = len(dict_alunos)
    content_range = "alunos 0-"+str(qtd)+"/"+str(qtd)
    # Configura headers
    arquivos.headers['Access-Control-Allow-Origin'] = '*'
    arquivos.headers['Access-Control-Expose-Headers'] = 'Content-Range'
    arquivos.headers['Content-Range'] = content_range
    return arquivos



def read_one(name):
    """
    This function responds to a request for /api/people/{lname}
    with one matching person from people
    :param lname:   last name of person to find
    :return:        person matching last name
    """
    # Does the person exist in people?
    if name in FILES:
        arquivo = FILES.get(name)

    # otherwise, nope, not found
    else:
        abort(
            404, "Arquivo com nome {name} não encontrado".format(name=name)
        )

    return person


def create(file):
    """
    This function creates a new person in the people structure
    based on the passed in person data
    :param person:  person to create in people structure
    :return:        201 on success, 406 on person exists
    """
    arquivo = file.get("name", None)

    # Does the person exist already?
    if name not in FILE and name is not None:
      try:
        f = request.files['file']
        f.save(secure_filename(f.filename))
        FILE[name] = {
            "name": name,
            "timestamp": get_timestamp(),
        }
        return make_response(
            "{name} file uploaded com sucesso".format(name=name), 201
        )

    # Otherwise, they exist, that's an error
    else:
        abort(
            406,
            "Arquivo {name} já existe".format(name=name),
        )


def delete(name):
    """
    This function deletes a person from the people structure
    :param lname:   last name of person to delete
    :return:        200 on successful delete, 404 if not found
    """
    # Does the person to delete exist?
    if name in FILES:
        del FILES[name]
        return make_response(
            "{name} successfully deleted".format(name=name), 200
        )

    # Otherwise, nope, person to delete not found
    else:
        abort(
            404, "Arquivo {name} não encontrado".format(name=name)
        )
