"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family: FamilyStructure = FamilyStructure("Jackson")

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
        return jsonify(members), 200  
    
    except Exception as e:
        return jsonify({"error": "Ocurrió un error en el servidor.", "detalle": str(e)}), 500


@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    try:
        member = jackson_family.get_member(member_id)
        if member is None:

            return jsonify({"mensaje": "Miembro no encontrado."}), 404
        
        return jsonify({
            "first_name": member["first_name"],
            "id": member["id"],
            "age": member["age"],
            "lucky_numbers": member["lucky_numbers"]
        }), 200
    
    except Exception as e:
        return jsonify({"error": "Ocurrió un error en el servidor.", "detalle": str(e)}), 500


@app.route('/member', methods=['POST'])
def add_member():
    try:
        request_body = request.json
        if not all(key in request_body for key in ("first_name", "age", "lucky_numbers")):

            return jsonify({"mensaje": "Faltan campos requeridos."}), 400
        
        if request_body["age"] < 0:

            return jsonify({"mensaje": "La edad debe ser un número mayor igual que 0."}), 400
        
        new_member = jackson_family.add_member(request_body) 
         
        return jsonify(new_member), 200 

    except Exception as e:
        return jsonify({"error": "Ocurrió un error en el servidor.", "detalle": str(e)}), 50


@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    try:
        result = jackson_family.delete_member(member_id)
        if not result:

            return jsonify({"mensaje": "Miembro no encontrado."}), 404
        
        return jsonify({"done": True}), 200
    
    except Exception as e:
        return jsonify({"error": "Ocurrió un error en el servidor.", "detalle": str(e)}), 500


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
