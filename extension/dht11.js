(function (Scratch) {
    'use strict';

    class CrowPiDHT11 {
        constructor() {
            this._temperature = 0;
            this._humidity = 0;
        }

        getInfo() {
            return {
                id: 'crowpidht11',
                name: 'CrowPi DHT11',
                blocks: [
                    {
                        opcode: 'update',
                        blockType: Scratch.BlockType.COMMAND,
                        text: 'mettre à jour DHT11'
                    },
                    {
                        opcode: 'temperature',
                        blockType: Scratch.BlockType.REPORTER,
                        text: 'température (°C)'
                    },
                    {
                        opcode: 'humidity',
                        blockType: Scratch.BlockType.REPORTER,
                        text: 'humidité (%)'
                    }
                ]
            };
        }

        update() {
            return fetch('http://127.0.0.1:3232/dht11/read')
                .then(r => r.json())
                .then(data => {
                    if (data.temperature !== null) {
                        this._temperature = data.temperature;
                        this._humidity = data.humidity;
                    }
                });
        }

        temperature() {
            return this._temperature;
        }

        humidity() {
            return this._humidity;
        }
    }

    Scratch.extensions.register(new CrowPiDHT11());

})(Scratch);