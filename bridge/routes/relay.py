from flask import Blueprint, jsonify, request

from bridge.modules.relay_mod import relay
from bridge.shared.locks import relay_lock


relay_bp = Blueprint("relay", __name__, url_prefix="/relay")


@relay_bp.route("/on", methods=["POST", "OPTIONS"])
def relay_on():
    if request.method == "OPTIONS":
        return "", 204

    with relay_lock:
        relay.on()

    return jsonify(ok=True)


@relay_bp.route("/off", methods=["POST", "OPTIONS"])
def relay_off():
    if request.method == "OPTIONS":
        return "", 204

    with relay_lock:
        relay.off()

    return jsonify(ok=True)


@relay_bp.route("/pulse", methods=["POST", "OPTIONS"])
def relay_pulse():
    if request.method == "OPTIONS":
        return "", 204

    data = request.get_json(silent=True) or {}
    duration = data.get("duration", 500)
    try:
        duration = int(duration)
    except (TypeError, ValueError):
        duration = 500

    with relay_lock:
        relay.pulse(duration)

    return jsonify(ok=True)

