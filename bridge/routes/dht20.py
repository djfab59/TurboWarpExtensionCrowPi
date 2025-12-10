from flask import Blueprint, jsonify
from bridge.modules.dht20_mod import dht20
from bridge.shared.locks import dht_lock

dht20_bp = Blueprint("dht20", __name__, url_prefix="/dht20")

@dht20_bp.route("/read", methods=["GET"])
def read():
    with dht_lock:
        temp, hum = dht20.read()

    return jsonify(
        temperature=temp,
        humidity=hum
    )