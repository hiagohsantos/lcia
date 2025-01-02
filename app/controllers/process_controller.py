from flask import Blueprint, request, jsonify
from app.services.process_service import ProcessService

process_bp = Blueprint('process', __name__)

@process_bp.route('/process/<int:process_id>', methods=['GET'])
def get_process_by_id(process_id):
    """
    Busca detalhes de um processo ou sentença pelo ID.
    """
    try:
        # Chama o serviço para buscar os detalhes
        process_data = ProcessService.get_process_by_id(process_id)
        return jsonify(process_data), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Erro interno do servidor'}), 500
