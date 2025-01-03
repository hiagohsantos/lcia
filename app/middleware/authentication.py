from flask import request, jsonify
from functools import wraps
from app.models.apikey import ApiKey
from app.repositories.base_repository import BaseRepository
from app.services.auth_service import AuthService

def require_auth(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        try: 
            api_key = request.headers.get('x-api-key') 

            if not api_key:
                return jsonify({'message': 'API key é necessária!'}), 401
            
            service = AuthService()
            hash = service.hash_api_key(api_key)
            repository = BaseRepository(ApiKey)

            saved_apikey = repository.get(hash=hash)

            if not saved_apikey:
                return jsonify({'message': 'API key inválida!'}), 403
            
            kwargs['organization'] = saved_apikey.organization
            return f(*args, **kwargs)
        
        except Exception as ex:
            print(f"Falha ao autenticar {ex}")
        
    return decorator
