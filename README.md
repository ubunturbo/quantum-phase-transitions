# Structural Correspondence Between Classical Phase Transitions and Quantum Stabilizer Codes

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![arXiv](https://img.shields.io/badge/arXiv-2410.xxxxx-b31b1b.svg)](https://arxiv.org/abs/2410.xxxxx)

**Takayuki Takagi** | Independent Researcher | October 2025

This repository contains all code, data, and analysis scripts for reproducing the results in:

> "Structural Correspondence Between Classical Phase Transitions and Quantum Stabilizer Codes: A Framework for Formal Causation in Quantum Information"

---

## 🎯 Key Results

- **Classical critical band:** U₄ ∈ [0.55, 0.65]
- **Quantum Structural Coherence Regime:** S̄ ≥ 0.90
- **Experimental measurements on IBM Quantum:**
  - **Mermin violation:** M = 3.655 ± 0.005 (>700σ)
  - **Stabilizer consistency:** S̄ = 0.908 ± 0.002
  - **State fidelity:** F ≥ 0.951

---

## 📁 Repository Structure

```
quantum-stabilizer-correspondence/
├── data/
│   ├── raw/              # IBM Quantum raw measurement data
│   ├── processed/        # Processed analysis results
│   └── classical/        # Ising model simulation outputs
├── src/
│   ├── classical/        # Monte Carlo simulations
│   ├── quantum/          # Qiskit circuits and measurements
│   ├── analysis/         # Correspondence analysis
│   └── visualization/    # Plotting utilities
├── notebooks/            # Jupyter analysis notebooks
├── scripts/              # Standalone execution scripts
├── tests/                # Unit tests
├── supplementary/        # Supplementary notes (PDFs)
└── docs/                 # Documentation
```

---

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/ubunturbo/quantum-stabilizer-correspondence.git
cd quantum-stabilizer-correspondence

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Run Classical Simulations

```bash
python scripts/run_ising_simulation.py --sizes 8 12 16 --n_temps 50
```

### Analyze Quantum Data (using pre-recorded measurements)

```bash
python scripts/analyze_quantum_results.py --data data/raw/
```

---

## 📊 Reproducing Results

### Option 1: Use Pre-recorded Data (Recommended for Reviewers)

All experimental data from IBM Quantum (October 10, 2025) is included:

```bash
# Analyze stabilizer measurements
python notebooks/02_quantum_experiments.ipynb

# Generate all figures
python scripts/generate_all_figures.py
```

### Option 2: Re-run Quantum Experiments

**Requires IBM Quantum account:**

```bash
# Configure credentials
export QISKIT_IBM_TOKEN="YOUR_TOKEN"

# Run experiments
python src/quantum/ghz_circuits.py --backend ibm_torino --shots 30000
```

**Note:** Queue time typically 2-6 hours.

---

## 📈 Key Files

| File | Description |
|------|-------------|
| `src/classical/ising_model.py` | 2D Ising model Monte Carlo simulation |
| `src/quantum/ghz_circuits.py` | GHZ state preparation and measurement |
| `data/raw/ghz_*_shots.json` | Raw IBM Quantum measurement data |
| `notebooks/03_correspondence_analysis.ipynb` | Classical-quantum mapping |
| `docs/REPRODUCIBILITY.md` | Detailed reproduction guide |

---

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Verify data integrity
python scripts/verify_data_integrity.py
```

---

## 📖 Citation

```bibtex
@article{Takagi2025Structural,
  title={Structural Correspondence Between Classical Phase Transitions 
         and Quantum Stabilizer Codes},
  author={Takagi, Takayuki},
  journal={arXiv preprint arXiv:2410.xxxxx},
  year={2025}
}
```

---

## 📧 Contact

**Takayuki Takagi**  
Email: lemissio@gmail.com

---

## 📜 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- IBM Quantum for providing access to quantum hardware
- Measurements performed on ibm_torino (127-qubit Eagle r3) on October 10, 2025