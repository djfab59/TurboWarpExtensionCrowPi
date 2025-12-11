import asyncio
import json

import websockets

from bridge.modules.buttonmatrix_mod import button_matrix
from bridge.shared.locks import matrix_lock


async def _handle_client(websocket):
    """
    Pour chaque client connecté :
    - boucle en lisant la matrice
    - envoie un message JSON à chaque événement détecté
      (appui ou relâche d'un bouton)
    """
    try:
        while True:
            # Fréquence de scan raisonnable pour ne pas saturer le CPU
            await asyncio.sleep(0.02)

            with matrix_lock:
                raw, mapped, state = button_matrix.step()

            # step() ne renvoie un état valide que sur front montant/descendant
            if state:
                message = json.dumps({
                    "raw": raw,
                    "mapped": mapped,
                    "state": state
                })
                try:
                    await websocket.send(message)
                except websockets.ConnectionClosed:
                    # Le client s'est déconnecté, on termine le handler
                    break
    except Exception as exc:
        # Log minimal pour faciliter le debug en cas de problème
        print("[WebSocket] Client handler error:", exc)


async def run_websocket_server(host: str = "127.0.0.1", port: int = 3233):
    """
    Lance le serveur WebSocket.
    Actuellement utilisé pour la matrice de boutons, mais peut être étendu
    à d'autres événements si besoin.
    """
    async with websockets.serve(_handle_client, host, port):
        # Tâche infinie pour garder le serveur vivant
        await asyncio.Future()
