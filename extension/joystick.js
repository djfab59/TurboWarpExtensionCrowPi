(function (Scratch) {
  'use strict';

  class CrowPiJoystick {
    constructor () {
      this._x = 512;
      this._y = 512;
      this._deadZone = 200;

      this._pendingEvents = [];

      this._lastLeft = false;
      this._lastRight = false;
      this._lastUp = false;
      this._lastDown = false;

      this.debug = typeof window !== 'undefined' &&
        window.location &&
        window.location.search &&
        window.location.search.includes('debug=1');

      this._connect();
    }

    getInfo () {
      return {
        id: 'crowpijoystick',
        name: 'CrowPi Joystick',
        color1: '#FF9800',
        color2: '#F57C00',
        color3: '#EF6C00',
        blocks: [
          {
            opcode: 'getX',
            blockType: Scratch.BlockType.REPORTER,
            text: 'joystick position X'
          },
          {
            opcode: 'getY',
            blockType: Scratch.BlockType.REPORTER,
            text: 'joystick position Y'
          },
          {
            opcode: 'setDeadZone',
            blockType: Scratch.BlockType.COMMAND,
            text: 'régler zone morte du joystick à [DEAD]',
            arguments: {
              DEAD: {
                type: Scratch.ArgumentType.NUMBER,
                defaultValue: 200
              }
            }
          },
          {
            opcode: 'whenLeft',
            blockType: Scratch.BlockType.HAT,
            text: 'quand joystick ←'
          },
          {
            opcode: 'whenRight',
            blockType: Scratch.BlockType.HAT,
            text: 'quand joystick →'
          },
          {
            opcode: 'whenUp',
            blockType: Scratch.BlockType.HAT,
            text: 'quand joystick ↑'
          },
          {
            opcode: 'whenDown',
            blockType: Scratch.BlockType.HAT,
            text: 'quand joystick ↓'
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

            // On ne s'intéresse qu'aux messages qui contiennent les valeurs joystick
            if (!Object.prototype.hasOwnProperty.call(data, 'joystickX') &&
                !Object.prototype.hasOwnProperty.call(data, 'joystickY')) {
              return;
            }

            const x = Number(data.joystickX);
            const y = Number(data.joystickY);

            if (!Number.isNaN(x)) {
              this._x = x;
            }
            if (!Number.isNaN(y)) {
              this._y = y;
            }

            if (this.debug) {
              console.log('[CrowPi Joystick] X:', this._x, 'Y:', this._y);
            }

            this._updateDirections();
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

    _updateDirections () {
      const center = 512;
      const dz = Math.max(0, Number(this._deadZone) || 0);

      const left = this._x > center + dz;
      const right = this._x < center - dz;
      const up = this._y > center + dz;
      const down = this._y < center - dz;

      // Gestion des événements “front montant” pour chaque direction
      if (left && !this._lastLeft) {
        this._pendingEvents.push({ type: 'left' });
      }
      if (right && !this._lastRight) {
        this._pendingEvents.push({ type: 'right' });
      }
      if (up && !this._lastUp) {
        this._pendingEvents.push({ type: 'up' });
      }
      if (down && !this._lastDown) {
        this._pendingEvents.push({ type: 'down' });
      }

      this._lastLeft = left;
      this._lastRight = right;
      this._lastUp = up;
      this._lastDown = down;
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

    // --- Blocs reporters / commandes ---

    getX () {
      return this._x;
    }

    getY () {
      return this._y;
    }

    setDeadZone (args) {
      const v = Number(args.DEAD);
      if (!Number.isNaN(v)) {
        this._deadZone = Math.max(0, v);
      }
    }

    // --- Hats directionnels ---

    whenLeft () {
      return this._consumeEvent('left');
    }

    whenRight () {
      return this._consumeEvent('right');
    }

    whenUp () {
      return this._consumeEvent('up');
    }

    whenDown () {
      return this._consumeEvent('down');
    }
  }

  Scratch.extensions.register(new CrowPiJoystick());
})(Scratch);
