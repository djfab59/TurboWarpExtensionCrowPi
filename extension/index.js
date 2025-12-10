(function (Scratch) {
  'use strict';

  const LCD = require('./lcd');
  const DHT = require('./dht20');

  class CrowPi {
    constructor () {
      this.lcd = new LCD();
      this.dht = new DHT();
    }

    getInfo () {
      return {
        id: 'crowpi',
        name: 'CrowPi',
        blocks: [
          ...this.lcd.getBlocks(),
          ...this.dht.getBlocks()
        ],
        menus: {
          ...this.lcd.getMenus(),
          ...this.dht.getMenus()
        }
      };
    }

    /* LCD forwarders */
    lcdOn () { return this.lcd.lcdOn(); }
    lcdOff () { return this.lcd.lcdOff(); }
    lcdClear () { return this.lcd.lcdClear(); }
    lcdWrite (args) { return this.lcd.lcdWrite(args); }
    lcdWriteLine (args) { return this.lcd.lcdWriteLine(args); }
    lcdWriteBoth (args) { return this.lcd.lcdWriteBoth(args); }
    lcdScrollStart (args) { return this.lcd.lcdScrollStart(args); }
    lcdScrollStop () { return this.lcd.lcdScrollStop(); }

    /* DHT forwarders */
    dhtTemp () {
      return this.dht.dhtTemp();
    }

    dhtHum () {
      return this.dht.dhtHum();
    }
  }

  Scratch.extensions.register(new CrowPi());

})(Scratch);
