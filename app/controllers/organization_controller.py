from flask import Blueprint, request, jsonify
from app.middleware.authentication import require_auth
from app.models.input_models.organization_input import OrganizationInputModel
from app.models.organization import Organization
from app.services.organization_service import  OrganizationService

bp = Blueprint('organization', __name__)


@bp.route('/organization/create', methods=['POST'])
@require_auth
def create_organization(organization: Organization):
    try: 
        if organization.name != "ADM":
            return jsonify({"error": "Apenas a conta ADM pode criar novas organizações."}), 401 
        try:
            data = OrganizationInputModel.model_validate(request.get_json())  
        except Exception as e:
            return jsonify({"error": str(e)}), 400 

        service = OrganizationService()
        organization, api_key = service.create_organization_and_api_key(data)

        return jsonify({
            "organization_id": organization.id,
            "organization_name": organization.name,
            "api_key": api_key
        }), 201
    
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500
