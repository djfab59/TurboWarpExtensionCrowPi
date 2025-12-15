import asyncio
import json

import websockets

from bridge.modules.buttonmatrix_mod import button_matrix
from bridge.modules.touchsensor_mod import touch_sensor
from bridge.modules.joystick_mod import joystick
from bridge.modules.tiltsensor_mod import tilt_sensor
from bridge.modules.soundsensor_mod import sound_sensor
from bridge.modules.irsensor_mod import ir_sensor
from bridge.modules.nfcsensor_mod import nfcsensor
from bridge.shared.locks import (
    matrix_lock,
    touchsensor_lock,
    joystick_lock,
    tiltsensor_lock,
    soundsensor_lock,
    irsensor_lock,
    nfcsensor_lock,
)


async def _handle_client(websocket):
    """
    Pour chaque client connecté :
    - boucle en lisant la matrice
    - lit aussi le capteur tactile, le joystick, le capteur d'inclinaison,
      le capteur de son, le capteur IR et le lecteur NFC
    - envoie un message JSON à chaque événement détecté
      (appui ou relâche d'un bouton, changement d'état du capteur tactile,
       changement d'état du tilt, événement sonore, IR ou NFC)
    """
    # État local pour lisser / limiter les envois joystick
    last_joy_x = None
    last_joy_y = None
    last_joy_sent = 0.0
    joy_threshold = 10  # variation minimale avant envoi
    joy_interval = 0.1  # intervalle minimal entre 2 envois (en secondes)

    try:
        loop = asyncio.get_event_loop()
        while True:
            # Fréquence de scan raisonnable pour ne pas saturer le CPU
            await asyncio.sleep(0.02)

            # ------- MATRICE DE BOUTONS (inchangé pour l'extension existante) -------
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

            # ------- CAPTEUR TACTILE (nouveaux messages dédiés) -------
            with touchsensor_lock:
                touch_value, touch_state = touch_sensor.step()

            if touch_state:
                # On envoie un message séparé pour le capteur tactile
                # Format différent pour ne PAS perturber buttonmatrix.js
                message = json.dumps({
                    "touchValue": touch_value,
                    "touchState": touch_state
                })
                try:
                    await websocket.send(message)
                except websockets.ConnectionClosed:
                    break

            # ------- JOYSTICK (valeurs brutes X/Y, broadcast si besoin) -------
            now = loop.time()
            if now - last_joy_sent >= joy_interval:
                with joystick_lock:
                    joy_x, joy_y = joystick.read()

                if (
                    last_joy_x is None
                    or abs(joy_x - last_joy_x) >= joy_threshold
                    or abs(joy_y - last_joy_y) >= joy_threshold
                ):
                    joy_message = json.dumps({
                        "joystickX": joy_x,
                        "joystickY": joy_y
                    })
                    try:
                        await websocket.send(joy_message)
                    except websockets.ConnectionClosed:
                        break

                    last_joy_x = joy_x
                    last_joy_y = joy_y
                    last_joy_sent = now

            # ------- TILT (événements gauche/droite uniquement sur changement) -------
            with tiltsensor_lock:
                tilt_value, tilt_direction = tilt_sensor.step()

            if tilt_direction:
                tilt_message = json.dumps({
                    "tiltValue": tilt_value,
                    "tiltDirection": tilt_direction
                })
                try:
                    await websocket.send(tilt_message)
                except websockets.ConnectionClosed:
                    break

            # ------- SOUNDSENSOR (événements de bruit) -------
            with soundsensor_lock:
                sound_value, sound_state = sound_sensor.step()

            if sound_state:
                sound_message = json.dumps({
                    "soundValue": sound_value,
                    "soundState": sound_state
                })
                try:
                    await websocket.send(sound_message)
                except websockets.ConnectionClosed:
                    break

            # ------- IRSENSOR (événements IR sur trame complète) -------
            with irsensor_lock:
                ir_code, ir_name = ir_sensor.step()

            if ir_name:
                ir_message = json.dumps({
                    "irCode": ir_code,
                    "irName": ir_name
                })
                try:
                    await websocket.send(ir_message)
                except websockets.ConnectionClosed:
                    break

            # ------- NFC (présence / insertion / retrait de carte) -------
            with nfcsensor_lock:
                nfc_present, nfc_uid, nfc_event = nfcsensor.step()

            if nfc_event:
                nfc_message = json.dumps({
                    "nfcPresent": bool(nfc_present),
                    "nfcUid": nfc_uid,
                    "nfcEvent": nfc_event
                })
                try:
                    await websocket.send(nfc_message)
                except websockets.ConnectionClosed:
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
