(function (Scratch) {
  'use strict';

  class CrowPiSoundSensor {
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
        id: 'crowpisoundsensor',
        name: 'CrowPi Sound Sensor',
        color1: '#FF5722',
        color2: '#F4511E',
        color3: '#E64A19',
        blocks: [
          {
            opcode: 'whenNoise',
            blockType: Scratch.BlockType.HAT,
            text: 'quand bruit détecté'
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

            if (!Object.prototype.hasOwnProperty.call(data, 'soundState')) {
              return;
            }

            const state = String(data.soundState || '');

            if (this.debug) {
              console.log('[CrowPi SoundSensor] event', data);
            }

            if (state === 'noise') {
              this._pendingEvents.push({ type: 'noise' });
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

    _consumeEvent (type) {
      for (let i = 0; i < this._pendingEvents.length; i++) {
        const ev = this._pendingEvents[i];
        if (ev.type === type) {
          this._pendingEvents.splice(i, 1);
          return true;
        }
      }
      return false;
    }

    whenNoise () {
      return this._consumeEvent('noise');
    }
  }

  Scratch.extensions.register(new CrowPiSoundSensor());
})(Scratch);

