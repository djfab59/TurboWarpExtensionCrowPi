(function (Scratch) {
  'use strict';

  class CrowPiDHT20 {
    getInfo () {
      return {
        id: 'crowpidht20',
        name: 'CrowPi DHT20',
        blocks: [
          {
            opcode: 'dhtTemp',
            blockType: Scratch.BlockType.REPORTER,
            text: 'température (°C)'
          },
          {
            opcode: 'dhtHum',
            blockType: Scratch.BlockType.REPORTER,
            text: 'humidité (%)'
          }
        ],
        menus: {}
      };
    }

    async dhtTemp () {
      try {
        const res = await fetch('http://127.0.0.1:3232/dht20/read');
        const data = await res.json();
        return (data && typeof data.temperature === 'number') ? data.temperature : 0;
      } catch (e) {
        return 0;
      }
    }

    async dhtHum () {
      try {
        const res = await fetch('http://127.0.0.1:3232/dht20/read');
        const data = await res.json();
        return (data && typeof data.humidity === 'number') ? data.humidity : 0;
      } catch (e) {
        return 0;
      }
    }
  }

  Scratch.extensions.register(new CrowPiDHT20());
})(Scratch);
