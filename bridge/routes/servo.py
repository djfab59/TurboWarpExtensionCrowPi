from flask import Blueprint, jsonify, request

from bridge.modules.servo_mod import servo_controller
from bridge.shared.locks import servo_lock


servo_bp = Blueprint("servo", __name__, url_prefix="/servo")


@servo_bp.route("/set_angle", methods=["POST", "OPTIONS"])
def set_angle():
    if request.method == "OPTIONS":
        return "", 204

    data = request.get_json(silent=True) or {}
    servo_id = int(data.get("id", 1))
    angle = data.get("angle", 90)
    try:
        angle = float(angle)
    except (TypeError, ValueError):
        angle = 90.0

    with servo_lock:
        servo_controller.set_angle(servo_id, angle)

    return jsonify(ok=True)


@servo_bp.route("/set_position", methods=["POST", "OPTIONS"])
def set_position():
    if request.method == "OPTIONS":
        return "", 204

    data = request.get_json(silent=True) or {}
    servo_id = int(data.get("id", 1))
    position = str(data.get("position", "center"))

    with servo_lock:
        servo_controller.set_position(servo_id, position)

    return jsonify(ok=True)


@servo_bp.route("/get_angle", methods=["GET"])
def get_angle():
    servo_id = request.args.get("id", "1")
    try:
        servo_id = int(servo_id)
    except (TypeError, ValueError):
        servo_id = 1

    with servo_lock:
        angle = servo_controller.get_angle(servo_id)

    if angle is None:
        return jsonify(ok=False, angle=None)

    return jsonify(ok=True, angle=round(float(angle), 1))

