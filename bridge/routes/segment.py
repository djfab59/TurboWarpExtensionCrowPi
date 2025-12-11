from flask import Blueprint, jsonify, request

from bridge.modules.segment_mod import segment_display
from bridge.shared.locks import segment_lock


segment_bp = Blueprint("segment", __name__, url_prefix="/segment")


@segment_bp.route("/init", methods=["POST", "OPTIONS"])
def init():
    if request.method == "OPTIONS":
        return "", 204

    with segment_lock:
        segment_display.init()

    return jsonify(ok=True)


@segment_bp.route("/display/number", methods=["POST", "OPTIONS"])
def display_number():
    if request.method == "OPTIONS":
        return "", 204

    data = request.get_json(silent=True) or {}
    value = data.get("value", 0)

    with segment_lock:
        segment_display.display_number(value)

    return jsonify(ok=True)


@segment_bp.route("/digit", methods=["POST", "OPTIONS"])
def digit():
    if request.method == "OPTIONS":
        return "", 204

    data = request.get_json(silent=True) or {}
    position = data.get("position", 1)
    value = data.get("value", 0)

    with segment_lock:
        segment_display.set_digit(position, value)

    return jsonify(ok=True)


@segment_bp.route("/decimal/on", methods=["POST", "OPTIONS"])
def decimal_on():
    if request.method == "OPTIONS":
        return "", 204

    data = request.get_json(silent=True) or {}
    position = data.get("position", 1)

    with segment_lock:
        segment_display.set_decimal_point(position, True)

    return jsonify(ok=True)


@segment_bp.route("/decimal/off", methods=["POST", "OPTIONS"])
def decimal_off():
    if request.method == "OPTIONS":
        return "", 204

    data = request.get_json(silent=True) or {}
    position = data.get("position", 1)

    with segment_lock:
        segment_display.set_decimal_point(position, False)

    return jsonify(ok=True)


@segment_bp.route("/colon/on", methods=["POST", "OPTIONS"])
def colon_on():
    if request.method == "OPTIONS":
        return "", 204

    with segment_lock:
        segment_display.set_colon(True)

    return jsonify(ok=True)


@segment_bp.route("/colon/off", methods=["POST", "OPTIONS"])
def colon_off():
    if request.method == "OPTIONS":
        return "", 204

    with segment_lock:
        segment_display.set_colon(False)

    return jsonify(ok=True)


@segment_bp.route("/digit/raw", methods=["POST", "OPTIONS"])
def digit_raw():
    if request.method == "OPTIONS":
        return "", 204

    data = request.get_json(silent=True) or {}
    position = data.get("position", 1)
    bitmask = data.get("bitmask", 0)

    with segment_lock:
        segment_display.set_digit_raw(position, bitmask)

    return jsonify(ok=True)


@segment_bp.route("/clear", methods=["POST", "OPTIONS"])
def clear():
    if request.method == "OPTIONS":
        return "", 204

    with segment_lock:
        segment_display.clear()

    return jsonify(ok=True)


@segment_bp.route("/brightness", methods=["POST", "OPTIONS"])
def brightness():
    if request.method == "OPTIONS":
        return "", 204

    data = request.get_json(silent=True) or {}
    level = data.get("level", 15)

    with segment_lock:
        segment_display.set_brightness(level)

    return jsonify(ok=True)

