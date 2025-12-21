(function (Scratch) {
  'use strict';

  class CrowPiServo {
    constructor () {
      this._lastAngleById = Object.create(null);
    }

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
            text: 'mettre le servo [ID] à angle [ANGLE] (maintenir)',
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
            text: 'mettre le servo [ID] à position [POS] (maintenir)',
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
            opcode: 'setAngleRelease',
            blockType: Scratch.BlockType.COMMAND,
            text: 'mettre le servo [ID] à angle [ANGLE] puis lâcher',
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
            opcode: 'setPositionRelease',
            blockType: Scratch.BlockType.COMMAND,
            text: 'mettre le servo [ID] à position [POS] puis lâcher',
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
          },
          {
            opcode: 'release',
            blockType: Scratch.BlockType.COMMAND,
            text: 'lâcher le servo [ID] (PWM off)',
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
      if (Number.isFinite(id) && Number.isFinite(angle)) {
        this._lastAngleById[String(id)] = angle;
      }
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
      const targetAngle = this._positionToAngle(pos);
      if (Number.isFinite(id) && targetAngle !== null) {
        this._lastAngleById[String(id)] = targetAngle;
      }
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

    async setAngleRelease (args) {
      const id = Number(args.ID || 1);
      const angle = Number(args.ANGLE || 0);
      const waitMs = this._estimateMoveTimeMs(id, angle);
      await this.setAngle({ ID: id, ANGLE: angle });
      await this._sleep(waitMs);
      await this.release({ ID: id });
    }

    async setPositionRelease (args) {
      const id = Number(args.ID || 1);
      const pos = String(args.POS || 'centre');
      const targetAngle = this._positionToAngle(pos);
      const waitMs = this._estimateMoveTimeMs(id, targetAngle === null ? 90 : targetAngle);
      await this.setPosition({ ID: id, POS: pos });
      await this._sleep(waitMs);
      await this.release({ ID: id });
    }

    async release (args) {
      const id = Number(args.ID || 1);
      try {
        await fetch('http://127.0.0.1:3232/servo/release', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            id
          })
        });
      } catch (e) {
        // ignore errors
      }
    }

    _positionToAngle (pos) {
      const p = String(pos || '').toLowerCase().trim();
      if (p === 'min') return 0;
      if (p === 'centre' || p === 'center' || p === 'mid') return 90;
      if (p === 'max') return 180;
      return null;
    }

    _estimateMoveTimeMs (id, targetAngle) {
      const defaultAngle = 90;
      const a = Number(targetAngle);
      const angle = Number.isFinite(a) ? Math.max(0, Math.min(180, a)) : defaultAngle;

      const key = String(id || 1);
      const prevRaw = this._lastAngleById[key];
      const prev = Number.isFinite(Number(prevRaw)) ? Number(prevRaw) : defaultAngle;
      const delta = Math.abs(angle - prev);

      // Estimation simple (à défaut de feedback) : base + facteur * delta.
      const ms = 150 + (delta * 4);
      return Math.max(150, Math.min(1200, Math.round(ms)));
    }

    _sleep (ms) {
      const delay = Math.max(0, Number(ms) || 0);
      return new Promise(resolve => setTimeout(resolve, delay));
    }
  }

  Scratch.extensions.register(new CrowPiServo());
})(Scratch);
