# crowpi_bridge.py
from flask import Flask, request, jsonify
from crowpi_lcd import LCDModule

lcd = LCDModule()
app = Flask(__name__)

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

@app.route("/lcd/write", methods=["POST"])
def lcd_write():
    text = request.json.get("text", "")
    lcd.write(text)
    return jsonify(ok=True)

@app.route("/lcd/clear", methods=["POST"])
def lcd_clear():
    lcd.clear()
    return jsonify(ok=True)

@app.route("/lcd/on", methods=["POST"])
def lcd_on():
    lcd.on()
    return jsonify(ok=True)

@app.route("/lcd/off", methods=["POST"])
def lcd_off():
    lcd.off()
    return jsonify(ok=True)

app.run(host="127.0.0.1", port=3232)

