 (function (Scratch) {
  'use strict';

  class CrowPiButtonMatrix {
    constructor (runtime) {
      this.runtime = runtime;
      this.lastRaw = -1;
      this.lastMapped = -1;
      this.lastState = null;
      // Mode debug activable via ?debug=1 dans l'URL
      this.debug = typeof window !== 'undefined' &&
        window.location &&
        window.location.search &&
        window.location.search.includes('debug=1');
      this._connect();
    }

    getInfo () {
      return {
        id: 'crowpibuttonmatrix',
        name: 'CrowPi Button Matrix',
        color1: '#FFD500',
        color2: '#E6C000',
        color3: '#B39800',
        blocks: [
          {
            opcode: 'whenKeyPressed',
            blockType: Scratch.BlockType.HAT,
            text: 'quand bouton [KEY] appuyé',
            arguments: {
              KEY: {
                type: Scratch.ArgumentType.STRING,
                defaultValue: '1',
                menu: 'keys'
              }
            }
          },
          {
            opcode: 'whenKeyReleased',
            blockType: Scratch.BlockType.HAT,
            text: 'quand bouton [KEY] relâché',
            arguments: {
              KEY: {
                type: Scratch.ArgumentType.STRING,
                defaultValue: '1',
                menu: 'keys'
              }
            }
          },
          {
            opcode: 'lastKey',
            blockType: Scratch.BlockType.REPORTER,
            text: 'dernier bouton'
          },
          {
            opcode: 'lastRawKey',
            blockType: Scratch.BlockType.REPORTER,
            text: 'dernier brut'
          }
        ],
        menus: {
          keys: {
            acceptReporters: false,
            items: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16']
          }
        }
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
            const raw = Number(data.raw);
            const mapped = Number(data.mapped);
            const state = typeof data.state === 'string' ? data.state : null;

            if (this.debug) {
              // Log minimal des événements pour le debug
              console.log('[CrowPi ButtonMatrix] event', data);
            }

            if (!Number.isNaN(raw)) {
              this.lastRaw = raw;
            }
            if (
              Number.isInteger(mapped) &&
              mapped >= 1 &&
              mapped <= 16
            ) {
              this.lastMapped = mapped;
              this.lastState = state;

              // Déclenchement des blocs chapeau selon l'état
              if (state === 'down') {
                this.runtime.startHats('crowpibuttonmatrix_whenKeyPressed', {
                  KEY: String(mapped)
                });
              } else if (state === 'up') {
                this.runtime.startHats('crowpibuttonmatrix_whenKeyReleased', {
                  KEY: String(mapped)
                });
              }
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

    whenKeyPressed (args) {
      // TurboWarp gère le filtrage via startHats() et l'argument KEY.
      // Ce bloc ne fait qu'autoriser le déclenchement de l'événement.
      return true;
    }

    whenKeyReleased (args) {
      // Idem pour la relâche : le filtrage se fait côté moteur Scratch.
      return true;
    }

    lastKey () {
      return this.lastMapped;
    }

    lastRawKey () {
      return this.lastRaw;
    }
  }

  Scratch.extensions.register(new CrowPiButtonMatrix(Scratch.vm.runtime));
})(Scratch);
