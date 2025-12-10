from flask import Blueprint, jsonify
from bridge.modules.dht11_mod import dht11
from bridge.shared.locks import dht_lock

dht11_bp = Blueprint("dht11", __name__, url_prefix="/dht11")

@dht11_bp.route("/read", methods=["GET"])
def read():
    with dht_lock:
        temp, hum = dht11.read()

    return jsonify(
        temperature=temp,
        humidity=hum
    )