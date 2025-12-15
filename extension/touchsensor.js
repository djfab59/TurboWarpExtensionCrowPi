(function (Scratch) {
  'use strict';

  class CrowPiTouchSensor {
    constructor () {
      this.currentValue = 0; // 0 ou 1
      this.lastState = null;
      this._pendingEvents = [];

      this.debug = typeof window !== 'undefined' &&
        window.location &&
        window.location.search &&
        window.location.search.includes('debug=1');

      this._connect();
    }

    getInfo () {
      return {
        id: 'crowpitouchsensor',
        name: 'CrowPi Touch Sensor',
        color1: '#4CAF50',
        color2: '#43A047',
        color3: '#2E7D32',
        blocks: [
          {
            opcode: 'whenTouched',
            blockType: Scratch.BlockType.HAT,
            text: 'quand capteur tactile touché'
          },
          {
            opcode: 'whenReleased',
            blockType: Scratch.BlockType.HAT,
            text: 'quand capteur tactile relâché'
          },
          {
            opcode: 'isTouched',
            blockType: Scratch.BlockType.BOOLEAN,
            text: 'capteur tactile appuyé ?'
          }
        ]
      };
    }

    _connect () {
      const url = 'ws://127.0.0.1:3233';
      try {
        const socket = new WebSocket(url);
        this._socket = socket;

        socket.onopen = () => {
          // rien de spécial à envoyer à l'ouverture
        };

        socket.onmessage = (event) => {
          try {
            const data = JSON.parse(event.data);

            // On ne s'intéresse qu'aux messages générés
            // pour le capteur tactile (touchValue/touchState).
            if (!Object.prototype.hasOwnProperty.call(data, 'touchState')) {
              return;
            }

            const value = Number(data.touchValue);
            const state = typeof data.touchState === 'string' ? data.touchState : null;

            if (this.debug) {
              console.log('[CrowPi TouchSensor] event', data);
            }

            if (!Number.isNaN(value)) {
              this.currentValue = value;
            }

            if (state === 'down' || state === 'up') {
              this.lastState = state;
              this._pendingEvents.push({ state });
            }
          } catch (e) {
            // ignore parsing errors
          }
        };

        socket.onclose = () => {
          // tentative de reconnexion simple, avec léger délai
          setTimeout(() => this._connect(), 500);
        };

        socket.onerror = () => {
          // l'erreur sera suivie d'un onclose -> reconnexion
        };
      } catch (e) {
        // Si création du WebSocket échoue, on ne fait rien de spécial.
      }
    }

    _consumeEvent (desiredState) {
      for (let i = 0; i < this._pendingEvents.length; i++) {
        const ev = this._pendingEvents[i];
        if (ev.state === desiredState) {
          this._pendingEvents.splice(i, 1);
          return true;
        }
      }
      return false;
    }

    whenTouched () {
      return this._consumeEvent('down');
    }

    whenReleased () {
      return this._consumeEvent('up');
    }

    isTouched () {
      return !!this.currentValue;
    }
  }

  Scratch.extensions.register(new CrowPiTouchSensor());
})(Scratch);

