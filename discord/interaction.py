from flask import Blueprint, request, current_app, jsonify

from .crypto import signed_by_discord

discord_interaction = Blueprint('discord_interaction', __name__)

@discord_interaction.route('/', methods=['POST'])
@signed_by_discord
def handle():
    current_app.logger.info("payload: %s", request.json)
    current_app.logger.info("headers: %s", request.headers)

    payload = request.json
    if payload["type"] == 1:
        return jsonify({
            "type": 1
        })
    
    return "NOPE"