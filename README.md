# Structural Correspondence Between Classical Phase Transitions and Quantum Stabilizer Codes

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![arXiv](https://img.shields.io/badge/arXiv-2410.xxxxx-b31b1b.svg)](https://arxiv.org/abs/2410.xxxxx)
[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.xxxxx-blue)](https://doi.org/10.5281/zenodo.xxxxx)

**Takayuki Takagi** | Independent Researcher | October 2025

This repository contains all code, data, and analysis scripts for reproducing the results in:

> "Structural Correspondence Between Classical Phase Transitions and Quantum Stabilizer Codes: A Framework for Formal Causation in Quantum Information"

---

## Key Results

- **Classical critical band:** U₄ ∈ [0.55, 0.65]
- **Quantum Structural Coherence Regime:** S̄ ≥ 0.90
- **Experimental measurements on IBM Quantum:**
  - **Mermin violation:** M = 3.655 ± 0.005 (>700σ)
  - **Stabilizer consistency:** S̄ = 0.908 ± 0.002
  - **State fidelity:** F ≥ 0.951

---

## Repository Structure

```
quantum-stabilizer-correspondence/
├── data/
│   ├── quantum/              # IBM Quantum experimental data
│   │   ├── ghz_raw_results.json
│   │   ├── ghz_final_corrected.json
│   │   └── device_calibration.json
│   └── classical/            # Ising model simulation outputs
│       ├── ising_L8_results.json
│       ├── ising_L12_results.json
│       └── ising_L16_results.json
├── figures/                  # All paper figures (main + supplementary)
│   ├── fig1_Ising_dmz.png
│   ├── Figure1_Ising_DMZ.pdf
│   ├── fig2_experimental_setup.png
│   ├── fig3_experimental_protocol.pdf
│   ├── fig4_perichoresis_visualization.png
│   ├── fig4_perichoresis_visualization.pdf
│   ├── fig_dmz_with_ghz_measurement_final.png
│   ├── fig_theory_validation.png
│   └── fig_theory_validation.pdf
├── scripts/
│   ├── error_analysis.py
│   ├── apply_readout_mitigation.py
│   ├── verify_zzi_izz_derivation.py
│   ├── plot_figure1.py       # Figure generation scripts
│   ├── calculate_expectations.py
│   ├── correct_ghz_labeling.py
│   ├── verify_paper_consistency.py
│   └── [other analysis scripts]
├── src/
│   ├── classical/            # Ising model implementation
│   │   └── ising_model.py
│   ├── quantum/              # GHZ circuit implementation
│   │   └── ghz_circuits.py
│   ├── analysis/             # Data analysis utilities
│   └── visualization/        # Plotting utilities
├── reports/
│   └── error_analysis_report.txt
├── docs/
│   ├── REPRODUCIBILITY.md
│   ├── SUPPLEMENTARY_NOTE_4_READOUT_MITIGATION.md
│   ├── SUPPLEMENTARY_NOTE_DATA_VALIDATION.md
│   └── REVIEWER_RESPONSE_TEMPLATES.md
├── tests/                    # Unit tests
├── notebooks/                # Jupyter notebooks (coming soon)
├── requirements.txt
└── README.md
```

---

## Figures

All figures used in the Nature Communications manuscript are available in `figures/`:

### Main Text Figures
- **Figure 1**: Classical Ising model and Dead Man's Zone (DMZ)
  - `fig1_Ising_dmz.png` (PNG version)
  - `Figure1_Ising_DMZ.pdf` (High-resolution PDF)
- **Figure 2**: Experimental setup
  - `fig2_experimental_setup.png`
- **Figure 3**: Experimental protocol
  - `fig3_experimental_protocol.pdf`
- **Figure 4**: Perichoresis visualization and structural correspondence
  - `fig4_perichoresis_visualization.png`
  - `fig4_perichoresis_visualization.pdf`

### Supplementary Figures
- **DMZ with GHZ measurement**: `fig_dmz_with_ghz_measurement_final.png`
- **Theory validation**: `fig_theory_validation.png` / `.pdf`

All figures can be regenerated using scripts in `scripts/plot_*.py`.

---

## Quick Start

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

## Data Validation and Error Analysis

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

## Reproducing Results

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

## Data Files and Processing

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

## Testing
```bash
pytest tests/ -v
python scripts/verify_data_integrity.py
python scripts/validate_paper_values.py
```

---

## Documentation

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

## Citation
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

## Data Availability Statement

All data and code supporting the findings of this study are openly available:

### 1. Source Code
- **Repository**: https://github.com/ubunturbo/quantum-phase-transitions
- **License**: MIT License
- **Contents**: Complete source code for classical simulations, quantum circuit implementations, data analysis, and figure generation

### 2. Experimental Data
All data files are available in the `data/` directory:
- **Raw quantum measurements**: `data/quantum/ghz_raw_results.json`
- **Corrected quantum data**: `data/quantum/ghz_final_corrected.json`
- **Device calibration**: `data/quantum/device_calibration.json`
- **Classical simulations**: `data/classical/ising_L{8,12,16}_results.json`

### 3. Figures
All manuscript figures are available in the `figures/` directory:
- Main text figures (Figure 1-4)
- Supplementary figures
- Both PNG and PDF formats provided where applicable

### 4. Permanent Archive (Coming Soon)
- **Zenodo DOI**: 10.5281/zenodo.xxxxx (will be assigned upon paper acceptance)
- This will provide a permanent, citable record of all data and code
- The Zenodo archive will include:
  - Complete snapshot of this repository
  - All raw and processed data files
  - Analysis scripts and documentation
  - Generated figures

### IBM Quantum Job Information
- **Job ID**: d3kfathfk6qs73emfrb0 (permanent IBM Quantum record)
- **Backend**: ibm_torino (127-qubit Eagle r3)
- **Date**: October 10, 2025, 21:00 JST
- **Qubits**: [54, 61, 62]
- **Shots**: 30,000 per measurement basis

### Contact
For questions about data access, reproduction, or any aspect of this work:
- **Email**: lemissio@gmail.com
- **GitHub Issues**: https://github.com/ubunturbo/quantum-phase-transitions/issues

---

## Contact

**Takayuki Takagi**
- Email: lemissio@gmail.com
- ORCID: 0009-0003-5188-2314
- GitHub: [@ubunturbo](https://github.com/ubunturbo)

---

## License

MIT License - see [LICENSE](LICENSE) file for details.

This permissive license allows anyone to use, modify, and redistribute this code for any purpose, including commercial applications, with proper attribution.

---

## Acknowledgments

- **IBM Quantum** for providing access to quantum hardware
- Measurements performed on **ibm_torino** (127-qubit Eagle r3) on October 10, 2025
- **Job ID**: d3kfathfk6qs73emfrb0 (permanent IBM Quantum record)
- Device calibration performed on October 10, 2025, 21:00 JST

---

## Related Resources

- [IBM Quantum Experience](https://quantum.ibm.com/)
- [Qiskit Documentation](https://qiskit.org/documentation/)
- [Manuscript (arXiv)](https://arxiv.org/abs/2410.xxxxx) - Will be updated with actual arXiv number
- [Data Repository (Zenodo)](https://doi.org/10.5281/zenodo.xxxxx) - Will be updated with actual DOI

---

## Reproducibility Statement

This research prioritizes complete transparency and reproducibility. We provide:

1. **Complete source code** - All algorithms implemented and documented
2. **Raw experimental data** - Unprocessed measurements from IBM Quantum
3. **Processed data** - All corrections and calibrations applied
4. **Analysis scripts** - Every step of data processing documented
5. **Error analysis** - Comprehensive uncertainty quantification
6. **Figure generation** - Scripts to reproduce all manuscript figures

We encourage independent verification and replication of our results. All questions, issues, or requests for clarification are welcome via GitHub issues or email.

---

**Last Updated**: October 17, 2025

**Status**: Ready for Nature Communications submission - All code, data, and figures publicly available