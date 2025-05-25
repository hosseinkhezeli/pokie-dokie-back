from flask import request, jsonify
from . import bp
from ..services.auth_service import signup_user, login_user

@bp.route('/signup', methods=['POST'])
def signup():
    """
      User registration
      ---
      tags:
        - auth
      parameters:
        - in: body
          name: body
          required: true
          schema:
            type: object
            properties:
              username:
                type: string
              email:
                type: string
              password:
                type: string
      responses:
        201:
          description: User created successfully
        400:
          description: Invalid input
      """
    data = request.get_json()
    resp, status = signup_user(data)
    return jsonify(resp), status

@bp.route('/login', methods=['POST'])
def login():
    """
        User login
        ---
        tags:
          - auth
        parameters:
          - in: body
            name: body
            required: true
            schema:
              type: object
              properties:
                email:
                  type: string
                password:
                  type: string
        responses:
          200:
            description: Login successful
          401:
            description: Invalid credentials
        """
    data = request.get_json()
    resp, status = login_user(data)
    return jsonify(resp), status