// engine.js - Ternary Engine
// Voice-of-Brahma-V1
// All Rights Reserved ® Seliim Ahmed

class TernaryEngine {
    constructor() {
        // Built-in ASCII to ternary mapping
        this.asciiToTernary = {};
        this.ternaryToAscii = {};
        this.buildTables();
    }

    buildTables() {
        for (let code = 0; code < 128; code++) {
            const trits = this.intToTernary5(code);
            const char = String.fromCharCode(code);
            this.asciiToTernary[char] = trits;
            this.ternaryToAscii[trits] = char;
        }
        console.log('✅ Ternary Engine initialized');
    }

    intToTernary5(n) {
        if (n === 0) return '00000';
        let digits = '';
        while (n > 0) {
            digits = (n % 3) + digits;
            n = Math.floor(n / 3);
        }
        return digits.padStart(5, '0');
    }

    textToTernary(text) {
        let result = '';
        for (let i = 0; i < text.length; i++) {
            const ch = text[i];
            const trits = this.asciiToTernary[ch];
            result += trits ? trits : '?????';
        }
        return result;
    }

    ternaryToText(trits) {
        trits = trits.replace(/\s/g, '');
        if (trits.length % 5 !== 0) {
            throw new Error('Ternary string length must be a multiple of 5');
        }
        let result = '';
        for (let i = 0; i < trits.length; i += 5) {
            const chunk = trits.substr(i, 5);
            const char = this.ternaryToAscii[chunk];
            result += char ? char : '?';
        }
        return result;
    }

    formatTernary(trits) {
        const groups = trits.match(/.{5}/g);
        return groups ? groups.join(' ') : trits;
    }

    // Enigma Rotor Simulation
    enigmaTransform(input, rotors, reflector) {
        const cleaned = input.replace(/[^012]/g, '');
        if (cleaned.length === 0) return '';

        const defaultRotors = [
            [0, 1, 2],
            [1, 2, 0],
            [2, 0, 1]
        ];
        const defaultReflector = [2, 1, 0];

        const r = rotors || defaultRotors;
        const ref = reflector || defaultReflector;

        const applyRotor = (sym, rotor, inv) => {
            return inv ? rotor.indexOf(sym) : rotor[sym];
        };

        let positions = [0, 0, 0];
        let output = '';

        for (let ch of cleaned) {
            let val = parseInt(ch, 10);
            val = (val + positions[0]) % 3;
            val = applyRotor(val, r[0], false);
            val = applyRotor(val, r[1], false);
            val = applyRotor(val, r[2], false);
            val = ref[val];
            val = applyRotor(val, r[2], true);
            val = applyRotor(val, r[1], true);
            val = applyRotor(val, r[0], true);
            val = (val - positions[0] + 3) % 3;
            output += String(val);
            positions[0] = (positions[0] + 1) % 3;
            if (positions[0] === 0) {
                positions[1] = (positions[1] + 1) % 3;
                if (positions[1] === 0) {
                    positions[2] = (positions[2] + 1) % 3;
                }
            }
        }
        return output;
    }
}

// Create a global instance of the engine
const ternaryEngine = new TernaryEngine();
