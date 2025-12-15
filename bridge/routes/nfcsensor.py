from flask import Blueprint, jsonify, request

from bridge.modules.nfcsensor_mod import nfcsensor
from bridge.shared.locks import nfcsensor_lock


nfcsensor_bp = Blueprint("nfcsensor", __name__, url_prefix="/nfcsensor")


@nfcsensor_bp.route("/read_text", methods=["GET"])
def read_text():
    """
    Lecture du texte stocké sur la carte NFC.
    Utilise l'API SimpleMFRC522.read() qui bloque jusqu'à la présence d'une carte.
    """
    with nfcsensor_lock:
        reader = getattr(nfcsensor, "reader", None)
        if reader is None:
            return jsonify(ok=False, error="nfc_unavailable"), 500

        try:
            card_id, text = reader.read()
        except Exception as exc:
            return jsonify(ok=False, error=str(exc)), 500

    return jsonify(ok=True, id=card_id, text=text)


@nfcsensor_bp.route("/write_text", methods=["POST", "OPTIONS"])
def write_text():
    """
    Écrit un texte sur la carte NFC.
    Utilise l'API SimpleMFRC522.write(text), qui bloque jusqu'à la présence d'une carte.
    """
    if request.method == "OPTIONS":
        return "", 204

    data = request.get_json(silent=True) or {}
    text = str(data.get("text", ""))

    with nfcsensor_lock:
        reader = getattr(nfcsensor, "reader", None)
        if reader is None:
            return jsonify(ok=False, error="nfc_unavailable"), 500

        try:
            reader.write(text)
        except Exception as exc:
            return jsonify(ok=False, error=str(exc)), 500

    return jsonify(ok=True)

