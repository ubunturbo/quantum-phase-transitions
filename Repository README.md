# Structural Correspondence Between Classical Phase Transitions and Quantum Stabilizer Codes

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![arXiv](https://img.shields.io/badge/arXiv-2410.xxxxx-b31b1b.svg)](https://arxiv.org/abs/2410.xxxxx)

**Takayuki Takagi** | Independent Researcher | October 2025

This repository contains all code, data, and analysis scripts for reproducing the results in:

> "Structural Correspondence Between Classical Phase Transitions and Quantum Stabilizer Codes: A Framework for Formal Causation in Quantum Information"

---

## Abstract

We demonstrate a structural correspondence between classical phase transitions and quantum stabilizer codes through Monte Carlo simulations of the 2D Ising model and experimental verification using three-qubit GHZ states on IBM Quantum hardware. The correspondence emerges from an isomorphic relation between classical correlation length and quantum stabilizer coherence length.

**Key Results:**
- Classical critical band: **0.55 ≤ U₄ ≤ 0.65**
- Quantum Structural Coherence Regime: **S̄ ≥ 0.90**
- Experimental GHZ measurements: **S̄ = 0.908 ± 0.002**, **M = 3.655 ± 0.005** (>700σ), **F ≥ 0.951**

---

## Repository Structure

```
.
├── data/
│   ├── raw/                    # IBM Quantum raw measurement data
│   ├── processed/              # Processed analysis results
│   └── classical/              # Ising model simulation outputs
├── src/
│   ├── classical/              # Monte Carlo simulations
│   ├── quantum/                # Qiskit circuits and measurements
│   ├── analysis/               # Correspondence analysis
│   └── visualization/          # Plotting utilities
├── notebooks/                  # Jupyter analysis notebooks
├── scripts/                    # Standalone execution scripts
├── tests/                      # Unit tests
└── supplementary/              # Supplementary notes (PDFs)
```

---

## Installation

### Prerequisites

- Python 3.9+
- IBM Quantum account (for hardware experiments)

### Quick Setup

```bash
# Clone repository
git clone https://github.com/ubunturbo/quantum-stabilizer-correspondence.git
cd quantum-stabilizer-correspondence

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Or use conda
conda env create -f environment.yml
conda activate qstabilizer
```

### Required Packages

```
numpy>=1.24.0
scipy>=1.10.0
matplotlib>=3.7.0
qiskit>=1.0.0
qiskit-ibm-runtime>=0.15.0
pandas>=2.0.0
jupyter>=1.0.0
pytest>=7.4.0
```

---

## Reproducing Results

### 1. Classical Simulations (2D Ising Model)

Generate data for Figure 1:

```bash
python scripts/run_ising_simulation.py --sizes 8 12 16 --n_temps 50
```

This performs Monte Carlo simulations with:
- 8,000 measurement sweeps
- 1,000 thermalization sweeps
- Temperature range: T ∈ [1.8, 2.8]

**Expected runtime:** ~30 minutes (single CPU core)

**Output:** `data/classical/ising_L{8,12,16}_data.npz`

### 2. Quantum Experiments (IBM Quantum)

**Configure IBM Quantum credentials:**

```bash
export QISKIT_IBM_CHANNEL="ibm_quantum"
export QISKIT_IBM_TOKEN="YOUR_API_TOKEN"
```

**Run GHZ state experiments:**

```bash
python scripts/submit_quantum_jobs.py \
    --backend ibm_torino \
    --shots 30000 \
    --experiments stabilizer mermin
```

**Note for reviewers:** Pre-recorded experimental data from October 10, 2025 (ibm_torino, 127-qubit Eagle r3) is available in `data/raw/`. You can skip hardware execution and directly analyze these results.

**Expected queue time:** 2-6 hours (IBM Quantum)  
**Output:** `data/raw/ghz_*_shots.json`, `device_calibration.json`

### 3. Generate All Figures

```bash
python scripts/generate_all_figures.py
```

**Generates:**
- Figure 1: Critical behavior of 2D Ising model (three panels)
- Supplementary figures for correspondence analysis

**Output directory:** `figures/`

### 4. Interactive Analysis

Launch Jupyter notebooks for detailed exploration:

```bash
jupyter notebook notebooks/
```

**Recommended sequence:**
1. `01_classical_simulations.ipynb` - Ising model analysis
2. `02_quantum_experiments.ipynb` - GHZ state characterization
3. `03_correspondence_analysis.ipynb` - Classical-quantum mapping
4. `04_reproduce_figures.ipynb` - Publication-quality plots

---

## Key Files

### Data Files (in `data/raw/`)

| File | Description | Size |
|------|-------------|------|
| `ghz_xxx_shots.json` | XXX stabilizer measurement | ~500 KB |
| `ghz_zzi_shots.json` | ZZI stabilizer measurement | ~500 KB |
| `ghz_izz_shots.json` | IZZ stabilizer measurement | ~500 KB |
| `mermin_xyy_shots.json` | XYY Mermin basis | ~500 KB |
| `device_calibration.json` | IBM hardware calibration | ~50 KB |

### Processed Results

- `stabilizer_results.csv` - Aggregated stabilizer expectations
- `mermin_analysis.csv` - Mermin operator calculations
- `correspondence_metrics.csv` - U₄ vs S̄ correlation data

---

## Testing

Run unit tests to verify implementation correctness:

```bash
pytest tests/ -v
```

**Coverage:**
- `test_ising_model.py` - Verify Monte Carlo observables
- `test_stabilizers.py` - Check stabilizer expectation calculations
- `test_correspondence.py` - Validate structural metrics

---

## Citation

If you use this code or data, please cite:

```bibtex
@article{Takagi2025Structural,
  title={Structural Correspondence Between Classical Phase Transitions 
         and Quantum Stabilizer Codes: A Framework for Formal Causation 
         in Quantum Information},
  author={Takagi, Takayuki},
  journal={arXiv preprint arXiv:2410.xxxxx},
  year={2025}
}
```

---

## Reproducibility Statement

All experimental measurements were performed on **October 10, 2025** using IBM Quantum's **ibm_torino** device (127-qubit Eagle r3 processor). Device specifications at measurement time:

- **Gate errors:** CNOT ~8×10⁻³, single-qubit ~5×10⁻⁴
- **Coherence times:** T₁ ≈ 199 μs, T₂ ≈ 90 μs
- **Readout fidelity:** ~97.5%

Complete calibration data is stored in `data/raw/device_calibration.json`.

---

## Contact

**Takayuki Takagi**  
Independent Researcher  
Email: lemissio@gmail.com

---

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- IBM Quantum for providing access to quantum computing hardware
- The Qiskit development team for excellent documentation and support