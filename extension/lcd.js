class LCDModule {
  getBlocks () {
    return [
      {
        opcode: 'lcdOn',
        blockType: Scratch.BlockType.COMMAND,
        text: 'allumer le LCD'
      },
      {
        opcode: 'lcdOff',
        blockType: Scratch.BlockType.COMMAND,
        text: 'éteindre le LCD'
      },
      {
        opcode: 'lcdClear',
        blockType: Scratch.BlockType.COMMAND,
        text: 'effacer le LCD'
      },
      {
        opcode: 'lcdWrite',
        blockType: Scratch.BlockType.COMMAND,
        text: 'afficher [TEXT] sur le LCD',
        arguments: {
          TEXT: {
            type: Scratch.ArgumentType.STRING,
            defaultValue: 'Hello CrowPi'
          }
        }
      },
      {
        opcode: 'lcdWriteLine',
        blockType: Scratch.BlockType.COMMAND,
        text: 'afficher [TEXT] sur ligne [LINE]',
        arguments: {
          TEXT: {
            type: Scratch.ArgumentType.STRING,
            defaultValue: 'Hello'
          },
          LINE: {
            type: Scratch.ArgumentType.NUMBER,
            defaultValue: 1,
            menu: 'lines'
          }
        }
      },
      {
        opcode: 'lcdWriteBoth',
        blockType: Scratch.BlockType.COMMAND,
        text: 'ligne 1 [LINE1] | ligne 2 [LINE2]',
        arguments: {
          LINE1: {
            type: Scratch.ArgumentType.STRING,
            defaultValue: 'Hello'
          },
          LINE2: {
            type: Scratch.ArgumentType.STRING,
            defaultValue: 'World'
          }
        }
      },
      {
        opcode: 'lcdScrollStart',
        blockType: Scratch.BlockType.COMMAND,
        text: 'défilement texte [TEXT] ligne [LINE] vitesse [SPEED] ms',
        arguments: {
          TEXT: {
            type: Scratch.ArgumentType.STRING,
            defaultValue: 'Hello CrowPi'
          },
          LINE: {
            type: Scratch.ArgumentType.NUMBER,
            defaultValue: 1,
            menu: 'lines'
          },
          SPEED: {
            type: Scratch.ArgumentType.NUMBER,
            defaultValue: 200
          }
        }
      },
      {
        opcode: 'lcdScrollStop',
        blockType: Scratch.BlockType.COMMAND,
        text: 'arrêter le défilement'
      }
    ];
  }

  getMenus () {
    return {
      lines: {
        acceptReporters: false,
        items: ['1', '2']
      }
    };
  }

  lcdOn () {
    this._post('/lcd/on', {});
  }

  lcdOff () {
    this._post('/lcd/off', {});
  }

  lcdClear () {
    this._post('/lcd/clear', {});
  }

  lcdWrite (args) {
    this._post('/lcd/write', { text: args.TEXT });
  }

  lcdWriteLine (args) {
    this._post('/lcd/line', {
      line: Number(args.LINE),
      text: args.TEXT
    });
  }

  lcdWriteBoth (args) {
    this._post('/lcd/both', {
      line1: args.LINE1,
      line2: args.LINE2
    });
  }

  lcdScrollStart (args) {
    this._post('/lcd/scroll/start', {
      text: args.TEXT,
      line: Number(args.LINE),
      speed: Number(args.SPEED)
    });
  }

  lcdScrollStop () {
    this._post('/lcd/scroll/stop', {});
  }

  _post (path, data) {
    fetch('http://127.0.0.1:3232' + path, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(data)
    });
  }
}

module.exports = LCDModule;
