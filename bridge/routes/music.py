from flask import Blueprint, jsonify, request

from bridge.modules.music_mod import music_manager
from bridge.shared.locks import music_lock


music_bp = Blueprint("music", __name__, url_prefix="/music")


@music_bp.route("/list", methods=["GET"])
def list_music():
    """
    Liste les fichiers sons/musiques disponibles dans ressources/sound.
    """
    with music_lock:
        data = music_manager.list_files()
    return jsonify(ok=True, **data)


@music_bp.route("/play_music", methods=["POST", "OPTIONS"])
def play_music():
    if request.method == "OPTIONS":
        return "", 204

    data = request.get_json(silent=True) or {}
    name = str(data.get("name", "")).strip()
    if not name:
        return jsonify(ok=False, error="missing_name"), 400

    with music_lock:
        music_manager.play_music(name)

    return jsonify(ok=True)


@music_bp.route("/stop_music", methods=["POST", "OPTIONS"])
def stop_music():
    if request.method == "OPTIONS":
        return "", 204

    with music_lock:
        music_manager.stop_music()

    return jsonify(ok=True)


@music_bp.route("/play_sound", methods=["POST", "OPTIONS"])
def play_sound():
    if request.method == "OPTIONS":
        return "", 204

    data = request.get_json(silent=True) or {}
    name = str(data.get("name", "")).strip()
    if not name:
        return jsonify(ok=False, error="missing_name"), 400

    with music_lock:
        music_manager.play_sound(name)

    return jsonify(ok=True)


@music_bp.route("/play_note", methods=["POST", "OPTIONS"])
def play_note():
    if request.method == "OPTIONS":
        return "", 204

    data = request.get_json(silent=True) or {}
    note = str(data.get("note", "")).strip()
    duration = data.get("duration", 500)

    if not note:
        return jsonify(ok=False, error="missing_note"), 400

    with music_lock:
        music_manager.play_note(note, duration)

    return jsonify(ok=True)

