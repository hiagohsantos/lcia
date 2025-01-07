import json
import os
from flask import Blueprint, Response, current_app, jsonify, request

from app.middleware.authentication import require_auth
from app.services.orders_service import OrdersService


bp = Blueprint('orders', __name__)

@bp.route('orders/extrair_informacoes', methods=['POST'])
@require_auth
def extract_data(organization):
    try:
        # Verifica se o arquivo foi enviado
        if 'file' not in request.files:
            return jsonify({'error': 'Nenhum arquivo foi enviado'}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'Arquivo não selecionado'}), 400

        upload_folder = current_app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)
        service = OrdersService()

        file_instance = service.create_file(file)

        if not file_instance:
            raise Exception('Houve um problema ao salvar os dados do arquivo.')

        new_filename = f"{file_instance.id}.{file_instance.file_extension}" 
        file_path = os.path.join(upload_folder, new_filename)
        file.seek(0)
        file.save(file_path)

        response = service.extract_data(file_path)

        if isinstance(response, str):
            try:
                response = json.loads(response)  
            except json.JSONDecodeError:
                return jsonify({'error': 'Resposta inválida do serviço'}), 500
        
        if isinstance(response, dict):
            return Response(json.dumps(response, ensure_ascii=False), mimetype='application/json')
        else:
            return jsonify({'error': 'Resposta inválida do serviço'}), 500
        
       
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    
    except Exception as e:
        return jsonify({'error': 'Erro interno do servidor'}), 500
    

# @bp.route('/publish/file/<file_id>', methods=['GET'])
# @require_auth
# def get_file(file_id, organization):
#     try:
#         # Verifica se o arquivo existe
#         file_instance = PublishService().get_file_by_id(file_id)

#         if not file_instance:
#             return jsonify({'error': 'Arquivo não encontrado'}), 404

#         # Usa o caminho definido no config para o diretório de upload
#         upload_folder = current_app.config['UPLOAD_FOLDER']

#         # Gera o caminho completo para o arquivo com base no ID e extensão
#         file_path = os.path.join(upload_folder, f"{file_instance.id}.{file_instance.file_extension}")

#         # Verifica se o arquivo realmente existe no diretório
#         if not os.path.isfile(file_path):
#             return jsonify({'error': 'Arquivo não encontrado no servidor'}), 404

#         # Retorna o arquivo
#         return send_from_directory(
#             directory=upload_folder,
#             path=f"{file_instance.id}.{file_instance.file_extension}",
#             as_attachment=True,
#             download_name=f"{file_instance.filename}.{file_instance.file_extension}" 
#             )

#     except Exception as e:
#         return jsonify({'error': 'Erro ao processar a solicitação', 'details': str(e)}), 500