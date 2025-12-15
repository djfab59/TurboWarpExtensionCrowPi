(function (Scratch) {
  'use strict';

  class CrowPiServo {
    getInfo () {
      return {
        id: 'crowpiservo',
        name: 'CrowPi Servo',
        color1: '#FFB300',
        color2: '#FFA000',
        color3: '#FB8C00',
        blocks: [
          {
            opcode: 'setAngle',
            blockType: Scratch.BlockType.COMMAND,
            text: 'mettre le servo [ID] à angle [ANGLE]',
            arguments: {
              ID: {
                type: Scratch.ArgumentType.NUMBER,
                defaultValue: 1
              },
              ANGLE: {
                type: Scratch.ArgumentType.ANGLE,
                defaultValue: 90
              }
            }
          },
          {
            opcode: 'setPosition',
            blockType: Scratch.BlockType.COMMAND,
            text: 'mettre le servo [ID] à position [POS]',
            arguments: {
              ID: {
                type: Scratch.ArgumentType.NUMBER,
                defaultValue: 1
              },
              POS: {
                type: Scratch.ArgumentType.STRING,
                defaultValue: 'centre',
                menu: 'positions'
              }
            }
          },
          {
            opcode: 'getAngle',
            blockType: Scratch.BlockType.REPORTER,
            text: 'position actuelle du servo [ID]',
            arguments: {
              ID: {
                type: Scratch.ArgumentType.NUMBER,
                defaultValue: 1
              }
            }
          }
        ],
        menus: {
          positions: {
            acceptReporters: false,
            items: ['min', 'centre', 'max']
          }
        }
      };
    }

    async setAngle (args) {
      const id = Number(args.ID || 1);
      const angle = Number(args.ANGLE || 0);
      try {
        await fetch('http://127.0.0.1:3232/servo/set_angle', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            id,
            angle
          })
        });
      } catch (e) {
        // ignore errors
      }
    }

    async setPosition (args) {
      const id = Number(args.ID || 1);
      const pos = String(args.POS || 'centre');
      try {
        await fetch('http://127.0.0.1:3232/servo/set_position', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            id,
            position: pos
          })
        });
      } catch (e) {
        // ignore errors
      }
    }

    async getAngle (args) {
      const id = Number(args.ID || 1);
      try {
        const res = await fetch(`http://127.0.0.1:3232/servo/get_angle?id=${encodeURIComponent(id)}`);
        const data = await res.json();
        if (data && data.ok && typeof data.angle === 'number') {
          return data.angle;
        }
      } catch (e) {
        // ignore errors
      }
      return 0;
    }
  }

  Scratch.extensions.register(new CrowPiServo());
})(Scratch);

