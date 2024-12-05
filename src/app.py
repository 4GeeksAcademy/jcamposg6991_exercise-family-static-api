import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)


jackson_family = FamilyStructure("Jackson")


john = {"first_name": "John", "age": 33, "lucky_numbers": [7, 13, 22]}
jane = {"first_name": "Jane", "age": 35, "lucky_numbers": [10, 14, 3]}
jimmy = {"first_name": "Jimmy", "age": 5, "lucky_numbers": [1]}

jackson_family.add_member(john)
jackson_family.add_member(jane)
jackson_family.add_member(jimmy)


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def get_all_members():
    members = jackson_family.get_all_members()
    return jsonify(members), 200


@app.route('/member/<int:id>', methods=['GET'])
def get_single_member(id):
    member = jackson_family.get_member(id)
    if member:
        return jsonify(member), 200
    return jsonify({"error": "Member not found"}), 404


@app.route('/member', methods=['POST'])
def create_member():
    new_member = request.json
    if not new_member:
        return jsonify({"error": "Invalid data"}), 400
    member = jackson_family.add_member(new_member)
    return jsonify(member), 200


@app.route('/member/<int:id>', methods=['DELETE'])
def delete_single_member(id):
    result = jackson_family.delete_member(id)
    if result["done"]:
        return jsonify({"done": True}), 200
    return jsonify({"error": "Member not found"}), 404


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
