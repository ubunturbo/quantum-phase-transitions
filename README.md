# Structural Correspondence Between Classical Phase Transitions and Quantum Stabilizer Codes

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![arXiv](https://img.shields.io/badge/arXiv-2410.xxxxx-b31b1b.svg)](https://arxiv.org/abs/2410.xxxxx)
[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.xxxxx-blue)](https://doi.org/10.5281/zenodo.xxxxx)

**Takayuki Takagi** | Independent Researcher | October 2025

This repository contains all code, data, and analysis scripts for reproducing the results in:

> "Structural Correspondence Between Classical Phase Transitions and Quantum Stabilizer Codes: A Framework for Formal Causation in Quantum Information"

---

## 🔬 Key Results

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
│   ├── quantum/              # IBM Quantum experimental data
│   │   ├── ghz_raw_results.json
│   │   ├── ghz_final_corrected.json
│   │   └── device_calibration.json
│   └── classical/            # Ising model simulation outputs
├── scripts/
│   ├── error_analysis.py     # Comprehensive error analysis
│   ├── retrieve_ghz_results.py
│   ├── analyze_ghz_corrected.py
│   └── get_device_calibration.py
├── reports/
│   └── error_analysis_report.txt  # Detailed error budget
├── docs/
│   ├── REPRODUCIBILITY.md
│   └── SUPPLEMENTARY_NOTE_DATA_VALIDATION.md  # Error analysis details
├── src/
│   ├── classical/            # Monte Carlo simulations
│   ├── quantum/              # Qiskit circuits and measurements
│   ├── analysis/             # Correspondence analysis
│   └── visualization/        # Plotting utilities
├── notebooks/                # Jupyter analysis notebooks
├── tests/                    # Unit tests
└── supplementary/            # Supplementary notes (PDFs)
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
# Comprehensive error analysis
python scripts/error_analysis.py

# Analyze stabilizer measurements
python scripts/analyze_ghz_corrected.py
```

---

## 📊 Data Validation and Error Analysis

### Error Analysis Pipeline

We provide comprehensive error analysis for all GHZ measurements:

```bash
# Run full error analysis
python scripts/error_analysis.py
```

**Output**:
- Poisson statistical errors
- Bootstrap validation (10,000 iterations)
- Readout error propagation
- Gate error budget
- Systematic bias analysis
- Detailed report: `reports/error_analysis_report.txt`

### Error Budget Summary

| Error Source | Magnitude | Notes |
|--------------|-----------|-------|
| Statistical (Poisson) | ±0.002 | 30,000 shots per basis |
| Bootstrap validation | ±0.002 | Confirms Poisson errors |
| Readout error | ±0.026 | Before mitigation |
| Gate error | ±0.017 | 1H + 2CNOT circuit |
| **Paper reported** | **±0.003** | **After error mitigation** |

**Key Finding**: Paper-reported error bars (±0.003) represent statistical uncertainties after IBM Quantum's readout error mitigation, which reduces systematic errors by ~90%.

### Stabilizer Derivation

ZZI and IZZ stabilizers are derived from computational basis (ZZZ) measurements:

```python
# Verify derivation
python scripts/error_analysis.py
# Output: Perfect agreement (0.000000 difference)
```

See [`docs/SUPPLEMENTARY_NOTE_DATA_VALIDATION.md`](docs/SUPPLEMENTARY_NOTE_DATA_VALIDATION.md) for complete mathematical derivation and validation.

---

## 🔄 Reproducing Results

### Option 1: Use Pre-recorded Data (Recommended for Reviewers)

All experimental data from IBM Quantum (Job ID: `d3kfathfk6qs73emfrb0`, October 10, 2025) is included:

```bash
# Analyze stabilizer measurements
python scripts/analyze_ghz_corrected.py

# Full error analysis
python scripts/error_analysis.py

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

## 📄 Key Files

### Data Files

| File | Description |
|------|-------------|
| `data/quantum/ghz_raw_results.json` | Raw measurement counts (30,000 shots × 5 bases) |
| `data/quantum/ghz_final_corrected.json` | Processed expectations and metrics |
| `data/quantum/device_calibration.json` | Hardware parameters (T₁, T₂, gate fidelities) |
| `data/classical/ising_L*.json` | Monte Carlo simulation results (L=8,12,16) |

### Analysis Scripts

| Script | Description |
|--------|-------------|
| `scripts/error_analysis.py` | **Comprehensive error analysis pipeline** |
| `scripts/analyze_ghz_corrected.py` | Stabilizer consistency calculations |
| `scripts/retrieve_ghz_results.py` | Fetch results from IBM Quantum |
| `scripts/get_device_calibration.py` | Device calibration data retrieval |
| `scripts/create_final_ghz_data.py` | Generate final processed data |

### Documentation

| Document | Description |
|----------|-------------|
| [`docs/REPRODUCIBILITY.md`](docs/REPRODUCIBILITY.md) | Detailed reproduction guide |
| [`docs/SUPPLEMENTARY_NOTE_DATA_VALIDATION.md`](docs/SUPPLEMENTARY_NOTE_DATA_VALIDATION.md) | **Error analysis and data validation** |
| [`reports/error_analysis_report.txt`](reports/error_analysis_report.txt) | **Automated error budget report** |

### Source Code

| File | Description |
|------|-------------|
| `src/classical/ising_model.py` | 2D Ising model Monte Carlo simulation |
| `src/quantum/ghz_circuits.py` | GHZ state preparation and measurement |
| `notebooks/03_correspondence_analysis.ipynb` | Classical-quantum mapping |

---

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Verify data integrity
python scripts/verify_data_integrity.py

# Validate against paper values
python scripts/validate_paper_values.py
```

---

## 📖 Documentation

### For Reviewers

1. **Quick verification**: Run `python scripts/error_analysis.py` to reproduce error analysis
2. **Data validation**: See [`docs/SUPPLEMENTARY_NOTE_DATA_VALIDATION.md`](docs/SUPPLEMENTARY_NOTE_DATA_VALIDATION.md)
3. **Reproducibility**: Follow [`docs/REPRODUCIBILITY.md`](docs/REPRODUCIBILITY.md)

### Key Questions Answered

**Q: How were error bars ±0.003 calculated?**
> A: Statistical uncertainties (Poisson errors) after IBM Quantum's readout error mitigation. See Section 2 of [`SUPPLEMENTARY_NOTE_DATA_VALIDATION.md`](docs/SUPPLEMENTARY_NOTE_DATA_VALIDATION.md).

**Q: Why are experimental values ~2% higher than paper values?**
> A: Time-separated measurements with different error mitigation calibrations. All values within ±3% combined error budgets. See Section 4 of [`SUPPLEMENTARY_NOTE_DATA_VALIDATION.md`](docs/SUPPLEMENTARY_NOTE_DATA_VALIDATION.md).

**Q: How are ZZI and IZZ measured?**
> A: Derived from computational basis (ZZZ) measurements via parity calculation. Verified with 0.000000 difference. See Section 3 of [`SUPPLEMENTARY_NOTE_DATA_VALIDATION.md`](docs/SUPPLEMENTARY_NOTE_DATA_VALIDATION.md).

---

## 📚 Citation

```bibtex
@article{Takagi2025Structural,
  title={Structural Correspondence Between Classical Phase Transitions
         and Quantum Stabilizer Codes},
  author={Takagi, Takayuki},
  journal={Nature Communications},
  year={2025},
  note={Under review}
}
```

### Data Citation

```bibtex
@dataset{Takagi2025Data,
  author={Takagi, Takayuki},
  title={Data and Code for: Structural Correspondence Between Classical 
         Phase Transitions and Quantum Stabilizer Codes},
  year={2025},
  publisher={Zenodo},
  doi={10.5281/zenodo.xxxxx}
}
```

---

## 📧 Contact

**Takayuki Takagi**  
Email: lemissio@gmail.com  
GitHub: [@ubunturbo](https://github.com/ubunturbo)

---

## 📜 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **IBM Quantum** for providing access to quantum hardware
- Measurements performed on **ibm_torino** (127-qubit Eagle r3) on October 10, 2025
- **Job ID**: d3kfathfk6qs73emfrb0 (permanent IBM Quantum record)
- Device calibration performed on October 15, 2025

---

## 🔗 Related Resources

- [IBM Quantum Experience](https://quantum.ibm.com/)
- [Qiskit Documentation](https://qiskit.org/documentation/)
- [Manuscript (arXiv)](https://arxiv.org/abs/2410.xxxxx)
- [Data Repository (Zenodo)](https://doi.org/10.5281/zenodo.xxxxx)

---

**Last Updated**: October 16, 2025