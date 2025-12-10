(function (Scratch) {
    'use strict';

    class CrowPiLCD {
        getInfo() {
            return {
                id: 'crowpilcd',
                name: 'CrowPi LCD',
                blocks: [
                    {
                        opcode: 'writeLine',
                        blockType: Scratch.BlockType.COMMAND,
                        text: 'afficher [TEXT] sur ligne [LINE]',
                        arguments: {
                            TEXT: {
                                type: Scratch.ArgumentType.STRING,
                                defaultValue: 'Hello'
                            },
                            LINE: {
                                type: Scratch.ArgumentType.NUMBER,
                                defaultValue: 1,
                                menu: 'lines'
                            }
                        }
                    },
                    {
                        opcode: 'scrollStart',
                        blockType: Scratch.BlockType.COMMAND,
                        text: 'défilement [TEXT] ligne [LINE] vitesse [SPEED] ms',
                        arguments: {
                            TEXT: { type: Scratch.ArgumentType.STRING, defaultValue: 'Scroll' },
                            LINE: { type: Scratch.ArgumentType.NUMBER, defaultValue: 1, menu: 'lines' },
                            SPEED: { type: Scratch.ArgumentType.NUMBER, defaultValue: 200 }
                        }
                    },
                    {
                        opcode: 'scrollStop',
                        blockType: Scratch.BlockType.COMMAND,
                        text: 'arrêter défilement'
                    }
                ],
                menus: {
                    lines: {
                        items: ['1', '2']
                    }
                }
            };
        }

        writeLine(args) {
            this._post('/lcd/line', {
                line: Number(args.LINE),
                text: args.TEXT
            });
        }

        scrollStart(args) {
            this._post('/lcd/scroll/start', {
                text: args.TEXT,
                line: Number(args.LINE),
                speed: Number(args.SPEED)
            });
        }

        scrollStop() {
            this._post('/lcd/scroll/stop', {});
        }

        _post(path, data) {
            const xhr = new XMLHttpRequest();
            xhr.open('POST', 'http://127.0.0.1:3232' + path);
            xhr.setRequestHeader('Content-Type', 'application/json');
            xhr.send(JSON.stringify(data));
        }
    }

    Scratch.extensions.register(new CrowPiLCD());

})(Scratch);