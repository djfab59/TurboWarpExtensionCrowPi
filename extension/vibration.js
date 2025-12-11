(function (Scratch) {
  'use strict';

  class CrowPiVibration {
    getInfo () {
      return {
        id: 'crowpivibration',
        name: 'Vibration',
        color1: '#FFB347',
        color2: '#E6A03F',
        color3: '#B37730',
        blocks: [
          {
            opcode: 'vibrationOn',
            blockType: Scratch.BlockType.COMMAND,
            text: 'activer vibration'
          },
          {
            opcode: 'vibrationOff',
            blockType: Scratch.BlockType.COMMAND,
            text: 'désactiver vibration'
          },
          {
            opcode: 'vibrationPulse',
            blockType: Scratch.BlockType.COMMAND,
            text: 'activer vibration pendant [DUR] ms',
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

    vibrationOn () {
      this._post('/vibration/on', {});
    }

    vibrationOff () {
      this._post('/vibration/off', {});
    }

    vibrationPulse (args) {
      const dur = Number(args.DUR);
      this._post('/vibration/pulse', {
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

  Scratch.extensions.register(new CrowPiVibration());
})(Scratch);

