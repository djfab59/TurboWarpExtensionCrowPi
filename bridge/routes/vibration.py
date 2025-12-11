from flask import Blueprint, jsonify, request

from bridge.modules.vibration_mod import vibration
from bridge.shared.locks import vibration_lock


vibration_bp = Blueprint("vibration", __name__, url_prefix="/vibration")


@vibration_bp.route("/on", methods=["POST", "OPTIONS"])
def vibration_on():
    if request.method == "OPTIONS":
        return "", 204

    with vibration_lock:
        vibration.on()

    return jsonify(ok=True)


@vibration_bp.route("/off", methods=["POST", "OPTIONS"])
def vibration_off():
    if request.method == "OPTIONS":
        return "", 204

    with vibration_lock:
        vibration.off()

    return jsonify(ok=True)


@vibration_bp.route("/pulse", methods=["POST", "OPTIONS"])
def vibration_pulse():
    if request.method == "OPTIONS":
        return "", 204

    data = request.get_json(silent=True) or {}
    duration = data.get("duration", 500)
    try:
        duration = int(duration)
    except (TypeError, ValueError):
        duration = 500

    with vibration_lock:
        vibration.pulse(duration)

    return jsonify(ok=True)

