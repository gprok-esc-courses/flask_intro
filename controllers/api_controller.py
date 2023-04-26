from flask import Blueprint, jsonify
from db import get_connection
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

api = Blueprint('api', __name__)

@api.route('/api/users/programs')
def api_users_program():
    db = get_connection()
    cursor = db.cursor()
    result = cursor.execute("""SELECT u.id, u.username, p.title
                            FROM users u
                            INNER JOIN programs p ON u.program_id=p.id""")
    return jsonify(result.fetchall())


@api.route('/api/token')
def token():
    access_token = create_access_token(identity='johndoe')
    return jsonify({'token': access_token})


@api.route('/api/protected')
@jwt_required()
def protected_request():
    current_user = get_jwt_identity()
    return jsonify({'user': current_user, 'data': 'protected data'})
