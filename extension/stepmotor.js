(function (Scratch) {
  'use strict';

  class CrowPiStepMotor {
    getInfo () {
      return {
        id: 'crowpistepmotor',
        name: 'CrowPi Step Motor',
        color1: '#8D6E63',
        color2: '#795548',
        color3: '#5D4037',
        blocks: [
          {
            opcode: 'turnDegrees',
            blockType: Scratch.BlockType.COMMAND,
            text: 'tourner le moteur pas à pas de [DEGREES] ° [DIR] à vitesse [SPEED]',
            arguments: {
              DEGREES: {
                type: Scratch.ArgumentType.ANGLE,
                defaultValue: 360
              },
              DIR: {
                type: Scratch.ArgumentType.STRING,
                defaultValue: 'horaire',
                menu: 'direction'
              },
              SPEED: {
                type: Scratch.ArgumentType.NUMBER,
                defaultValue: 5
              }
            }
          },
          {
            opcode: 'turnSteps',
            blockType: Scratch.BlockType.COMMAND,
            text: 'tourner le moteur pas à pas de [STEPS] pas [DIR] à vitesse [SPEED]',
            arguments: {
              STEPS: {
                type: Scratch.ArgumentType.NUMBER,
                defaultValue: 10
              },
              DIR: {
                type: Scratch.ArgumentType.STRING,
                defaultValue: 'horaire',
                menu: 'direction'
              },
              SPEED: {
                type: Scratch.ArgumentType.NUMBER,
                defaultValue: 5
              }
            }
          },
          {
            opcode: 'resetPosition',
            blockType: Scratch.BlockType.COMMAND,
            text: 'réinitialiser la position du moteur pas à pas'
          },
          {
            opcode: 'getPosition',
            blockType: Scratch.BlockType.REPORTER,
            text: 'position logique du moteur pas à pas (°)'
          }
        ],
        menus: {
          direction: {
            acceptReporters: false,
            items: ['horaire', 'anti-horaire']
          }
        }
      };
    }

    _dirToCode (dir) {
      const s = String(dir || '').toLowerCase();
      if (s.includes('anti')) {
        return 'ccw';
      }
      return 'cw';
    }

    async turnDegrees (args) {
      const degrees = Number(args.DEGREES || 0);
      const direction = this._dirToCode(args.DIR);
      const speed = Number(args.SPEED || 1);
      try {
        await fetch('http://127.0.0.1:3232/stepmotor/turn_degrees', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            degrees,
            direction,
            speed
          })
        });
      } catch (e) {
        // ignore errors
      }
    }

    async turnSteps (args) {
      const steps = Number(args.STEPS || 0);
      const direction = this._dirToCode(args.DIR);
      const speed = Number(args.SPEED || 1);
      try {
        await fetch('http://127.0.0.1:3232/stepmotor/turn_steps', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            steps,
            direction,
            speed
          })
        });
      } catch (e) {
        // ignore errors
      }
    }

    async resetPosition () {
      try {
        await fetch('http://127.0.0.1:3232/stepmotor/reset_position', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          }
        });
      } catch (e) {
        // ignore errors
      }
    }

    async getPosition () {
      try {
        const res = await fetch('http://127.0.0.1:3232/stepmotor/get_position');
        const data = await res.json();
        if (data && data.ok && typeof data.degrees === 'number') {
          return data.degrees;
        }
      } catch (e) {
        // ignore errors
      }
      return 0;
    }
  }

  Scratch.extensions.register(new CrowPiStepMotor());
})(Scratch);
