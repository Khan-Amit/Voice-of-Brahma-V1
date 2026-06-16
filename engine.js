// ================================================================
// engine.js – Voice-of-Brahma-V1 Complete Backend Engine
// All Rights Reserved ® Seliim Ahmed
// ================================================================

class VoiceOfBrahmaEngine {

    constructor() {
        // ============================================================
        // 1. ASCII CODE LIBRARY (5-trit)
        // ============================================================
        this.asciiToTernary = {};
        this.ternaryToAscii = {};
        this._buildAsciiLibrary();

        // ============================================================
        // 2. RESONANCE CURVE / ENERGY CONSUMPTION MATRIX
        // ============================================================
        this.resonanceDatabase = [];
        this.energyConsumptionMatrix = {};
        this._initResonanceDatabase();
        this._buildEnergyConsumptionMatrix();

        // ============================================================
        // 3. SCALE MATRIX (scalePRT derived values)
        // ============================================================
        this.scaleMatrix = {};
        this._buildScaleMatrix();

        // ============================================================
        // 4. CALCULATION MATRIX (formulas)
        // ============================================================
        this.calculationMatrix = {};
        this._buildCalculationMatrix();

        // ============================================================
        // 5. ENIGMA ROTORS
        // ============================================================
        this.rotors = [
            [0, 1, 2],
            [1, 2, 0],
            [2, 0, 1]
        ];
        this.reflector = [2, 1, 0];

        console.log('✅ Voice-of-Brahma Engine initialized');
        console.log('📚 ASCII Library: 128 entries');
        console.log('📊 Resonance Database: ' + this.resonanceDatabase.length + ' entries');
        console.log('⚡ Energy Consumption Matrix: Built');
        console.log('📐 Scale Matrix: Built');
        console.log('🧮 Calculation Matrix: Built');
        this._printSampleMappings();
    }

    // ================================================================
    // 1. ASCII CODE LIBRARY (5-trit)
    // ================================================================

    _intToTernary5(n) {
        if (n === 0) return '00000';
        let digits = '';
        while (n > 0) {
            digits = (n % 3) + digits;
            n = Math.floor(n / 3);
        }
        return digits.padStart(5, '0');
    }

    _buildAsciiLibrary() {
        for (let code = 0; code < 128; code++) {
            const trits = this._intToTernary5(code);
            const char = String.fromCharCode(code);
            this.asciiToTernary[char] = trits;
            this.asciiToTernary[code] = trits;
            this.ternaryToAscii[trits] = char;
        }
        // Verify critical mappings
        this._verifyAsciiLibrary();
    }

    _verifyAsciiLibrary() {
        const tests = [
            { char: 'A', expected: '02102' },
            { char: 'B', expected: '02110' },
            { char: ' ', expected: '01012' },
            { char: '0', expected: '01210' },
            { char: 'z', expected: '11112' }
        ];
        console.log('   ASCII Library Verification:');
        for (const test of tests) {
            const result = this.asciiToTernary[test.char];
            const status = result === test.expected ? '✅' : '❌';
            console.log(`      ${test.char} -> ${result} (expected ${test.expected}) ${status}`);
        }
    }

    getAsciiLibrary() {
        return this.asciiToTernary;
    }

