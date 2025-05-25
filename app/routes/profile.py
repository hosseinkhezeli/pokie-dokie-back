from flask import jsonify
from . import bp
from ..utils import token_required
from ..services.user_service import get_user_profile

@bp.route('/profile', methods=['GET'])
@token_required
def profile(current_user):
    """
    Get user profile
    ---
    tags:
      - user
    security:
      - Bearer: []
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
        description: JWT token using the Bearer scheme (Bearer YOUR_TOKEN)
    responses:
      200:
        description: User profile data
        schema:
          $ref: '#/definitions/UserProfile'
      401:
        description: Unauthorized
    """
    profile_data = get_user_profile(current_user)
    return jsonify(profile_data)

