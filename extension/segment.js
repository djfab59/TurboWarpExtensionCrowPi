(function (Scratch) {
  'use strict';

  class CrowPiSegment {
    getInfo () {
      return {
        id: 'crowpisegment',
        name: 'Afficheur 7 segments',
        color1: '#9E9E9E',
        color2: '#8E8E8E',
        color3: '#6E6E6E',
        blocks: [
          {
            opcode: 'init',
            blockType: Scratch.BlockType.COMMAND,
            text: 'initialiser le 7-segments'
          },
          {
            opcode: 'displayNumber',
            blockType: Scratch.BlockType.COMMAND,
            text: 'afficher nombre [NUM] sur le 7-segments',
            arguments: {
              NUM: {
                type: Scratch.ArgumentType.NUMBER,
                defaultValue: 0
              }
            }
          },
          {
            opcode: 'setDigit',
            blockType: Scratch.BlockType.COMMAND,
            text: 'écrire chiffre [DIGIT] au digit [POS]',
            arguments: {
              DIGIT: {
                type: Scratch.ArgumentType.NUMBER,
                defaultValue: 0,
                menu: 'digits'
              },
              POS: {
                type: Scratch.ArgumentType.NUMBER,
                defaultValue: 1,
                menu: 'positions'
              }
            }
          },
          {
            opcode: 'decimalOn',
            blockType: Scratch.BlockType.COMMAND,
            text: 'activer le point du digit [POS]',
            arguments: {
              POS: {
                type: Scratch.ArgumentType.NUMBER,
                defaultValue: 1,
                menu: 'positions'
              }
            }
          },
          {
            opcode: 'decimalOff',
            blockType: Scratch.BlockType.COMMAND,
            text: 'désactiver le point du digit [POS]',
            arguments: {
              POS: {
                type: Scratch.ArgumentType.NUMBER,
                defaultValue: 1,
                menu: 'positions'
              }
            }
          },
          {
            opcode: 'colonOn',
            blockType: Scratch.BlockType.COMMAND,
            text: 'activer le deux-points'
          },
          {
            opcode: 'colonOff',
            blockType: Scratch.BlockType.COMMAND,
            text: 'désactiver le deux-points'
          },
          {
            opcode: 'setDigitRaw',
            blockType: Scratch.BlockType.COMMAND,
            text: 'écrire segments bruts [MASK] au digit [POS]',
            arguments: {
              MASK: {
                type: Scratch.ArgumentType.NUMBER,
                defaultValue: 0
              },
              POS: {
                type: Scratch.ArgumentType.NUMBER,
                defaultValue: 1,
                menu: 'positions'
              }
            }
          },
          {
            opcode: 'clear',
            blockType: Scratch.BlockType.COMMAND,
            text: 'effacer l’affichage'
          },
          {
            opcode: 'setBrightness',
            blockType: Scratch.BlockType.COMMAND,
            text: 'régler luminosité [LEVEL]',
            arguments: {
              LEVEL: {
                type: Scratch.ArgumentType.NUMBER,
                defaultValue: 15
              }
            }
          }
        ],
        menus: {
          digits: {
            acceptReporters: false,
            items: ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
          },
          positions: {
            acceptReporters: false,
            items: ['1', '2', '3', '4']
          }
        }
      };
    }

    init () {
      this._post('/segment/init', {});
    }

    displayNumber (args) {
      const n = Number(args.NUM);
      this._post('/segment/display/number', {
        value: Number.isFinite(n) ? n : 0
      });
    }

    setDigit (args) {
      const d = Number(args.DIGIT);
      const p = Number(args.POS);
      this._post('/segment/digit', {
        value: Number.isFinite(d) ? d : 0,
        position: Number.isFinite(p) ? p : 1
      });
    }

    decimalOn (args) {
      const p = Number(args.POS);
      this._post('/segment/decimal/on', {
        position: Number.isFinite(p) ? p : 1
      });
    }

    decimalOff (args) {
      const p = Number(args.POS);
      this._post('/segment/decimal/off', {
        position: Number.isFinite(p) ? p : 1
      });
    }

    colonOn () {
      this._post('/segment/colon/on', {});
    }

    colonOff () {
      this._post('/segment/colon/off', {});
    }

    setDigitRaw (args) {
      const mask = Number(args.MASK);
      const p = Number(args.POS);
      this._post('/segment/digit/raw', {
        bitmask: Number.isFinite(mask) ? mask : 0,
        position: Number.isFinite(p) ? p : 1
      });
    }

    clear () {
      this._post('/segment/clear', {});
    }

    setBrightness (args) {
      const lvl = Number(args.LEVEL);
      this._post('/segment/brightness', {
        level: Number.isFinite(lvl) ? lvl : 15
      });
    }

    _post (path, data) {
      fetch('http://127.0.0.1:3232' + path, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
      });
    }
  }

  Scratch.extensions.register(new CrowPiSegment());
})(Scratch);