    getTernaryLibrary() {
        return this.ternaryToAscii;
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
            throw new Error('Ternary length must be multiple of 5');
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

    // ================================================================
    // 2. RESONANCE CURVE / ENERGY CONSUMPTION MATRIX
    // ================================================================

    _initResonanceDatabase() {
        // Pre-populate with typical resonance values
        this.resonanceDatabase = [
            {
                id: 1,
                name: 'Standard U-Groove',
                fwhm_hz: 41700,
                temp_k: 300,
                material: 'GeSbTe',
                wavelength_nm: 780,
                description: 'Standard optical disc with U-bottom groove'
            },
            {
                id: 2,
                name: 'High-Q U-Groove',
                fwhm_hz: 12000,
                temp_k: 300,
                material: 'GeSbTe',
                wavelength_nm: 780,
                description: 'Optimized high-quality resonator'
            },
            {
                id: 3,
                name: 'Low-Q U-Groove',
                fwhm_hz: 100000,
                temp_k: 300,
                material: 'GeSbTe',
                wavelength_nm: 780,
                description: 'Broader resonance for faster readout'
            },
            {
                id: 4,
                name: 'Cryogenic U-Groove',
                fwhm_hz: 1000,
                temp_k: 4,
                material: 'Superconductor',
                wavelength_nm: 780,
                description: 'Near-ideal resonator at low temperature'
            },
            {
                id: 5,
                name: 'Blue Laser U-Groove',
                fwhm_hz: 41700,
                temp_k: 300,
                material: 'GeSbTe',
                wavelength_nm: 405,
                description: 'Higher density with shorter wavelength'
            }
        ];
        console.log('   Resonance Database initialized with ' + this.resonanceDatabase.length + ' entries');
    }

    _buildEnergyConsumptionMatrix() {
        // Energy Consumption Matrix: maps FWHM → energy per bit
        const kB = 1.380649e-23;
        const h = 6.62607015e-34;
        const fwhmValues = [1000, 5000, 10000, 20000, 41700, 50000, 100000, 200000, 500000];
        const tempK = 300;

        for (const fwhm of fwhmValues) {
            const E_res = h * fwhm; // Energy of resonance
            const E_land = kB * tempK * Math.log(2); // Landauer limit at 300K
            const ratio = E_land / E_res;
            const energy_per_bit_j = E_res;
            const energy_per_bit_ev = E_res / 1.602176634e-19;

            this.energyConsumptionMatrix[fwhm] = {
                fwhm_hz: fwhm,
                resonance_energy_j: E_res,
                resonance_energy_ev: energy_per_bit_ev,
                landauer_energy_j: E_land,
                ratio_to_landauer: ratio,
                energy_per_bit_j: energy_per_bit_j,
                energy_per_bit_ev: energy_per_bit_ev,
                relative_to_landauer: ratio
            };
        }
        console.log('   Energy Consumption Matrix built with ' + Object.keys(this.energyConsumptionMatrix).length + ' entries');
        // Print sample
        const sample = this.energyConsumptionMatrix[41700];
        console.log('   Sample (41700 Hz): ' + sample.energy_per_bit_ev.toExponential(4) + ' eV/bit');
    }

    getEnergyConsumption(fwhm_hz) {
        // Get energy consumption for a specific FWHM
        if (this.energyConsumptionMatrix[fwhm_hz]) {
            return this.energyConsumptionMatrix[fwhm_hz];
        }
        // If not in matrix, compute on the fly
        const h = 6.62607015e-34;
        const kB = 1.380649e-23;
        const tempK = 300;
        const E_res = h * fwhm_hz;
        const E_land = kB * tempK * Math.log(2);
        const ratio = E_land / E_res;
        return {
            fwhm_hz: fwhm_hz,
            resonance_energy_j: E_res,
            resonance_energy_ev: E_res / 1.602176634e-19,
            landauer_energy_j: E_land,
            ratio_to_landauer: ratio,
            energy_per_bit_j: E_res,
            energy_per_bit_ev: E_res / 1.602176634e-19,
            relative_to_landauer: ratio
        };
    }

    addResonanceEntry(entry) {
        const newEntry = {
            id: this.resonanceDatabase.length + 1,
            name: entry.name || 'Custom',
            fwhm_hz: entry.fwhm_hz || 41700,
            temp_k: entry.temp_k || 300,
            material: entry.material || 'GeSbTe',
            wavelength_nm: entry.wavelength_nm || 780,
            description: entry.description || 'User-defined resonance',
            date_added: new Date().toISOString()
        };
        this.resonanceDatabase.push(newEntry);
        // Also update energy matrix
        this._buildEnergyConsumptionMatrix();
        console.log('✅ Added resonance entry: ' + newEntry.name);
        return newEntry;
    }

    getResonanceById(id) {
        return this.resonanceDatabase.find(r => r.id === id) || null;
    }

    getResonanceDatabase() {
        return this.resonanceDatabase;
    }

    getEnergyConsumptionMatrix() {
        return this.energyConsumptionMatrix;
    }

    // ================================================================
    // 3. SCALE MATRIX (scalePRT derived values)
    // ================================================================

    _buildScaleMatrix() {
        const fwhmValues = [1000, 5000, 10000, 20000, 41700, 50000, 100000];
        const temp = 300;
        const lambda = 780e-9;
        const kB = 1.380649e-23;
        const h = 6.62607015e-34;
        const log2_3 = Math.log2(3);
        const pi = Math.PI;

        for (const fwhm of fwhmValues) {
            const E_land = kB * temp * Math.log(2);
            const E_res = h * fwhm;
            const ratio = E_land / E_res;
            const scalePRT = (lambda / (2 * pi)) * ratio / log2_3;
            this.scaleMatrix[fwhm] = {
                fwhm_hz: fwhm,
                temperature_k: temp,
                wavelength_m: lambda,
                energy_landauer_j: E_land,
                energy_resonance_j: E_res,
                ratio_to_landauer: ratio,
                scalePRT_m: scalePRT,
                scalePRT_nm: scalePRT * 1e9,
                equivalent_bit_length_m: scalePRT * log2_3,
                equivalent_bit_length_nm: scalePRT * 1e9 * log2_3
            };
        }
        console.log('   Scale Matrix built with ' + Object.keys(this.scaleMatrix).length + ' entries');
        const sample = this.scaleMatrix[41700];
        console.log('   Sample (41700 Hz): ' + sample.scalePRT_m.toExponential(4) + ' m');
    }

    computeScalePRT(fwhm_hz, temp_k = 300, wavelength_nm = 780) {
        const kB = 1.380649e-23;
        const h = 6.62607015e-34;
        const lambda = wavelength_nm * 1e-9;
        const log2_3 = Math.log2(3);
        const pi = Math.PI;

        if (fwhm_hz <= 0) {
            return { scalePRT_m: Infinity, ratio: Infinity, error: 'FWHM must be positive' };
        }

        const E_land = kB * temp_k * Math.log(2);
        const E_res = h * fwhm_hz;
        const ratio = E_land / E_res;
        const scalePRT = (lambda / (2 * pi)) * ratio / log2_3;

        return {
            scalePRT_m: scalePRT,
            scalePRT_nm: scalePRT * 1e9,
            ratio_to_landauer: ratio,
            energy_landauer_j: E_land,
            energy_resonance_j: E_res,
            energy_resonance_ev: E_res / 1.602176634e-19,
            fwhm_hz: fwhm_hz,
            temperature_k: temp_k,
            wavelength_m: lambda,
            equivalent_bit_length_m: scalePRT * log2_3,
            equivalent_bit_length_nm: scalePRT * 1e9 * log2_3
        };
    }

    getScaleMatrix() {
        return this.scaleMatrix;
    }

    // ================================================================
    // 4. CALCULATION MATRIX (Formulas)
    // ================================================================

    _buildCalculationMatrix() {
        this.calculationMatrix = {
            // Information capacity
            ternary_information_per_symbol: Math.log2(3), // 1.585 bits
            binary_to_ternary_gain_percent: (Math.log2(3) - 1) * 100, // 58.5%

            // Landauer limit
            landauer_limit_formula: 'E_landauer = k_B × T × ln(2)',
            landauer_limit_at_300K: 1.380649e-23 * 300 * Math.log(2),

            // ScalePRT formula
            scalePRT_formula: 'scalePRT = (lambda / 2π) × (E_landauer / E_resonance) / log₂(3)',

            // Density scaling
            density_scaling_formula: 'D_new = D_old × log₂(3) × N_modes × η × (B_total / R_s)',

            // Energy efficiency
            energy_per_bit_formula: 'E_bit = P_read / (R_s × log₂(3))',

            // Throughput
            throughput_formula: 'Throughput = N_grooves × R_s × log₂(3)',

            // ScalePRT to bit length
            bit_length_formula: 'L_bit = scalePRT × log₂(3)'
        };
        console.log('   Calculation Matrix built with ' + Object.keys(this.calculationMatrix).length + ' formulas');
    }

    getCalculationMatrix() {
        return this.calculationMatrix;
    }

    // ================================================================
    // 5. ENIGMA ROTOR
    // ================================================================

    _applyRotor(symbol, rotor, inverse) {
        return inverse ? rotor.indexOf(symbol) : rotor[symbol];
    }

    enigmaTransform(inputTrits, rotorConfig = null) {
        const rotors = rotorConfig ? rotorConfig.rotors : this.rotors;
        const reflector = rotorConfig ? rotorConfig.reflector : this.reflector;

        const cleaned = inputTrits.replace(/[^012]/g, '');
        if (cleaned.length === 0) return '';

        let positions = [0, 0, 0];
        let output = '';

        for (let ch of cleaned) {
            let val = parseInt(ch, 10);
            val = (val + positions[0]) % 3;
            val = this._applyRotor(val, rotors[0], false);
            val = this._applyRotor(val, rotors[1], false);
            val = this._applyRotor(val, rotors[2], false);
            val = reflector[val];
            val = this._applyRotor(val, rotors[2], true);
            val = this._applyRotor(val, rotors[1], true);
            val = this._applyRotor(val, rotors[0], true);
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

    // ================================================================
    // 6. LANGUAGE ASSEMBLY: Python ↔ Enigma ↔ Binary ↔ Ternary
    // ================================================================

    binaryToTernary(binaryString) {
        if (binaryString.length % 8 !== 0) {
            throw new Error('Binary string length must be multiple of 8');
        }
        let text = '';
        for (let i = 0; i < binaryString.length; i += 8) {
            const byte = binaryString.substr(i, 8);
            const code = parseInt(byte, 2);
            text += String.fromCharCode(code);
        }
        return this.textToTernary(text);
    }

    ternaryToBinary(ternaryString) {
        const text = this.ternaryToText(ternaryString);
        let binary = '';
        for (let i = 0; i < text.length; i++) {
            const code = text.charCodeAt(i);
            binary += code.toString(2).padStart(8, '0');
        }
        return binary;
    }

    pythonToTernary(pythonCode) {
        return this.textToTernary(pythonCode);
    }

    ternaryToPython(ternaryString) {
        return this.ternaryToText(ternaryString);
    }

    pythonToBinary(pythonCode) {
        let binary = '';
        for (let i = 0; i < pythonCode.length; i++) {
            const code = pythonCode.charCodeAt(i);
            binary += code.toString(2).padStart(8, '0');
        }
        return binary;
    }

    binaryToPython(binaryString) {
        if (binaryString.length % 8 !== 0) {
            throw new Error('Binary length must be multiple of 8');
        }
        let text = '';
        for (let i = 0; i < binaryString.length; i += 8) {
            const byte = binaryString.substr(i, 8);
            text += String.fromCharCode(parseInt(byte, 2));
        }
        return text;
    }

    // ================================================================
    // 7. UTILITY
    // ================================================================

    _printSampleMappings() {
        console.log('\n   Sample ASCII to Ternary mappings:');
        const samples = ['A', 'B', 'C', ' ', '0', '1', '2', 'a', 'b', 'c', 'z'];
        for (const char of samples) {
            const trits = this.asciiToTernary[char];
            console.log(`      ${char} -> ${trits}`);
        }
        console.log('');
    }

    getSystemStatus() {
        return {
            ascii_library_size: Object.keys(this.asciiToTernary).length,
            ternary_to_ascii_size: Object.keys(this.ternaryToAscii).length,
            resonance_entries: this.resonanceDatabase.length,
            energy_matrix_entries: Object.keys(this.energyConsumptionMatrix).length,
            scale_matrix_entries: Object.keys(this.scaleMatrix).length,
            calculation_matrix_entries: Object.keys(this.calculationMatrix).length,
            status: 'operational',
            version: '1.0',
            rotors: this.rotors,
            reflector: this.reflector
        };
    }

    // Get complete ASCII table for export
    getAsciiTable() {
        return this.asciiToTernary;
    }

    getTernaryTable() {
        return this.ternaryToAscii;
    }

    // Get complete energy consumption matrix
    getEnergyMatrix() {
        return this.energyConsumptionMatrix;
    }
}

// Create global instance
const engine = new VoiceOfBrahmaEngine();

// Export for Node.js
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { VoiceOfBrahmaEngine, engine };
}
