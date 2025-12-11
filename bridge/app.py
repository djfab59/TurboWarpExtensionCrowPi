from flask import Flask
from bridge.routes.lcd import lcd_bp
from bridge.routes.dht20 import dht20_bp

app = Flask(__name__)


@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response


# Enregistrement des blueprints
app.register_blueprint(lcd_bp)
app.register_blueprint(dht20_bp)
