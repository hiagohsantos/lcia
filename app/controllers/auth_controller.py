from flask import Blueprint, Response, json, request, jsonify
from app.middleware.authentication import require_auth
from app.services.organization_service import AuthService
from app.models.organization import Organization

bp = Blueprint('auth', __name__)

@bp.route('/auth/verify-key', methods=['GET'])
@require_auth
def auth(organization: Organization):
    response =  {
        'message': 'Sucesso, sua API-Key está válida!',
        'organization_name': organization.name
    }
    return Response(json.dumps(response, ensure_ascii=False), mimetype='application/json')