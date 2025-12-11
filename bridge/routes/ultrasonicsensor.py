from flask import Blueprint, jsonify

from bridge.modules.ultrasonicsensor_mod import ultrasonicsensor
from bridge.shared.locks import ultrasonicsensor_lock


ultrasonicsensor_bp = Blueprint(
    "ultrasonicsensor",
    __name__,
    url_prefix="/ultrasonicsensor"
)


@ultrasonicsensor_bp.route("/read", methods=["GET"])
def read():
    with ultrasonicsensor_lock:
        dist = ultrasonicsensor.read()

    if isinstance(dist, (int, float)):
        dist = round(dist, 2)
    else:
        dist = None

    return jsonify(distance=dist)

