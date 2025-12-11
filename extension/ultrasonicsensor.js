(function (Scratch) {
  'use strict';

  class CrowPiUltrasonic {
    getInfo () {
      return {
        id: 'crowpiultrasonic',
        name: 'Capteur ultrason',
        color1: '#4FC3F7',
        color2: '#46AFDE',
        color3: '#3687AC',
        blocks: [
          {
            opcode: 'distance',
            blockType: Scratch.BlockType.REPORTER,
            text: 'distance (cm)'
          }
        ],
        menus: {}
      };
    }

    async distance () {
      try {
        const res = await fetch('http://127.0.0.1:3232/ultrasonicsensor/read');
        const data = await res.json();
        if (data && typeof data.distance === 'number') {
          return data.distance;
        }
        // Pas de mesure valide (ex: timeout capteur) -> on renvoie -1
        return -1;
      } catch (e) {
        return -1;
      }
    }
  }

  Scratch.extensions.register(new CrowPiUltrasonic());
})(Scratch);

