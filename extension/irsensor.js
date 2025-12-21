(function (Scratch) {
  'use strict';

  class CrowPiIRSensor {
    constructor () {
      this._pendingEvents = [];
      this._lastButtonName = '';

      this.debug = typeof window !== 'undefined' &&
        window.location &&
        window.location.search &&
        window.location.search.includes('debug=1');

      this._connect();
    }

    getInfo () {
      return {
        id: 'crowpiirsensor',
        name: 'CrowPi IR Sensor',
        color1: '#3F51B5',
        color2: '#3949AB',
        color3: '#303F9F',
        blocks: [
          {
            opcode: 'whenCHMinus',
            blockType: Scratch.BlockType.HAT,
            text: 'Quand bouton CH- appuyé'
          },
          {
            opcode: 'whenCH',
            blockType: Scratch.BlockType.HAT,
            text: 'Quand bouton CH appuyé'
          },
          {
            opcode: 'whenCHPlus',
            blockType: Scratch.BlockType.HAT,
            text: 'Quand bouton CH+ appuyé'
          },
          {
            opcode: 'whenPrev',
            blockType: Scratch.BlockType.HAT,
            text: 'Quand bouton PREV appuyé'
          },
          {
            opcode: 'whenNext',
            blockType: Scratch.BlockType.HAT,
            text: 'Quand bouton NEXT appuyé'
          },
          {
            opcode: 'whenPlayPause',
            blockType: Scratch.BlockType.HAT,
            text: 'Quand bouton PLAY/PAUSE appuyé'
          },
          {
            opcode: 'whenPrevTrack',
            blockType: Scratch.BlockType.HAT,
            text: 'Quand bouton précédent (musique) appuyé'
          },
          {
            opcode: 'whenNextTrack',
            blockType: Scratch.BlockType.HAT,
            text: 'Quand bouton suivant (musique) appuyé'
          },
          {
            opcode: 'whenEQ',
            blockType: Scratch.BlockType.HAT,
            text: 'Quand bouton EQ appuyé'
          },
          {
            opcode: 'whenNum0',
            blockType: Scratch.BlockType.HAT,
            text: 'Quand bouton 0 appuyé'
          },
          {
            opcode: 'whenNum1',
            blockType: Scratch.BlockType.HAT,
            text: 'Quand bouton 1 appuyé'
          },
          {
            opcode: 'whenNum2',
            blockType: Scratch.BlockType.HAT,
            text: 'Quand bouton 2 appuyé'
          },
          {
            opcode: 'whenNum3',
            blockType: Scratch.BlockType.HAT,
            text: 'Quand bouton 3 appuyé'
          },
          {
            opcode: 'whenNum4',
            blockType: Scratch.BlockType.HAT,
            text: 'Quand bouton 4 appuyé'
          },
          {
            opcode: 'whenNum5',
            blockType: Scratch.BlockType.HAT,
            text: 'Quand bouton 5 appuyé'
          },
          {
            opcode: 'whenNum6',
            blockType: Scratch.BlockType.HAT,
            text: 'Quand bouton 6 appuyé'
          },
          {
            opcode: 'whenNum7',
            blockType: Scratch.BlockType.HAT,
            text: 'Quand bouton 7 appuyé'
          },
          {
            opcode: 'whenNum8',
            blockType: Scratch.BlockType.HAT,
            text: 'Quand bouton 8 appuyé'
          },
          {
            opcode: 'whenNum9',
            blockType: Scratch.BlockType.HAT,
            text: 'Quand bouton 9 appuyé'
          },
          {
            opcode: 'when100Plus',
            blockType: Scratch.BlockType.HAT,
            text: 'Quand bouton 100+ appuyé'
          },
          {
            opcode: 'when200Plus',
            blockType: Scratch.BlockType.HAT,
            text: 'Quand bouton 200+ appuyé'
          },
          {
            opcode: 'lastButton',
            blockType: Scratch.BlockType.REPORTER,
            text: 'dernier bouton IR'
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

            if (!Object.prototype.hasOwnProperty.call(data, 'irName')) {
              return;
            }

            const name = String(data.irName || '');

            if (this.debug) {
              console.log('[CrowPi IRSensor] event', data);
            }

            if (name) {
              this._lastButtonName = name;
              this._pendingEvents.push({ name });
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

    _consumeEvent (targetName) {
      for (let i = 0; i < this._pendingEvents.length; i++) {
        const ev = this._pendingEvents[i];
        if (ev.name === targetName) {
          this._pendingEvents.splice(i, 1);
          return true;
        }
      }
      return false;
    }

    whenCHMinus () {
      return this._consumeEvent('CH_MINUS');
    }

    whenCH () {
      return this._consumeEvent('CH');
    }

    whenCHPlus () {
      return this._consumeEvent('CH_PLUS');
    }

    whenPrev () {
      return this._consumeEvent('PREV');
    }

    whenNext () {
      return this._consumeEvent('NEXT');
    }

    whenPlayPause () {
      return this._consumeEvent('PLAY_PAUSE');
    }

    whenPrevTrack () {
      return this._consumeEvent('PREV_TRACK');
    }

    whenNextTrack () {
      return this._consumeEvent('NEXT_TRACK');
    }

    whenEQ () {
      return this._consumeEvent('EQ');
    }

    whenNum0 () {
      return this._consumeEvent('NUM_0');
    }

    whenNum1 () {
      return this._consumeEvent('NUM_1');
    }

    whenNum2 () {
      return this._consumeEvent('NUM_2');
    }

    whenNum3 () {
      return this._consumeEvent('NUM_3');
    }

    whenNum4 () {
      return this._consumeEvent('NUM_4');
    }

    whenNum5 () {
      return this._consumeEvent('NUM_5');
    }

    whenNum6 () {
      return this._consumeEvent('NUM_6');
    }

    whenNum7 () {
      return this._consumeEvent('NUM_7');
    }

    whenNum8 () {
      return this._consumeEvent('NUM_8');
    }

    whenNum9 () {
      return this._consumeEvent('NUM_9');
    }

    when100Plus () {
      return this._consumeEvent('HUNDRED_PLUS');
    }

    when200Plus () {
      return this._consumeEvent('TWOHUNDRED_PLUS');
    }

    lastButton () {
      return this._lastButtonName;
    }
  }

  Scratch.extensions.register(new CrowPiIRSensor());
})(Scratch);
