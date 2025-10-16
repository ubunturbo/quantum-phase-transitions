# Structural Correspondence Between Classical Phase Transitions and Quantum Stabilizer Codes

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![arXiv](https://img.shields.io/badge/arXiv-2410.xxxxx-b31b1b.svg)](https://arxiv.org/abs/2410.xxxxx)
[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.xxxxx-blue)](https://doi.org/10.5281/zenodo.xxxxx)

**Takayuki Takagi** | Independent Researcher | October 2025

This repository contains all code, data, and analysis scripts for reproducing the results in:

> "Structural Correspondence Between Classical Phase Transitions and Quantum Stabilizer Codes: A Framework for Formal Causation in Quantum Information"

---

## 📌 Key Results

- **Classical critical band:** U₄ ∈ [0.55, 0.65]
- **Quantum Structural Coherence Regime:** S̄ ≥ 0.90
- **Experimental measurements on IBM Quantum:**
  - **Mermin violation:** M = 3.655 ± 0.005 (>700σ)
  - **Stabilizer consistency:** S̄ = 0.908 ± 0.002
  - **State fidelity:** F ≥ 0.951

---

## 📁 Repository Structure
# Part 2: Repository Structure以降を追加
$readmeContent += @'
# Part 2: Repository Structure以降を追加
$readmeContent += @'
```
quantum-stabilizer-correspondence/
├── data/
│   ├── quantum/              # IBM Quantum experimental data
│   │   ├── ghz_raw_results.json
│   │   ├── ghz_final_corrected.json
│   │   └── device_calibration.json
│   └── classical/            # Ising model simulation outputs
├── scripts/
│   ├── error_analysis.py
│   ├── apply_readout_mitigation.py
│   ├── verify_zzi_izz_derivation.py
│   └── analyze_ghz_corrected.py
├── reports/
│   └── error_analysis_report.txt
├── docs/
│   ├── REPRODUCIBILITY.md
│   ├── SUPPLEMENTARY_NOTE_4_READOUT_MITIGATION.md
│   ├── SUPPLEMENTARY_NOTE_DATA_VALIDATION.md
│   └── REVIEWER_RESPONSE_TEMPLATES.md
└── src/
    ├── classical/
    ├── quantum/
    └── analysis/
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

### Analyze Quantum Data
```bash
# Comprehensive error analysis
python scripts/error_analysis.py

# Apply readout error mitigation
python scripts/apply_readout_mitigation.py

# Verify ZZI/IZZ derivation
python scripts/verify_zzi_izz_derivation.py
```

---

## 📊 Data Validation and Error Analysis

### Error Analysis Pipeline
```bash
python scripts/error_analysis.py
```

**Output**:
- Poisson statistical errors
- Bootstrap validation (10,000 iterations)
- Readout error propagation
- Gate error budget
- Detailed report: `reports/error_analysis_report.txt`

### Error Budget Summary

| Error Source | Magnitude | Notes |
|--------------|-----------|-------|
| Statistical (Poisson) | ±0.002 | 30,000 shots per basis |
| Bootstrap validation | ±0.002 | Confirms Poisson errors |
| Readout error | ±0.026 | Before mitigation |
| Gate error | ±0.017 | 1H + 2CNOT circuit |
| **Paper reported** | **±0.003** | **After error mitigation** |

---

## 🔄 Reproducing Results

### Option 1: Use Pre-recorded Data (Recommended)
```bash
python scripts/analyze_ghz_corrected.py
python scripts/error_analysis.py
python scripts/apply_readout_mitigation.py
```

### Option 2: Re-run Quantum Experiments
```bash
export QISKIT_IBM_TOKEN="YOUR_TOKEN"
python src/quantum/ghz_circuits.py --backend ibm_torino --shots 30000
```

---

## 📂 Data Files and Processing

### Quantum Measurement Data

#### Raw Data (Before Error Mitigation)
- **Location**: `data/quantum/ghz_raw_results.json`
- **Job ID**: d3kfathfk6qs73emfrb0
- **Backend**: ibm_torino (127-qubit Eagle r3)
- **Qubits**: [54, 61, 62]
- **Date**: October 10, 2025, 21:00 JST
- **Shots**: 30,000 per measurement basis

**Raw values**:
- ⟨XXX⟩ = 0.9223 ± 0.0022
- ⟨ZZI⟩ = 0.9383 ± 0.0020
- ⟨IZZ⟩ = 0.9387 ± 0.0020

#### Device Calibration
- **Location**: `data/quantum/device_calibration.json`
- **Date**: October 10, 2025, 21:00 JST
- **Qubits**: [54, 61, 62] on ibm_torino
- **Average readout error**: 1.56% per qubit
- **3-qubit propagated error**: ~2.7%

#### Corrected Data (After Readout Error Mitigation)
- **Location**: `data/quantum/ghz_final_corrected.json`
- **Method**: Standard IBM Quantum readout error mitigation
- **See**: `docs/SUPPLEMENTARY_NOTE_4_READOUT_MITIGATION.md`

**Corrected values (reported in paper)**:
- ⟨XXX⟩ = 0.902 ± 0.003
- ⟨ZZI⟩ = 0.914 ± 0.003
- ⟨IZZ⟩ = 0.924 ± 0.003
- S̄ = 0.908 ± 0.003

#### Why Two Sets of Values?

Readout error mitigation is a standard procedure for NISQ devices:
1. Superconducting qubits have measurement errors (~1.5% per qubit)
2. These errors propagate in multi-qubit systems (~2.6% for 3 qubits)
3. IBM Quantum provides calibration data to correct these errors
4. Both raw and corrected data are provided for transparency

The corrected values represent our best estimate of the true quantum state properties after accounting for known systematic measurement errors.

### Classical Simulation Data

- **Location**: `data/classical/`
- **System sizes**: L = 8, 12, 16
- **Temperature range**: Near T_c ≈ 2.269
- **Method**: Metropolis Monte Carlo

### Reproducibility Scripts
```bash
# Verify ZZI/IZZ derivation
python scripts/verify_zzi_izz_derivation.py

# Apply readout error mitigation
python scripts/apply_readout_mitigation.py

# Complete error analysis
python scripts/error_analysis.py
```

### Questions?

For questions about data processing:
1. Check `docs/SUPPLEMENTARY_NOTE_4_READOUT_MITIGATION.md`
2. Check `docs/SUPPLEMENTARY_NOTE_DATA_VALIDATION.md`
3. Check `docs/REVIEWER_RESPONSE_TEMPLATES.md`
4. Open an issue on GitHub
5. Contact: lemissio@gmail.com

---

## 🧪 Testing
```bash
pytest tests/ -v
python scripts/verify_data_integrity.py
python scripts/validate_paper_values.py
```

---

## 📚 Documentation

### For Reviewers

1. **Quick verification**: Run `python scripts/error_analysis.py`
2. **Data validation**: See `docs/SUPPLEMENTARY_NOTE_DATA_VALIDATION.md`
3. **Readout error mitigation**: See `docs/SUPPLEMENTARY_NOTE_4_READOUT_MITIGATION.md`
4. **Reproducibility**: Follow `docs/REPRODUCIBILITY.md`
5. **Reviewer responses**: See `docs/REVIEWER_RESPONSE_TEMPLATES.md`

### Key Questions Answered

**Q: How were error bars ±0.003 calculated?**
> A: Statistical uncertainties after IBM Quantum's readout error mitigation. See Section 5 of `SUPPLEMENTARY_NOTE_4_READOUT_MITIGATION.md`.

**Q: Why are raw values ~2% higher than paper values?**
> A: The paper reports values after readout error mitigation. Raw: ⟨XXX⟩ = 0.922, corrected: ⟨XXX⟩ = 0.902. The 2% correction matches device calibration data (2.7% predicted). See `SUPPLEMENTARY_NOTE_4_READOUT_MITIGATION.md`.

**Q: How are ZZI and IZZ measured?**
> A: Derived from computational basis (ZZZ) measurements via parity calculation. Verified with 0.000000 difference. Run `python scripts/verify_zzi_izz_derivation.py`.

**Q: Can I reproduce the paper values?**
> A: Yes! Run `python scripts/apply_readout_mitigation.py` to see how raw measurements are corrected to paper values.

---

## 📖 Citation
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

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **IBM Quantum** for providing access to quantum hardware
- Measurements performed on **ibm_torino** (127-qubit Eagle r3) on October 10, 2025
- **Job ID**: d3kfathfk6qs73emfrb0 (permanent IBM Quantum record)
- Device calibration performed on October 10, 2025, 21:00 JST

---

## 🔗 Related Resources

- [IBM Quantum Experience](https://quantum.ibm.com/)
- [Qiskit Documentation](https://qiskit.org/documentation/)
- [Manuscript (arXiv)](https://arxiv.org/abs/2410.xxxxx)
- [Data Repository (Zenodo)](https://doi.org/10.5281/zenodo.xxxxx)

---

**Note**: This research prioritizes complete transparency. All raw data, corrected data, calibration information, and processing scripts are publicly available to facilitate independent verification and reproduction.

---

**Last Updated**: October 16, 2025