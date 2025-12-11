from flask import Blueprint, jsonify

from bridge.modules.lightsensor_mod import lightsensor
from bridge.shared.locks import lightsensor_lock


lightsensor_bp = Blueprint("lightsensor", __name__, url_prefix="/lightsensor")


@lightsensor_bp.route("/read", methods=["GET"])
def read():
    with lightsensor_lock:
        lux = lightsensor.read()

    if isinstance(lux, (int, float)):
        lux = round(lux, 2)
    else:
        lux = None

    return jsonify(lux=lux)

