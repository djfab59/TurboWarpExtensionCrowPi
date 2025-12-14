(function (Scratch) {
  'use strict';

  class CrowPiLedMatrix {
    getInfo () {
      return {
        id: 'crowpiledmatrix',
        name: 'Matrice 8x8',
        color1: '#AA66CC',
        color2: '#995CB8',
        color3: '#774690',
        blocks: [
          {
            opcode: 'clear',
            blockType: Scratch.BlockType.COMMAND,
            text: 'effacer la matrice'
          },
          {
            opcode: 'setPixelColor',
            blockType: Scratch.BlockType.COMMAND,
            text: 'allumer pixel x [X] y [Y] couleur [COLOR]',
            arguments: {
              X: {
                type: Scratch.ArgumentType.NUMBER,
                defaultValue: 1
              },
              Y: {
                type: Scratch.ArgumentType.NUMBER,
                defaultValue: 1
              },
              COLOR: {
                type: Scratch.ArgumentType.STRING,
                defaultValue: 'blanc',
                menu: 'colors'
              }
            }
          },
          {
            opcode: 'setPixelRGB',
            blockType: Scratch.BlockType.COMMAND,
            text: 'pixel x [X] y [Y] couleur R [R] V [G] B [B]',
            arguments: {
              X: {
                type: Scratch.ArgumentType.NUMBER,
                defaultValue: 1
              },
              Y: {
                type: Scratch.ArgumentType.NUMBER,
                defaultValue: 1
              },
              R: {
                type: Scratch.ArgumentType.NUMBER,
                defaultValue: 255
              },
              G: {
                type: Scratch.ArgumentType.NUMBER,
                defaultValue: 255
              },
              B: {
                type: Scratch.ArgumentType.NUMBER,
                defaultValue: 255
              }
            }
          },
          {
            opcode: 'clearPixel',
            blockType: Scratch.BlockType.COMMAND,
            text: 'éteindre pixel x [X] y [Y]',
            arguments: {
              X: {
                type: Scratch.ArgumentType.NUMBER,
                defaultValue: 1
              },
              Y: {
                type: Scratch.ArgumentType.NUMBER,
                defaultValue: 1
              }
            }
          },
          {
            opcode: 'fillColor',
            blockType: Scratch.BlockType.COMMAND,
            text: 'remplir matrice couleur [COLOR]',
            arguments: {
              COLOR: {
                type: Scratch.ArgumentType.STRING,
                defaultValue: 'blanc',
                menu: 'colors'
              }
            }
          },
          {
            opcode: 'playEmoji',
            blockType: Scratch.BlockType.COMMAND,
            text: 'jouer emoji [EMOJI]',
            arguments: {
              EMOJI: {
                type: Scratch.ArgumentType.STRING,
                defaultValue: 'smiley',
                menu: 'emojis'
              }
            }
          }
        ],
        menus: {
          colors: {
            acceptReporters: false,
            items: [
              'rouge',
              'vert',
              'bleu',
              'blanc',
              'jaune',
              'cyan',
              'magenta',
              'rose',
              'orange',
              'violet',
              'noir'
            ]
          },
          emojis: {
            acceptReporters: false,
            items: ['smiley', 'smiley_langue', 'smiley_square', 'smiley_square_sad', 'smiley_square_love', 'smiley_square_Ho', 'smiley_square_crazy', 'sad', 'heart', 'blink']
          }
        }
      };
    }

    clear () {
      this._post('/ledmatrix/clear', {});
    }

    setPixelColor (args) {
      this._post('/ledmatrix/pixel/color', {
        x: Number(args.X),
        y: Number(args.Y),
        color: args.COLOR
      });
    }

    setPixelRGB (args) {
      this._post('/ledmatrix/pixel/rgb', {
        x: Number(args.X),
        y: Number(args.Y),
        r: Number(args.R),
        g: Number(args.G),
        b: Number(args.B)
      });
    }

    clearPixel (args) {
      this._post('/ledmatrix/pixel/off', {
        x: Number(args.X),
        y: Number(args.Y)
      });
    }

    fillColor (args) {
      this._post('/ledmatrix/fill/color', {
        color: args.COLOR
      });
    }

    playEmoji (args) {
      this._post('/ledmatrix/emoji', {
        name: args.EMOJI
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

  Scratch.extensions.register(new CrowPiLedMatrix());
})(Scratch);
