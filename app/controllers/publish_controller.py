from flask import Blueprint, jsonify
from app.services.publish_service import ProcessService

bp = Blueprint('publish', __name__)

@bp.route('/publish/<int:publish_id>', methods=['GET'])
def get_process_by_id(publish_id):
    try:
        process_data = ProcessService.get_process_by_id(publish_id)
        return jsonify(process_data), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    
    except Exception as e:
        return jsonify({'error': 'Erro interno do servidor'}), 500
