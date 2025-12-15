(function (Scratch) {
  'use strict';

  class CrowPiTiltSensor {
    constructor () {
      this._pendingEvents = [];

      this.debug = typeof window !== 'undefined' &&
        window.location &&
        window.location.search &&
        window.location.search.includes('debug=1');

      this._connect();
    }

    getInfo () {
      return {
        id: 'crowpitiltsensor',
        name: 'CrowPi Tilt Sensor',
        color1: '#9C27B0',
        color2: '#8E24AA',
        color3: '#6A1B9A',
        blocks: [
          {
            opcode: 'whenLeft',
            blockType: Scratch.BlockType.HAT,
            text: 'quand penché à gauche'
          },
          {
            opcode: 'whenRight',
            blockType: Scratch.BlockType.HAT,
            text: 'quand penché à droite'
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
          // rien à envoyer à l'ouverture
        };

        socket.onmessage = (event) => {
          try {
            const data = JSON.parse(event.data);

            if (!Object.prototype.hasOwnProperty.call(data, 'tiltDirection')) {
              return;
            }

            const direction = String(data.tiltDirection || '');

            if (this.debug) {
              console.log('[CrowPi TiltSensor] event', data);
            }

            if (direction === 'left' || direction === 'right') {
              this._pendingEvents.push({ direction });
            }
          } catch (e) {
            // ignore parsing errors
          }
        };

        socket.onclose = () => {
          setTimeout(() => this._connect(), 500);
        };

        socket.onerror = () => {
          // l'erreur sera suivie d'un onclose -> reconnexion
        };
      } catch (e) {
        // Si création du WebSocket échoue, on ne fait rien de spécial.
      }
    }

    _consumeEvent (direction) {
      for (let i = 0; i < this._pendingEvents.length; i++) {
        const ev = this._pendingEvents[i];
        if (ev.direction === direction) {
          this._pendingEvents.splice(i, 1);
          return true;
        }
      }
      return false;
    }

    whenLeft () {
      return this._consumeEvent('left');
    }

    whenRight () {
      return this._consumeEvent('right');
    }
  }

  Scratch.extensions.register(new CrowPiTiltSensor());
})(Scratch);

