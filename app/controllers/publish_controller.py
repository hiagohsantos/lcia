import json
from flask import Blueprint, Response, jsonify, request, current_app, send_from_directory
from app.models.organization import Organization
from app.repositories.LC_repository import LCRepository
from app.services.publish_service import PublishService
from app.middleware.authentication import require_auth
import os

bp = Blueprint('publish', __name__)

@bp.route('/publish/<int:publish_id>', methods=['GET'])
@require_auth
def publish(publish_id, organization: Organization)-> Response:
    try:
        process_data = PublishService(organization).get_publish_by_id(publish_id)
        return  Response(json.dumps(process_data, ensure_ascii=False), mimetype='application/json')
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    
    except Exception as e:
        return jsonify({'error': 'Erro interno do servidor'}), 500

