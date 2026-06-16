# U‑Bottom Groove Reader – Hardware Concept

## Principle

A U‑bottom groove on an optical disc acts as a coupled resonator. By measuring the reflected intensity vs. frequency (or vs. radial position), we recover the amplitude contributions of the three modes (left wall, bottom, right wall). These amplitudes correspond to ternary symbols.

## Components

| Component | Specification |
|-----------|---------------|
| Laser diode | 780 nm (CD), 405 nm (Blu‑ray) |
| Tunable | 1–100 MHz modulation |
| Photodetector | Fast PIN diode, >100 MHz bandwidth |
| ADC | 12‑bit, 200 MS/s |
| FPGA/µC | Real‑time FFT, threshold decision |
| Actuator | Radial positioning (50 nm precision) |

## Block Diagram
