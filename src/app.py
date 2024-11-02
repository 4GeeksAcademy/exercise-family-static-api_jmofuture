"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family: FamilyStructure = FamilyStructure("Jackson")

jackson_family.add_member({"first_name": "Jean", "age": 25, "lucky_numbers": [7, 14, 21]})
jackson_family.add_member({"first_name": "Lucia", "age": 30, "lucky_numbers": [3, 5, 9]})
jackson_family.add_member({"first_name": "Agustin", "age": 30, "lucky_numbers": [3, 5, 9]})


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def handle_members():
    try:
        members = jackson_family.get_all_members()

        if not members:
            return jsonify({"mensaje": "No hay miembros en la familia."}), 404

        response_body = {
            "family": members,
        }

        return jsonify(response_body), 200

    except Exception as e:
        return jsonify({"error": "Ocurrió un error en el servidor.", "details": str(e)}), 500


@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    try:
        member = jackson_family.get_member_by_id(member_id)

        if member is None:
            return jsonify({"mensaje": "Miembro no encontrado."}), 404

        return jsonify(member), 200

    except Exception as e:
        return jsonify({"error": "Ocurrió un error en el servidor.", "details": str(e)}), 500


@app.route('/member', methods=['POST'])
def add_member():
    try:
        request_body = request.json

        if not all(key in request_body for key in ("id", "first_name", "age", "lucky_numbers")):
            return jsonify({"mensaje": "Faltan campos requeridos."}), 400
        
        if request_body["age"] <= 0:
            return jsonify({"mensaje": "La edad debe ser un número mayor que 0."}), 404
        
        jackson_family.add_member(request_body)

        return jsonify(request_body), 200

    except Exception as e:
        return jsonify({"error": "Ocurrió un error en el servidor.", "details": str(e)}), 500


@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    try:
        member_deleted = jackson_family.delete_member(member_id)

        if member_deleted:
            return jsonify({"done": True}), 200
        else:
            return jsonify({"message": "Miembro no encontrado."}), 404

    except Exception as e:
        return jsonify({"error": "Ocurrió un error en el servidor.", "details": str(e)}), 500


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
