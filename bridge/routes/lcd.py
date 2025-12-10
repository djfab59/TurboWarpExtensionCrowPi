from flask import Blueprint, request, jsonify
import time
import threading

from bridge.modules.lcd_mod import LCD
from bridge.shared.locks import lcd_lock

lcd_bp = Blueprint("lcd", __name__, url_prefix="/lcd")
lcd = LCD()

_scroll_thread = None
_scroll_stop = threading.Event()

@lcd_bp.route("/write", methods=["POST", "OPTIONS"])
def write():
    if request.method == "OPTIONS":
        return '', 204

    data = request.get_json(silent=True) or {}
    with lcd_lock:
        lcd.write(data.get("text", ""))
        time.sleep(0.05)
    return jsonify(ok=True)

@lcd_bp.route("/line", methods=["POST", "OPTIONS"])
def line():
    if request.method == "OPTIONS":
        return '', 204

    data = request.get_json(silent=True) or {}
    with lcd_lock:
        lcd.write_line(int(data.get("line", 1)), data.get("text", ""))
        time.sleep(0.05)
    return jsonify(ok=True)

@lcd_bp.route("/both", methods=["POST", "OPTIONS"])
def both():
    if request.method == "OPTIONS":
        return '', 204

    data = request.get_json(silent=True) or {}
    with lcd_lock:
        lcd.write_both(data.get("line1", ""), data.get("line2", ""))
        time.sleep(0.05)
    return jsonify(ok=True)

@lcd_bp.route("/clear", methods=["POST", "OPTIONS"])
def clear():
    if request.method == "OPTIONS":
        return '', 204

    with lcd_lock:
        lcd.clear()
        time.sleep(0.05)
    return jsonify(ok=True)

@lcd_bp.route("/on", methods=["POST", "OPTIONS"])
def on():
    if request.method == "OPTIONS":
        return '', 204

    with lcd_lock:
        lcd.on()
    return jsonify(ok=True)

@lcd_bp.route("/off", methods=["POST", "OPTIONS"])
def off():
    if request.method == "OPTIONS":
        return '', 204

    with lcd_lock:
        lcd.off()
    return jsonify(ok=True)

@lcd_bp.route("/scroll/start", methods=["POST", "OPTIONS"])
def scroll_start():
    global _scroll_thread

    if request.method == "OPTIONS":
        return '', 204

    data = request.get_json(silent=True) or {}
    _scroll_stop.set()
    time.sleep(0.05)
    _scroll_stop.clear()

    _scroll_thread = threading.Thread(
        target=lcd.scroll,
        args=(
            int(data.get("line", 1)),
            data.get("text", ""),
            int(data.get("speed", 200)),
            _scroll_stop
        ),
        daemon=True
    )
    _scroll_thread.start()

    return jsonify(ok=True)

@lcd_bp.route("/scroll/stop", methods=["POST", "OPTIONS"])
def scroll_stop():
    if request.method == "OPTIONS":
        return '', 204

    _scroll_stop.set()
    return jsonify(ok=True)