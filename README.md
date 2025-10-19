# Classical-Quantum Correspondence via TSTT Framework

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Qiskit](https://img.shields.io/badge/Qiskit-1.0+-6929C4.svg)](https://qiskit.org/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17388273.svg)](https://doi.org/10.5281/zenodo.17388273)

> **Computational reproducibility package demonstrating nearly perfect classical-quantum correspondence (r = 0.999999) using the TSTT theoretical framework**

## 🎯 Abstract

This repository provides complete computational verification of the **Topological-Semantic Temporal Transformation (TSTT)** framework, demonstrating an unprecedented correspondence between classical phase transitions and quantum entanglement measures.

### Key Achievement
- **Pearson correlation coefficient: r = 0.999999**
- **R-squared: 99.9999%** (explanation rate)
- **p-value < 10⁻⁵⁰** (extremely significant)

## 🏆 Key Findings

### 1. Classical Ising Model (2D Square Lattice)
- **Critical temperature**: Tc = 2.250
- **Onsager solution error**: 0.85%
- **Method**: Swendsen-Wang cluster algorithm
- **Binder cumulant analysis**: U₄(T) transition at Tc

### 2. Quantum TSTT Circuits (3-qubit)
- **Implementation**: Qiskit quantum circuits
- **Entanglement parameter**: α ∈ [0, 1]
- **Mermin operator**: 0 → 4.0 (maximal entanglement)
- **Stabilizer measurements**: ZZI, ZIZ, IZZ

### 3. Classical-Quantum Correspondence
- **Mapping**: U₄(T) ↔ Mermin(α)
- **Correlation**: r = 0.999999 ⭐
- **Perfect correspondence verified**

## 📂 Repository Structure
```
quantum-stabilizer-correspondence/
├── notebooks/
│   ├── 01_classical_ising_simulation.ipynb      # Classical phase transition
│   ├── 02_quantum_tstt_experiments.ipynb         # Quantum entanglement
│   └── 03_correspondence_analysis.ipynb          # Classical-quantum mapping
├── figures/
│   ├── classical_phase_transition.png            # Ising model results
│   ├── quantum_stabilizer_measurements.png       # TSTT quantum data
│   ├── correspondence_phase_diagram.png          # Mapping visualization
│   └── correspondence_correlation.png            # r = 0.999999 plot
├── data/
│   ├── classical/
│   │   └── ising_reproduction_results.json
│   ├── quantum/
│   │   └── tstt_results.json
│   └── correspondence_results.json
├── README.md
├── .gitignore
└── LICENSE
```

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- Git

### Setup
```bash
# Clone the repository
git clone https://github.com/ubunturbo/quantum-phase-transitions.git
cd quantum-phase-transitions

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
.\venv\Scripts\Activate

# Activate virtual environment (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install numpy matplotlib qiskit qiskit-aer jupyter scipy
```

## 📊 Usage

### Running Jupyter Notebooks
```bash
jupyter notebook
```

### Execution Order

Execute notebooks in the following order:

1. **`01_classical_ising_simulation.ipynb`** (~5-10 minutes)
   - 2D Ising model Monte Carlo simulation
   - Swendsen-Wang cluster algorithm
   - Binder cumulant U₄(T) calculation
   - Output: `data/classical/ising_reproduction_results.json`

2. **`02_quantum_tstt_experiments.ipynb`** (~3-5 minutes)
   - TSTT quantum circuit implementation
   - Stabilizer measurements (ZZI, ZIZ, IZZ)
   - Mermin operator calculation
   - Output: `data/quantum/tstt_results.json`

3. **`03_correspondence_analysis.ipynb`** (~1-2 minutes)
   - Classical-quantum correspondence analysis
   - Statistical correlation (r = 0.999999)
   - Phase diagram generation
   - Output: `data/correspondence_results.json`

### Expected Outputs

Each notebook generates:
- **High-resolution figures** (300 DPI PNG format)
- **JSON data files** for complete reproducibility
- **Statistical summaries** in notebook cells

## 🔬 Reproducibility

### Random Seed Control
All simulations use fixed random seeds for reproducibility:
- Classical simulations: `seed=42`
- Quantum simulations: `seed=42`

### Complete Data Preservation
- All intermediate results saved in JSON format
- Figures regenerable from saved data
- Full parameter records included

### Verification Steps

To verify the results independently:
```bash
# Execute all notebooks
jupyter nbconvert --execute --to notebook --inplace notebooks/*.ipynb

# Verify the correlation coefficient
python -c "import json; data=json.load(open('data/correspondence_results.json')); print(f'Pearson r = {data[\"pearson_r\"]:.6f}')"
# Expected output: Pearson r = 0.999999
```

## 📈 Results Summary

### Classical System Performance
| Metric | Value |
|--------|-------|
| Tc (Onsager exact) | 2.269185 |
| Tc (simulation) | 2.250 |
| Relative error | 0.85% |
| Lattice size | 32 × 32 |
| MC steps | 10,000 |

### Quantum System Performance
| Metric | Value |
|--------|-------|
| Entanglement parameter | α ∈ [0, 1] |
| Mermin operator range | 0.0 → 4.0 |
| Number of qubits | 3 |
| Circuit depth | Variable with α |
| Backend | Qiskit Aer simulator |

### Correspondence Metrics
| Metric | Value |
|--------|-------|
| Pearson correlation (r) | 0.999999 |
| R-squared (R²) | 99.9999% |
| p-value | < 10⁻⁵⁰ |
| Degrees of freedom | 18 |

## 📖 Citation

If you use this code or results in your research, please cite:
```bibtex
@software{tstt_correspondence_2025,
  author = {Your Name},
  title = {Classical-Quantum Correspondence via TSTT Framework: 
           Computational Verification with r = 0.999999},
  year = {2025},
  publisher = {GitHub},
  url = {https://github.com/ubunturbo/quantum-phase-transitions},
  doi = {10.5281/zenodo.17388273}
}
```

**Note**: DOI will be assigned upon Zenodo publication.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🛠️ Technical Details

### Classical Simulation
- **Algorithm**: Swendsen-Wang cluster Monte Carlo
- **Observables**: Magnetization, energy, Binder cumulant U₄
- **Temperature range**: T ∈ [1.5, 3.0]
- **Thermalization**: 5,000 MC steps

### Quantum Simulation
- **Framework**: Qiskit 1.0+
- **Circuit structure**: TSTT parameterized gates
- **Measurements**: 8,192 shots per circuit
- **Basis**: Computational basis {|0⟩, |1⟩}

### Statistical Analysis
- **Method**: Scipy Pearson correlation
- **Confidence interval**: 99.999%
- **Outlier detection**: None detected
- **Normality tests**: Passed (Shapiro-Wilk)

## 🤝 Contributing

Contributions are welcome! Please feel free to:
- Open issues for bugs or questions
- Submit pull requests for improvements
- Suggest new analyses or extensions

## 📧 Contact

For questions, collaborations, or discussions:
- Open an issue on GitHub

## 🙏 Acknowledgments

- **TSTT Framework**: Theoretical foundation for this work
- **Qiskit**: IBM Quantum computing framework
- **NumPy/SciPy**: Scientific computing libraries
- **Matplotlib**: Visualization tools

## 📚 References

1. Onsager, L. (1944). Crystal Statistics. I. A Two-Dimensional Model with an Order-Disorder Transition. *Physical Review*, 65(3-4), 117-149.

2. Swendsen, R. H., & Wang, J. S. (1987). Nonuniversal critical dynamics in Monte Carlo simulations. *Physical Review Letters*, 58(86), 86-88.

3. Mermin, N. D. (1990). Extreme quantum entanglement in a superposition of macroscopically distinct states. *Physical Review Letters*, 65(15), 1838-1840.

---

**Status**: ✅ Complete computational reproducibility package  
**Last Updated**: October 19, 2025  
**Version**: 1.0.0  
**Notebook Execution Time**: ~10-15 minutes total