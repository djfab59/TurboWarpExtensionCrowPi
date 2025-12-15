from flask import Blueprint, jsonify, request

from bridge.modules.stepmotor_mod import stepmotor
from bridge.shared.locks import stepmotor_lock


stepmotor_bp = Blueprint("stepmotor", __name__, url_prefix="/stepmotor")


@stepmotor_bp.route("/turn_degrees", methods=["POST", "OPTIONS"])
def turn_degrees():
    if request.method == "OPTIONS":
        return "", 204

    data = request.get_json(silent=True) or {}
    degrees = data.get("degrees", 0)
    direction = str(data.get("direction", "cw"))
    speed = data.get("speed", 1.0)

    try:
        degrees = float(degrees)
    except (TypeError, ValueError):
        degrees = 0.0

    if direction not in ("cw", "ccw"):
        direction = "cw"

    try:
        speed = float(speed)
    except (TypeError, ValueError):
        speed = 1.0

    with stepmotor_lock:
        stepmotor.turn_degrees(degrees, direction=direction, speed=speed)

    return jsonify(ok=True)


@stepmotor_bp.route("/turn_steps", methods=["POST", "OPTIONS"])
def turn_steps():
    if request.method == "OPTIONS":
        return "", 204

    data = request.get_json(silent=True) or {}
    steps = data.get("steps", 0)
    direction = str(data.get("direction", "cw"))
    speed = data.get("speed", 1.0)

    try:
        steps = int(steps)
    except (TypeError, ValueError):
        steps = 0

    if direction not in ("cw", "ccw"):
        direction = "cw"

    try:
        speed = float(speed)
    except (TypeError, ValueError):
        speed = 1.0

    with stepmotor_lock:
        stepmotor.turn_steps(steps, direction=direction, speed=speed)

    return jsonify(ok=True)


@stepmotor_bp.route("/reset_position", methods=["POST", "OPTIONS"])
def reset_position():
    if request.method == "OPTIONS":
        return "", 204

    with stepmotor_lock:
        stepmotor.reset_position()

    return jsonify(ok=True)


@stepmotor_bp.route("/get_position", methods=["GET"])
def get_position():
    with stepmotor_lock:
        degrees = stepmotor.get_position_degrees()

    return jsonify(ok=True, degrees=round(float(degrees), 1))
