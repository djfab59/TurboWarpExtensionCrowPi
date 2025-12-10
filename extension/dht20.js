class DHTModule {
  getBlocks () {
    return [
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
    ];
  }

  getMenus () {
    return {};
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

module.exports = DHTModule;
