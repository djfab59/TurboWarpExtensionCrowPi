(function (Scratch) {
  'use strict';

  const MUSIC_FILES = ['happybirthday.mp3', 'tetris.mp3'];
  const SOUND_FILES = ['die.wav', 'ding.wav', 'dong.wav', 'hit.wav', 'm_die.wav', 'point.wav', 'swoosh.wav'];
  const NOTES = ['do', 're', 'mi', 'fa', 'sol', 'la', 'si', 'do2', 're2', 'mi2', 'fa2', 'sol2', 'la2', 'si2'];

  class CrowPiMusic {
    getInfo () {
      return {
        id: 'crowpimusic',
        name: 'CrowPi Music',
        color1: '#9C27B0',
        color2: '#8E24AA',
        color3: '#6A1B9A',
        blocks: [
          {
            opcode: 'playMusic',
            blockType: Scratch.BlockType.COMMAND,
            text: 'joue la musique [MUSIC]',
            arguments: {
              MUSIC: {
                type: Scratch.ArgumentType.STRING,
                defaultValue: 'happybirthday.mp3',
                menu: 'musics'
              }
            }
          },
          {
            opcode: 'stopMusic',
            blockType: Scratch.BlockType.COMMAND,
            text: 'arrêter la musique'
          },
          {
            opcode: 'playSound',
            blockType: Scratch.BlockType.COMMAND,
            text: 'joue le son [SOUND]',
            arguments: {
              SOUND: {
                type: Scratch.ArgumentType.STRING,
                defaultValue: 'ding.wav',
                menu: 'sounds'
              }
            }
          },
          {
            opcode: 'playNote',
            blockType: Scratch.BlockType.COMMAND,
            text: 'joue la note [NOTE] pendant [DURATION] ms',
            arguments: {
              NOTE: {
                type: Scratch.ArgumentType.STRING,
                defaultValue: 'sol',
                menu: 'notes'
              },
              DURATION: {
                type: Scratch.ArgumentType.NUMBER,
                defaultValue: 500
              }
            }
          }
        ],
        menus: {
          musics: {
            acceptReporters: false,
            items: MUSIC_FILES
          },
          sounds: {
            acceptReporters: false,
            items: SOUND_FILES
          },
          notes: {
            acceptReporters: false,
            items: NOTES
          }
        }
      };
    }

    async playMusic (args) {
      const name = String(args.MUSIC || '').trim();
      if (!name) return;
      try {
        await fetch('http://127.0.0.1:3232/music/play_music', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ name })
        });
      } catch (e) {
        // ignore errors
      }
    }

    async stopMusic () {
      try {
        await fetch('http://127.0.0.1:3232/music/stop_music', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          }
        });
      } catch (e) {
        // ignore errors
      }
    }

    async playSound (args) {
      const name = String(args.SOUND || '').trim();
      if (!name) return;
      try {
        await fetch('http://127.0.0.1:3232/music/play_sound', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ name })
        });
      } catch (e) {
        // ignore errors
      }
    }

    async playNote (args) {
      const note = String(args.NOTE || '').trim();
      let duration = Number(args.DURATION || 0);
      if (!note) return;
      if (Number.isNaN(duration) || duration <= 0) {
        duration = 500;
      }
      try {
        await fetch('http://127.0.0.1:3232/music/play_note', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            note,
            duration
          })
        });
      } catch (e) {
        // ignore errors
      }
    }
  }

  Scratch.extensions.register(new CrowPiMusic());
})(Scratch);
