# quantum-phase-transitions
Code for "Structural Correspondence Between Classical Phase Transitions and Quantum Stabilizer Codes" (Nature Communications submission)
markdown# Structural Correspondence Between Classical Phase Transitions and Quantum Stabilizer Codes

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## Manuscript Information

**Author:** Takayuki Takagi (Independent Researcher)  
**Journal:** Nature Communications  
**Manuscript ID:** NCOMMS-25-82293  
**Status:** Under Review  
**Submission Date:** October 14, 2025

## Abstract

Quantum error correction protocols rely on stabilizer codes to preserve coherence, yet the structural origins of this protection remain elusive. We demonstrate a correspondence between classical phase transitions and quantum stabilizer symmetries, revealing that both exhibit analogous regimes of order, criticality, and disorder.

Through Monte Carlo simulations of the 2D Ising model and experimental verification using three-qubit GHZ states on IBM Quantum hardware, we establish that the classical critical band—characterized by Binder cumulant values U₄ ∈ [0.55, 0.65]—maps structurally to quantum states with high stabilizer consistency (S̄ ≥ 0.90).

## Key Results

### Experimental Verification
- **Mermin Violations:** M = 3.655 ± 0.005 (exceeding 700σ)
- **Stabilizer Consistency:** S̄ = 0.908 ± 0.002
- **State Fidelity:** F ≥ 0.951

### Theoretical Framework
- Structural isomorphism between classical correlation length and quantum stabilizer coherence length
- Both quantify how global constraints suppress local fluctuations
- Operational framework connecting formal causation to quantum error correction

## Repository Structure
quantum-phase-transitions/
├── README.md                     # This file
├── LICENSE                       # MIT License
├── requirements.txt              # Python dependencies (coming soon)
│
├── monte_carlo/                  # Monte Carlo simulations
│   ├── ising_model.py           # 2D Ising model implementation
│   ├── binder_cumulant.py       # Binder cumulant calculations
│   └── critical_analysis.py     # Critical phenomenon analysis
│
├── quantum_circuits/             # IBM Quantum implementations
│   ├── ghz_states.py            # GHZ state preparation
│   ├── stabilizer_measurements.py  # Stabilizer measurements
│   └── mermin_operator.py       # Mermin operator implementation
│
├── analysis/                     # Data analysis
│   ├── correlation_analysis.py  # Correlation function analysis
│   ├── statistical_tests.py     # Statistical testing
│   └── visualization.py         # Data visualization
│
└── notebooks/                    # Jupyter notebooks
├── 01_ising_simulation.ipynb
├── 02_quantum_experiments.ipynb
└── 03_correspondence_analysis.ipynb

## Installation
```bash
git clone https://github.com/ubunturbo/quantum-phase-transitions.git
cd quantum-phase-transitions
pip install -r requirements.txt
Requirements

Python 3.8+
NumPy
SciPy
Matplotlib
Qiskit (for IBM Quantum experiments)
IBM Quantum account (for quantum circuit execution)

Usage
Monte Carlo Simulation
pythonfrom monte_carlo import IsingModel

# Initialize 2D Ising model
model = IsingModel(size=64, temperature=2.269)

# Run simulation
results = model.run_simulation(steps=100000)

# Calculate Binder cumulant
U4 = model.calculate_binder_cumulant()
Quantum Circuit Experiments
pythonfrom quantum_circuits import GHZState

# Create 3-qubit GHZ state
ghz = GHZState(n_qubits=3)

# Measure stabilizers
results = ghz.measure_stabilizers(shots=8192)

# Calculate Mermin operator
M = ghz.calculate_mermin_violation()
Code Availability
Note: Code is being uploaded progressively. For immediate access during peer review, please contact:
Email: lemissio@gmail.com
ORCID: 0009-0003-5188-2314
Citation
If you use this work in your research, please cite:
bibtex@article{takagi2025structural,
  title={Structural Correspondence Between Classical Phase Transitions and Quantum Stabilizer Codes: A Framework for Formal Causation in Quantum Information},
  author={Takagi, Takayuki},
  journal={Nature Communications},
  year={2025},
  note={Manuscript ID: NCOMMS-25-82293, Under Review}
}
License
This project is licensed under the MIT License - see the LICENSE file for details.
Contact
Takayuki Takagi
Independent Researcher
Email: lemissio@gmail.com
ORCID: 0009-0003-5188-2314
Acknowledgments
This research was conducted using IBM Quantum services. The views expressed are those of the author and do not reflect the official policy or position of IBM.

This repository is associated with a manuscript currently under peer review at Nature Communications.
