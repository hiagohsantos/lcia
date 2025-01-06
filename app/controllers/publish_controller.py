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
        return jsonify(process_data), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    
    except Exception as e:
        return jsonify({'error': 'Erro interno do servidor'}), 500



@bp.route('/publish/upload', methods=['POST'])
@require_auth
def upload_file(organization) -> Response:
    try:
        # Verifica se o arquivo foi enviado
        if 'file' not in request.files:
            return jsonify({'error': 'Nenhum arquivo foi enviado'}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'Arquivo não selecionado'}), 400

        # Usa o caminho definido no config
        upload_folder = current_app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)

        file_instance = PublishService().create_file(file)

        if not file_instance:
            raise Exception('Houve um problema ao salvar os dados do arquivo.')

        new_filename = f"{file_instance.id}.{file_instance.file_extension}" 
        file_path = os.path.join(upload_folder, new_filename)
        file.seek(0)
        file.save(file_path)

        return jsonify({'message': 'Arquivo enviado com sucesso', 'file_id':file_instance.id}), 201

    except Exception as e:
        return jsonify({'error': 'Erro ao processar o arquivo', 'details': str(e)} ), 500
    

@bp.route('/publish/file/<file_id>', methods=['GET'])
@require_auth
def get_file(file_id, organization):
    try:
        # Verifica se o arquivo existe
        file_instance = PublishService().get_file_by_id(file_id)

        if not file_instance:
            return jsonify({'error': 'Arquivo não encontrado'}), 404

        # Usa o caminho definido no config para o diretório de upload
        upload_folder = current_app.config['UPLOAD_FOLDER']

        # Gera o caminho completo para o arquivo com base no ID e extensão
        file_path = os.path.join(upload_folder, f"{file_instance.id}.{file_instance.file_extension}")

        # Verifica se o arquivo realmente existe no diretório
        if not os.path.isfile(file_path):
            return jsonify({'error': 'Arquivo não encontrado no servidor'}), 404

        # Retorna o arquivo
        return send_from_directory(
            directory=upload_folder,
            path=f"{file_instance.id}.{file_instance.file_extension}",
            as_attachment=True,
            download_name=f"{file_instance.filename}.{file_instance.file_extension}" 
            )

    except Exception as e:
        return jsonify({'error': 'Erro ao processar a solicitação', 'details': str(e)}), 500