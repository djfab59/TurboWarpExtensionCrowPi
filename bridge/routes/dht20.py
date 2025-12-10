from flask import Blueprint, jsonify
from bridge.modules.dht20_mod import dht20
from bridge.shared.locks import dht_lock

dht20_bp = Blueprint("dht20", __name__, url_prefix="/dht20")

@dht20_bp.route("/read", methods=["GET"])
def read():
    with dht_lock:
        temp, hum = dht20.read()

    # Arrondit proprement à 2 décimales si les valeurs sont numériques
    if isinstance(temp, (int, float)):
        temp = round(temp, 2)
    if isinstance(hum, (int, float)):
        hum = round(hum, 2)

    return jsonify(
        temperature=temp,
        humidity=hum
    )
