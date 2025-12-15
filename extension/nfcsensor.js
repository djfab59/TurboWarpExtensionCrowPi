(function (Scratch) {
  'use strict';

  class CrowPiNFCSensor {
    constructor () {
      this._present = false;
      this._uid = '';
      this._pendingEvents = [];

      this.debug = typeof window !== 'undefined' &&
        window.location &&
        window.location.search &&
        window.location.search.includes('debug=1');

      this._connect();
    }

    getInfo () {
      return {
        id: 'crowpinfcsensor',
        name: 'CrowPi NFC Sensor',
        color1: '#009688',
        color2: '#00897B',
        color3: '#00695C',
        blocks: [
          {
            opcode: 'whenInserted',
            blockType: Scratch.BlockType.HAT,
            text: 'quand carte NFC détectée'
          },
          {
            opcode: 'whenRemoved',
            blockType: Scratch.BlockType.HAT,
            text: 'quand carte NFC retirée'
          },
          {
            opcode: 'readText',
            blockType: Scratch.BlockType.REPORTER,
            text: 'lire texte NFC'
          },
          {
            opcode: 'writeText',
            blockType: Scratch.BlockType.COMMAND,
            text: 'écrire texte NFC [TEXT]',
            arguments: {
              TEXT: {
                type: Scratch.ArgumentType.STRING,
                defaultValue: 'Hello NFC'
              }
            }
          },
          {
            opcode: 'getUid',
            blockType: Scratch.BlockType.REPORTER,
            text: 'UID de la carte NFC'
          },
          {
            opcode: 'isPresent',
            blockType: Scratch.BlockType.BOOLEAN,
            text: 'carte NFC présente ?'
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

            if (!Object.prototype.hasOwnProperty.call(data, 'nfcEvent')) {
              return;
            }

            const present = Boolean(data.nfcPresent);
            const uid = String(data.nfcUid || '');
            const evt = String(data.nfcEvent || '');

            this._present = present;
            this._uid = uid;

            if (this.debug) {
              console.log('[CrowPi NFCSensor] event', data);
            }

            if (evt === 'insert' || evt === 'remove') {
              this._pendingEvents.push({ type: evt });
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

    whenInserted () {
      return this._consumeEvent('insert');
    }

    whenRemoved () {
      return this._consumeEvent('remove');
    }

    getUid () {
      return this._uid;
    }

    isPresent () {
      return this._present;
    }

    // --- Lecture / écriture de texte NFC via HTTP ---

    async readText () {
      try {
        const res = await fetch('http://127.0.0.1:3232/nfcsensor/read_text');
        const data = await res.json();
        if (data && data.ok && typeof data.text === 'string') {
          return data.text;
        }
      } catch (e) {
        // ignore errors
      }
      return '';
    }

    async writeText (args) {
      const text = String(args.TEXT || '');
      try {
        await fetch('http://127.0.0.1:3232/nfcsensor/write_text', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ text })
        });
      } catch (e) {
        // ignore errors
      }
    }
  }

  Scratch.extensions.register(new CrowPiNFCSensor());
})(Scratch);
