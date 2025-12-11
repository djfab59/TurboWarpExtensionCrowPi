from flask import Blueprint, jsonify, request

from bridge.modules.ledmatrix_mod import ledmatrix
from bridge.shared.locks import ledmatrix_lock


ledmatrix_bp = Blueprint("ledmatrix", __name__, url_prefix="/ledmatrix")


@ledmatrix_bp.route("/clear", methods=["POST", "OPTIONS"])
def clear():
    if request.method == "OPTIONS":
        return "", 204

    with ledmatrix_lock:
        ledmatrix.clear()

    return jsonify(ok=True)


@ledmatrix_bp.route("/pixel/color", methods=["POST", "OPTIONS"])
def pixel_color():
    if request.method == "OPTIONS":
        return "", 204

    data = request.get_json(silent=True) or {}
    x = data.get("x", 1)
    y = data.get("y", 1)
    color = data.get("color", "blanc")

    with ledmatrix_lock:
        ledmatrix.set_pixel_named(x, y, color)

    return jsonify(ok=True)


@ledmatrix_bp.route("/pixel/rgb", methods=["POST", "OPTIONS"])
def pixel_rgb():
    if request.method == "OPTIONS":
        return "", 204

    data = request.get_json(silent=True) or {}
    x = data.get("x", 1)
    y = data.get("y", 1)
    r = data.get("r", 255)
    g = data.get("g", 255)
    b = data.get("b", 255)

    with ledmatrix_lock:
        ledmatrix.set_pixel_rgb(x, y, r, g, b)

    return jsonify(ok=True)


@ledmatrix_bp.route("/pixel/off", methods=["POST", "OPTIONS"])
def pixel_off():
    if request.method == "OPTIONS":
        return "", 204

    data = request.get_json(silent=True) or {}
    x = data.get("x", 1)
    y = data.get("y", 1)

    with ledmatrix_lock:
        ledmatrix.clear_pixel(x, y)

    return jsonify(ok=True)


@ledmatrix_bp.route("/fill/color", methods=["POST", "OPTIONS"])
def fill_color():
    if request.method == "OPTIONS":
        return "", 204

    data = request.get_json(silent=True) or {}
    color = data.get("color", "blanc")

    with ledmatrix_lock:
        ledmatrix.fill_named(color)

    return jsonify(ok=True)


@ledmatrix_bp.route("/animation", methods=["POST", "OPTIONS"])
def animation():
    if request.method == "OPTIONS":
        return "", 204

    data = request.get_json(silent=True) or {}
    name = data.get("name", "")
    color = data.get("color")

    with ledmatrix_lock:
        ledmatrix.play_animation(name, color_name=color)

    return jsonify(ok=True)
