(function (Scratch) {
  'use strict';

  class CrowPiRelay {
    getInfo () {
      return {
        id: 'crowpirelay',
        name: 'Relais',
        color1: '#4DB6AC',
        color2: '#45A39A',
        color3: '#357A73',
        blocks: [
          {
            opcode: 'relayOn',
            blockType: Scratch.BlockType.COMMAND,
            text: 'activer relais'
          },
          {
            opcode: 'relayOff',
            blockType: Scratch.BlockType.COMMAND,
            text: 'désactiver relais'
          },
          {
            opcode: 'relayPulse',
            blockType: Scratch.BlockType.COMMAND,
            text: 'activer relais pendant [DUR] ms',
            arguments: {
              DUR: {
                type: Scratch.ArgumentType.NUMBER,
                defaultValue: 500
              }
            }
          }
        ],
        menus: {}
      };
    }

    relayOn () {
      this._post('/relay/on', {});
    }

    relayOff () {
      this._post('/relay/off', {});
    }

    relayPulse (args) {
      const dur = Number(args.DUR);
      this._post('/relay/pulse', {
        duration: Number.isFinite(dur) ? dur : 500
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

  Scratch.extensions.register(new CrowPiRelay());
})(Scratch);

