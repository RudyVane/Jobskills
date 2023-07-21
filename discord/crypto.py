from functools import wraps

from flask import current_app, jsonify, make_response, request
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError


def signed_by_discord(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        signature = None
        timestamp = None
        if 'X-Signature-Ed25519' in request.headers and 'X-Signature-Timestamp' in request.headers:
            signature = request.headers['X-Signature-Ed25519']
            timestamp = request.headers['X-Signature-Timestamp']
        if not signature:
            return make_response(jsonify({
                "message": "A valid signature is missing"
            }), 401)
        
        verify_key = VerifyKey(bytes.fromhex(current_app.config['DISCORD_PUBLIC_KEY']))
        try:
            verify_key.verify(timestamp.encode() + request.data, bytes.fromhex(signature))
        except BadSignatureError:
            return make_response(jsonify({
                "message": "invalid request signature"
            }), 401)
        
        
        return current_app.ensure_sync(f)(*args, **kwargs)

    return decorator