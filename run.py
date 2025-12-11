#!/usr/bin/env python3

import asyncio
import threading

from bridge.app import app
from bridge.websocket import run_websocket_server


def _start_websocket():
    """
    Lance le serveur WebSocket dans un thread séparé.
    Actuellement utilisé pour buttonmatrix, mais pourra servir à d'autres
    événements par la suite.
    """
    asyncio.run(run_websocket_server(host="127.0.0.1", port=3233))


if __name__ == "__main__":
    # Démarrage du serveur WebSocket (événementiel)
    ws_thread = threading.Thread(target=_start_websocket, daemon=True)
    ws_thread.start()

    # Démarrage du serveur HTTP Flask existant (lcd, dht20, etc.)
    app.run(host="127.0.0.1", port=3232)
