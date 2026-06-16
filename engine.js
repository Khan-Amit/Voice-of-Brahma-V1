// engine.js – Data-driven Voice-of-Brahma-V1 engine
// All Rights Reserved ® Seliim Ahmed

class VoiceOfBrahmaEngine {
    constructor() {
        this.asciiTable = null;
        this.resonanceProfiles = null;
        this.rotorConfigs = null;
        this.energyMatrix = null;
        this.scaleMatrix = null;
        this._loaded = false;
    }

    async loadData() {
        try {
            // Load all data files in parallel
            const [ascii, resonance, rotors] = await Promise.all([
                fetch('data/ascii_table.json').then(r => r.json()),
                fetch('data/resonance_profiles.json').then(r => r.json()),
                fetch('data/rotor_configs.json').then(r => r.json())
            ]);

            this.asciiTable = ascii.mapping;
            this.resonanceProfiles = resonance.profiles;
            this.rotorConfigs = rotors.configs;
            this._loaded = true;

            // Build matrices
            this._buildMatrices();

            console.log('✅ Engine loaded from data files');
            return true;
        } catch (e) {
            console.error('❌ Failed to load data:', e.message);
            return false;
        }
    }

    _buildMatrices() {
        // Build energy and scale matrices from resonance profiles
        this.energyMatrix = {};
        this.scaleMatrix = {};
        const kB = 1.380649e-23;
        const h = 6.62607015e-34;
        const log2_3 = Math.log2(3);
        const pi = Math.PI;

        for (const profile of this.resonanceProfiles) {
            const f = profile.fwhm_hz;
            const lambda = profile.wavelength_nm * 1e-9;
            const E_res = h * f;
            const E_land = kB * profile.temp_k * Math.log(2);
            const ratio = E_land / E_res;
            const scale = (lambda / (2 * pi)) * ratio / log2_3;

            this.energyMatrix[f] = {
                fwhm_hz: f,
                resonance_energy_ev: E_res / 1.602e-19,
                ratio_to_landauer: ratio,
                profile_name: profile.name
            };

            this.scaleMatrix[f] = {
                fwhm_hz: f,
                groove_coupling_length_m: scale,
                ratio_to_landauer: ratio,
                profile_name: profile.name
            };
        }
    }

    textToTernary(text) {
        if (!this._loaded) throw new Error('Engine not loaded');
        let result = '';
        for (const ch of text) {
            const trits = this.asciiTable[ch];
            result += trits ? trits : '?????';
        }
        return result;
    }

    ternaryToText(trits) {
        if (!this._loaded) throw new Error('Engine not loaded');
        trits = trits.replace(/\s/g, '');
        if (trits.length % 5 !== 0) {
            throw new Error('Ternary length must be multiple of 5');
        }
        let result = '';
        const reverseTable = {};
        for (const [key, val] of Object.entries(this.asciiTable)) {
            reverseTable[val] = key;
        }
        for (let i = 0; i < trits.length; i += 5) {
            const chunk = trits.substr(i, 5);
            result += reverseTable[chunk] || '?';
        }
        return result;
    }

    formatTernary(trits) {
        const groups = trits.match(/.{5}/g);
        return groups ? groups.join(' ') : trits;
    }

    formatBinary(binary) {
        const groups = binary.match(/.{8}/g);
        return groups ? groups.join(' ') : binary;
    }

    textToBinary(text) {
        let b = '';
        for (const ch of text) {
            b += ch.charCodeAt(0).toString(2).padStart(8, '0');
        }
        return b;
    }

    binaryToText(binary) {
        if (binary.length % 8 !== 0) {
            throw new Error('Binary length must be multiple of 8');
        }
        let text = '';
        for (let i = 0; i < binary.length; i += 8) {
            const byte = binary.substr(i, 8);
            text += String.fromCharCode(parseInt(byte, 2));
        }
        return text;
    }

    getEnergyMatrix() {
        return this.energyMatrix;
    }

    getScaleMatrix() {
        return this.scaleMatrix;
    }

    computeScale(fwhm_hz, temp_k = 300, wavelength_nm = 780) {
        const kB = 1.380649e-23;
        const h = 6.62607015e-34;
        const lambda = wavelength_nm * 1e-9;
        const log2_3 = Math.log2(3);
        const pi = Math.PI;

        if (fwhm_hz <= 0) {
            return { error: 'FWHM must be positive' };
        }

        const E_land = kB * temp_k * Math.log(2);
        const E_res = h * fwhm_hz;
        const ratio = E_land / E_res;
        const scale = (lambda / (2 * pi)) * ratio / log2_3;

        return {
            groove_coupling_length_m: scale,
            ratio_to_landauer: ratio,
            resonance_energy_ev: E_res / 1.602e-19,
            fwhm_hz: fwhm_hz,
            temperature_k: temp_k
        };
    }
}

// Global instance
const engine = new VoiceOfBrahmaEngine();

// Load data on startup
engine.loadData().then(() => {
    console.log('✅ Engine ready');
});

if (typeof module !== 'undefined') {
    module.exports = { engine };
}
