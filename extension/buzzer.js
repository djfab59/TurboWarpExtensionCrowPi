(function (Scratch) {
  'use strict';

  class CrowPiBuzzer {
    getInfo () {
      return {
        id: 'crowpibuzzer',
        name: 'CrowPi Buzzer',
        color1: '#FF8C1A',
        color2: '#E67E17',
        color3: '#B35F11',
        blocks: [
          {
            opcode: 'buzzerOn',
            blockType: Scratch.BlockType.COMMAND,
            text: 'buzzer ON à [FREQ] Hz',
            arguments: {
              FREQ: {
                type: Scratch.ArgumentType.NUMBER,
                defaultValue: 440
              }
            }
          },
          {
            opcode: 'buzzerOff',
            blockType: Scratch.BlockType.COMMAND,
            text: 'buzzer OFF'
          },
          {
            opcode: 'playNote',
            blockType: Scratch.BlockType.COMMAND,
            text: 'jouer la note [NOTE] pendant [DUR] ms',
            arguments: {
              NOTE: {
                type: Scratch.ArgumentType.STRING,
                defaultValue: 'C4'
              },
              DUR: {
                type: Scratch.ArgumentType.NUMBER,
                defaultValue: 500
              }
            }
          },
          {
            opcode: 'playMelody',
            blockType: Scratch.BlockType.COMMAND,
            text: 'jouer mélodie [MELODY]',
            arguments: {
              MELODY: {
                type: Scratch.ArgumentType.STRING,
                defaultValue: 'alerte',
                menu: 'melodies'
              }
            }
          }
        ],
        menus: {
          melodies: {
            acceptReporters: false,
            items: ['marion', 'alerte', 'victoire', 'echec']
          }
        }
      };
    }

    buzzerOn (args) {
      const freq = Number(args.FREQ);
      this._post('/buzzer/on', { freq: Number.isFinite(freq) ? freq : 440 });
    }

    buzzerOff () {
      this._post('/buzzer/off', {});
    }

    playNote (args) {
      const dur = Number(args.DUR);
      this._post('/buzzer/note', {
        note: args.NOTE || 'C4',
        duration: Number.isFinite(dur) ? dur : 500
      });
    }

    playMelody (args) {
      const name = String(args.MELODY || '').toLowerCase();
      this._post('/buzzer/melody', { name });
    }

    _post (path, data) {
      fetch('http://127.0.0.1:3232' + path, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
      });
    }
  }

  Scratch.extensions.register(new CrowPiBuzzer());
})(Scratch);

