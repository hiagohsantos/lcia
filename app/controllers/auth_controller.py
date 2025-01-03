from flask import Blueprint, request, jsonify
from app.middleware.authentication import require_auth
from app.services.auth_service import AuthService
from app.models.organization import Organization

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/auth/create-organization', methods=['POST'])
def create_organization():
    # Recebe o nome da empresa
    data = request.get_json()
    empresa_nome = data.get("organization_name")

    if not empresa_nome:
        return jsonify({"error": "Organization name is required"}), 400

    organization, api_key = AuthService.create_organization_and_api_key(empresa_nome)

    return jsonify({
        "organization_id": organization.id,
        "organization_name": organization.name,
        "api_key": api_key
    }), 201


@auth_bp.route('/auth', methods=['GET'])
@require_auth
def auth(organization: Organization):
    return jsonify({
        'message': 'Sucesso, você está autenticado!',
        'organization_name': organization.name
    })