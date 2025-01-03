from flask import request, jsonify
from functools import wraps
from app.models.apikey import  ApiKey

def require_auth(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        try: 
            api_key = request.headers.get('x-api-key') 
            if not api_key:
                return jsonify({'message': 'API key é necessária!'}), 401
            
            hash = ApiKey.hash_api_key(api_key)

            apikey = ApiKey.query.filter_by(hash=hash).first()

            if not apikey:
                return jsonify({'message': 'API key inválida!'}), 403
            
            kwargs['organization'] = apikey.organization
            return f(*args, **kwargs)
        
        except Exception as e:
            print("Falha", e)
        
    return decorator
