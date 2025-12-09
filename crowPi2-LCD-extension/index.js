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
                    }
                ]
            };
        }

        write(args) {
            this._post('/lcd/write', { text: args.TEXT });
        }

        clear() {
            this._post('/lcd/clear', {});
        }

        _post(path, data) {
            var xhr = new XMLHttpRequest();
            xhr.open('POST', 'http://127.0.0.1:3232' + path, true);
            xhr.setRequestHeader('Content-Type', 'application/json');
            xhr.send(JSON.stringify(data));
        }
    }

    Scratch.extensions.register(new CrowPi3LCD());

})(Scratch);

