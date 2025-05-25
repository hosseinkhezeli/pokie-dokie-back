from flask import request, jsonify
from . import bp
from ..utils import token_required
from ..services.session_service import create_session, get_sessions_for_user

@bp.route('/sessions', methods=['POST'])
@token_required
def create():
    """
       Create a new session
       ---
       tags:
         - sessions
       security:
         - Bearer: []
       parameters:
         - name: Authorization
           in: header
           type: string
           required: true
           description: JWT token
         - in: body
           name: body
           required: true
           schema:
             type: object
             properties:
               session_name:
                 type: string
               duration:
                 type: integer
               notes:
                 type: string
             example:
               session_name: "Morning Workout"
               duration: 60
               notes: "Completed all sets"
       responses:
         201:
           description: Session created successfully
           schema:
             type: object
             properties:
               id:
                 type: string
               session_name:
                 type: string
               user_id:
                 type: string
               created_at:
                 type: string
                 format: date-time
         400:
           description: Invalid input data
         401:
           description: Unauthorized
       """
    current_user = request.current_user
    data = request.get_json()
    session, status = create_session(current_user, data)
    return jsonify(session), status

@bp.route('/sessions', methods=['GET'])
@token_required
def list_sessions():
    """
        Get all user sessions
        ---
        tags:
          - sessions
        security:
          - Bearer: []
        parameters:
          - name: Authorization
            in: header
            type: string
            required: true
            description: JWT token
        responses:
          200:
            description: List of user sessions
            schema:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: string
                  session_name:
                    type: string
                  duration:
                    type: integer
                  created_at:
                    type: string
                    format: date-time
          401:
            description: Unauthorized
        """
    current_user = request.current_user
    sessions = get_sessions_for_user(current_user)
    return jsonify(sessions)