from flask import Blueprint, jsonify, request

from bridge.modules.buzzer_mod import buzzer
from bridge.shared.locks import buzzer_lock


buzzer_bp = Blueprint("buzzer", __name__, url_prefix="/buzzer")


@buzzer_bp.route("/on", methods=["POST", "OPTIONS"])
def buzzer_on():
    if request.method == "OPTIONS":
        return "", 204

    data = request.get_json(silent=True) or {}
    freq = data.get("freq", 440)
    try:
        freq = float(freq)
    except (TypeError, ValueError):
        freq = 440

    with buzzer_lock:
        buzzer.on_freq(freq)

    return jsonify(ok=True)


@buzzer_bp.route("/off", methods=["POST", "OPTIONS"])
def buzzer_off():
    if request.method == "OPTIONS":
        return "", 204

    with buzzer_lock:
        buzzer.off()

    return jsonify(ok=True)


@buzzer_bp.route("/note", methods=["POST", "OPTIONS"])
def buzzer_note():
    if request.method == "OPTIONS":
        return "", 204

    data = request.get_json(silent=True) or {}
    note = data.get("note", "C4")
    duration = data.get("duration", 500)
    try:
        duration = int(duration)
    except (TypeError, ValueError):
        duration = 500

    with buzzer_lock:
        buzzer.play_note(note, duration)

    return jsonify(ok=True)


@buzzer_bp.route("/melody", methods=["POST", "OPTIONS"])
def buzzer_melody():
    if request.method == "OPTIONS":
        return "", 204

    data = request.get_json(silent=True) or {}
    name = data.get("name", "")
    name = str(name).lower()

    with buzzer_lock:
        buzzer.play_melody(name)

    return jsonify(ok=True)

