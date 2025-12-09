(function (Scratch) {
    'use strict';

    class CrowPi3LCD {
        getInfo() {
            return {
                id: 'crowpi3lcd',
                name: 'CrowPi3 LCD',
                blocks: [
                    {
                        opcode: 'write',
                        blockType: Scratch.BlockType.COMMAND,
                        text: 'afficher [TEXT] sur le LCD',
                        arguments: {
                            TEXT: {
                                type: Scratch.ArgumentType.STRING,
                                defaultValue: 'Hello CrowPi3'
                            }
                        }
                    },
                    {
                        opcode: 'clear',
                        blockType: Scratch.BlockType.COMMAND,
                        text: 'effacer le LCD'
                    },
                    {
                        opcode: 'on',
                        blockType: Scratch.BlockType.COMMAND,
                        text: 'allumer le LCD'
                    },
                    {
                        opcode: 'off',
                        blockType: Scratch.BlockType.COMMAND,
                        text: 'éteindre le LCD'
                    }
                ]
            };
        }

        write(args) {
            const text = (args.TEXT === undefined || args.TEXT === null) ? '' : String(args.TEXT);
            this._post('/lcd/write', { text });
        }

        clear() {
            this._post('/lcd/clear');
        }

        on() {
            this._post('/lcd/on');
        }

        off() {
            this._post('/lcd/off');
        }

        _post(path, data) {
            const options = { method: 'POST' };
            if (data !== undefined) {
                options.headers = { 'Content-Type': 'application/json' };
                options.body = JSON.stringify(data);
            }
            fetch('http://localhost:3232' + path, options);
        }
    }

    Scratch.extensions.register(new CrowPi3LCD());

})(Scratch);
