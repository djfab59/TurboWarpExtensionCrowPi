#!/usr/bin/env python3

from flask import Flask, request, jsonify
from OLD.crowpi_lcd import LCDModule
import time
import threading

lcd_lock = threading.Lock()
lcd = LCDModule()
scroll_thread = None
scroll_stop_event = threading.Event()

app = Flask(__name__)

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

@app.route("/lcd/on", methods=["POST", "OPTIONS"])
def lcd_on():
    if request.method == "OPTIONS":
        return '', 204
    with lcd_lock:
        lcd.on()
        time.sleep(0.05)
    return jsonify(ok=True)

@app.route("/lcd/off", methods=["POST", "OPTIONS"])
def lcd_off():
    if request.method == "OPTIONS":
        return '', 204
    with lcd_lock:
        lcd.off()
        time.sleep(0.05)
    lcd.off()
    return jsonify(ok=True)

@app.route("/lcd/clear", methods=["POST", "OPTIONS"])
def lcd_clear():
    if request.method == "OPTIONS":
        return '', 204
    with lcd_lock:
        lcd.clear()
        time.sleep(0.05)
    return jsonify(ok=True)

@app.route("/lcd/write", methods=["POST", "OPTIONS"])
def lcd_write():
    if request.method == "OPTIONS":
        return '', 204
    text = request.json.get("text", "")
    with lcd_lock:
        lcd.write(text)
        time.sleep(0.05)
    return jsonify(ok=True)

@app.route("/lcd/line", methods=["POST", "OPTIONS"])
def lcd_line():
    if request.method == "OPTIONS":
        return '', 204
    data = request.get_json(silent=True) or {}
    line = int(data.get("line", 1))
    text = data.get("text", "")
    with lcd_lock:
        lcd.write_line(line, text)
        time.sleep(0.05)
    return jsonify(ok=True)

@app.route("/lcd/both", methods=["POST", "OPTIONS"])
def lcd_both():
    if request.method == "OPTIONS":
        return '', 204
    data = request.get_json(silent=True) or {}
    line1 = data.get("line1", "")
    line2 = data.get("line2", "")
    with lcd_lock:
        lcd.write_both(line1, line2)
        time.sleep(0.05)
    return jsonify(ok=True)

@app.route("/lcd/scroll/start", methods=["POST", "OPTIONS"])
def lcd_scroll_start():
    global scroll_thread
    if request.method == "OPTIONS":
        return '', 204
    data = request.get_json(silent=True) or {}
    text = data.get("text", "")
    line = int(data.get("line", 1))
    speed = int(data.get("speed", 200))  # ms
    # Arrêter un éventuel scroll existant
    scroll_stop_event.set()
    time.sleep(0.05)
    scroll_stop_event.clear()
    scroll_thread = threading.Thread(
        target=lcd.scroll_text,
        args=(line, text, speed, scroll_stop_event),
        daemon=True
    )
    scroll_thread.start()
    return jsonify(ok=True)

@app.route("/lcd/scroll/stop", methods=["POST", "OPTIONS"])
def lcd_scroll_stop():
    if request.method == "OPTIONS":
        return '', 204
    scroll_stop_event.set()
    return jsonify(ok=True)

app.run(host="127.0.0.1", port=3232)

