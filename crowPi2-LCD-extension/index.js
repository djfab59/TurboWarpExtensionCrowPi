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
                        opcode: 'writeBoth',
                        blockType: Scratch.BlockType.COMMAND,
                        text: 'ligne 1 [LINE1] | ligne 2 [LINE2]',
                        arguments: {
                            LINE1: {
                                type: Scratch.ArgumentType.STRING,
                                defaultValue: 'Hello'
                            },
                            LINE2: {
                                type: Scratch.ArgumentType.STRING,
                                defaultValue: 'World'
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
                ],
                menus: {
                    lines: {
                        acceptReporters: false,
                        items: ['1', '2']
                    }
                }
            };
        }

        write(args) {
            this._post('/lcd/write', { text: args.TEXT });
        }

        writeLine(args) {
            this._post('/lcd/line', {
                line: Number(args.LINE),
                text: args.TEXT
            });
        }

        writeBoth(args) {
            this._post('/lcd/both', {
                line1: args.LINE1,
                line2: args.LINE2
            });
        }
        
        clear() {
            this._post('/lcd/clear', {});
        }

        on() {
            this._post('/lcd/on', {});
        }

        off() {
            this._post('/lcd/off', {});
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
