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
            opcode: 'playAnimation',
            blockType: Scratch.BlockType.COMMAND,
            text: 'jouer animation [ANIM] couleur [COLOR]',
            arguments: {
              ANIM: {
                type: Scratch.ArgumentType.STRING,
                defaultValue: 'smiley',
                menu: 'anims'
              },
              COLOR: {
                type: Scratch.ArgumentType.STRING,
                defaultValue: 'blanc',
                menu: 'colors'
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
          anims: {
            acceptReporters: false,
            items: ['smiley', 'sad', 'heart', 'blink']
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

    playAnimation (args) {
      this._post('/ledmatrix/animation', {
        name: args.ANIM,
        color: args.COLOR
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
