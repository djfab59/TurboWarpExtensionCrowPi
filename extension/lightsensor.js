(function (Scratch) {
  'use strict';

  class CrowPiLightSensor {
    getInfo () {
      return {
        id: 'crowpilightsensor',
        name: 'Capteur de lumière',
        color1: '#66CCFF',
        color2: '#5CB8E6',
        color3: '#4690B3',
        blocks: [
          {
            opcode: 'lux',
            blockType: Scratch.BlockType.REPORTER,
            text: 'luminosité (lux)'
          }
        ],
        menus: {}
      };
    }

    async lux () {
      try {
        const res = await fetch('http://127.0.0.1:3232/lightsensor/read');
        const data = await res.json();
        if (data && typeof data.lux === 'number') {
          return data.lux;
        }
      } catch (e) {
        // ignore errors and return 0
      }
      return 0;
    }
  }

  Scratch.extensions.register(new CrowPiLightSensor());
})(Scratch);

