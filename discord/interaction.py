from flask import Blueprint, request, abort, current_app, jsonify
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError

discord_interaction = Blueprint('discord_interaction', __name__)

# FIXME: to config
PUBLIC_KEY = 'ada8547aa7193a4b570c7bed1b13d523a07b5a20139a57753f7715b21c3d9b1f'

verify_key = VerifyKey(bytes.fromhex(PUBLIC_KEY))

@discord_interaction.route('/', methods=['POST'])
def handle():
    signature = request.headers["X-Signature-Ed25519"]
    timestamp = request.headers["X-Signature-Timestamp"]

    try:
        verify_key.verify(timestamp.encode() + request.data, bytes.fromhex(signature))
    except BadSignatureError:
        abort(401, 'invalid request signature')

    current_app.logger.info("payload: %s", request.json)
    current_app.logger.info("headers: %s", request.headers)

    payload = request.json
    if payload["type"] == 1:
        return jsonify({
            "type": 1
        })
    
    return "NOPE"