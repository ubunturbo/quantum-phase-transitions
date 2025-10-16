# Reproducibility Guide

This document provides detailed instructions for reproducing all results reported in "Structural Correspondence Between Classical Phase Transitions and Quantum Stabilizer Codes."

---

## Computational Environment

### Hardware Specifications

**Classical simulations:**
- CPU: Any modern processor (tested on Intel Core i7-12700)
- RAM: Minimum 8 GB recommended
- Storage: ~500 MB for all data

**Quantum experiments:**
- IBM Quantum access required
- Device used: **ibm_torino** (127-qubit Eagle r3)
- Measurement date: **October 10, 2025**

### Software Versions

```
Python: 3.9.18
NumPy: 1.24.3
SciPy: 1.10.1
Matplotlib: 3.7.1
Qiskit: 1.0.2
Qiskit-IBM-Runtime: 0.18.0
Pandas: 2.0.3
```

**Installation verification:**

```bash
python -c "import sys; print(f'Python {sys.version}')"
python -c "import numpy; print(f'NumPy {numpy.__version__}')"
python -c "import qiskit; print(f'Qiskit {qiskit.__version__}')"
```

---

## Step-by-Step Reproduction

### Phase 1: Classical Monte Carlo Simulations

**Goal:** Generate Figure 1 data (heat capacity, susceptibility, Binder cumulant)

#### 1.1 Single System Size Test

```bash
python src/classical/ising_model.py --L 8 --T_min 2.0 --T_max 2.5 --n_points 10
```

**Expected output:**
```
L=8, T=2.000 (1/10)
L=8, T=2.056 (2/10)
...
Critical band: [2.20, 2.34]
Saved: data/classical/ising_L8_data.npz
```

**Verification checklist:**
- [ ] Peak in heat capacity near T ≈ 2.269
- [ ] Peak in susceptibility at same temperature
- [ ] U₄ crosses 0.61 near critical temperature
- [ ] Data saved in correct format

#### 1.2 Full Figure 1 Reproduction

```bash
python scripts/run_ising_simulation.py \
    --sizes 8 12 16 \
    --T_min 1.8 \
    --T_max 2.8 \
    --n_points 50 \
    --n_sweeps 8000 \
    --thermalization 1000
```

**Runtime estimates:**
- L=8: ~10 minutes
- L=12: ~20 minutes  
- L=16: ~40 minutes
- **Total: ~70 minutes**

**Output validation:**

```python
import numpy as np

# Load data
data_L8 = np.load('data/classical/ising_L8_data.npz')
T = data_L8['temperatures']
U4 = data_L8['U4']

# Check critical temperature
T_c_exact = 2 / np.log(1 + np.sqrt(2))  # 2.269185...
idx_peak = np.argmax(data_L8['C'])
T_c_measured = T[idx_peak]

print(f"Exact Tc: {T_c_exact:.6f}")
print(f"Measured Tc: {T_c_measured:.6f}")
print(f"Deviation: {abs(T_c_measured - T_c_exact):.4f}")
# Should be < 0.05 for L=16
```

#### 1.3 Critical Band Identification

```python
from src.classical.critical_band import identify_critical_band

T_lower, T_upper = identify_critical_band(U4, T)
print(f"Critical band: [{T_lower:.3f}, {T_upper:.3f}]")
print(f"Width: {T_upper - T_lower:.3f}")

# Expected values (approximate):
# L=8:  [2.15, 2.40] (width ~0.25)
# L=12: [2.19, 2.35] (width ~0.16)
# L=16: [2.22, 2.32] (width ~0.10)
```

---

### Phase 2: Quantum Hardware Experiments

**IMPORTANT FOR REVIEWERS:** You can either:
1. **Use provided data** (`data/raw/*.json`) from our October 10, 2025 measurements
2. **Re-run experiments** on IBM Quantum (requires queue time)

#### 2.1 IBM Quantum Setup

```bash
# Save API token
qiskit-ibm-runtime save-account --token YOUR_API_TOKEN --channel ibm_quantum

# Verify access
python -c "from qiskit_ibm_runtime import QiskitRuntimeService; \
           service = QiskitRuntimeService(); \
           print(service.backends())"
```

#### 2.2 Device Selection

**Recommended device:** `ibm_torino` (127-qubit Eagle r3)

**Check device availability:**

```python
from qiskit_ibm_runtime import QiskitRuntimeService

service = QiskitRuntimeService()
backend = service.backend('ibm_torino')

print(f"Status: {backend.status().status_msg}")
print(f"Queue length: {backend.status().pending_jobs}")

# Check calibration data
props = backend.properties()
print(f"CNOT error (q0-q1): {props.gate_error('cx', [0,1]):.4f}")
print(f"T1 (q0): {props.t1(0)*1e6:.1f} μs")
```

**Alternative devices:** `ibm_kyoto`, `ibm_osaka` (similar specs)

#### 2.3 Run Stabilizer Measurements

**Option A: Use provided data (fastest)**

```python
import json

with open('data/raw/ghz_xxx_shots.json') as f:
    counts_xxx = json.load(f)

from src.quantum.ghz_circuits import StabilizerAnalysis
analyzer = StabilizerAnalysis()

exp_xxx = analyzer.compute_expectation(counts_xxx, 'XXX')
print(f"⟨XXX⟩ = {exp_xxx:.4f}")
# Expected: 0.9021 ± 0.0030
```

**Option B: Re-run on hardware**

```bash
python src/quantum/ghz_circuits.py --backend ibm_torino --shots 30000
```

**Queue considerations:**
- Typical wait: 2-6 hours
- Job duration: ~5 minutes per circuit
- Total circuits: 8 (4 stabilizer + 4 Mermin)

#### 2.4 Verify Stabilizer Consistency

```python
from src.quantum.ghz_circuits import StabilizerAnalysis
import json

# Load all stabilizer measurements
stabilizers = {}
for name in ['XXX', 'ZZI', 'IZZ']:
    with open(f'data/raw/ghz_{name.lower()}_shots.json') as f:
        counts = json.load(f)
        stabilizers[name] = StabilizerAnalysis.compute_expectation(counts, name)

# Compute S̄
S_bar = StabilizerAnalysis.compute_stabilizer_consistency(stabilizers)
print(f"S̄ = {S_bar:.4f}")

# Expected values:
# ⟨XXX⟩ = 0.902 ± 0.003
# ⟨ZZI⟩ = 0.914 ± 0.003
# ⟨IZZ⟩ = 0.924 ± 0.002
# S̄ = 0.908 ± 0.002

# Check threshold
if S_bar >= 0.90:
    print("✓ State in Structural Coherence Regime")
else:
    print("✗ Below SCR threshold")
```

#### 2.5 Mermin Operator Verification

```python
# Load Mermin basis measurements
mermin_exp = {}
for basis in ['XXX', 'XYY', 'YXY', 'YYX']:
    with open(f'data/raw/mermin_{basis.lower()}_shots.json') as f:
        counts = json.load(f)
        mermin_exp[basis] = StabilizerAnalysis.compute_expectation(counts, basis)

# Compute M (with phase correction)
M = mermin_exp['XXX'] - mermin_exp['XYY'] - mermin_exp['YXY'] - mermin_exp['YYX']
print(f"M = {M:.4f}")

# Expected: 3.655 ± 0.005
# Theoretical bound: |M| ≤ 2 (local realism)
# Quantum maximum: M = 4

sigma_violation = (M - 2) / 0.005  # Approximate uncertainty
print(f"Violation of local bound: {sigma_violation:.0f}σ")
```

---

### Phase 3: Correspondence Analysis

#### 3.1 Structural Mapping

```python
from src.analysis.correspondence import compute_structural_correspondence

# Load classical data
classical_data = {
    'L8': np.load('data/classical/ising_L8_data.npz'),
    'L12': np.load('data/classical/ising_L12_data.npz'),
    'L16': np.load('data/classical/ising_L16_data.npz')
}

# Load quantum data
quantum_results = {
    'S_bar': 0.908,
    'fidelity': 0.951,
    'mermin': 3.655
}

# Compute correspondence
correspondence = compute_structural_correspondence(
    classical_data, 
    quantum_results
)

print(f"Classical critical band width: {correspondence['band_width']:.3f}")
print(f"Quantum SCR confidence: {correspondence['scr_confidence']:.3f}")
print(f"Structural isomorphism score: {correspondence['iso_score']:.3f}")
```

#### 3.2 Generate Publication Figures

```bash
python scripts/generate_all_figures.py --output figures/ --format pdf --dpi 300
```

**Generates:**
- `figure1_ising_critical.pdf` - Three-panel Ising model plot
- `figure_correspondence.pdf` - U₄ vs S̄ comparison
- `figure_mermin.pdf` - Mermin violation visualization

**Verification:**
- [ ] Figure 1A: C peak at T ≈ 2.269
- [ ] Figure 1B: χ peak at same T
- [ ] Figure 1C: U₄ critical band (gray) spans 0.55-0.65
- [ ] All curves labeled with system sizes

---

## Error Analysis

### Classical Simulations

**Statistical errors:**
- Jackknife resampling for U₄ uncertainty
- Bootstrap for C and χ error bars

```python
from src.analysis.error_analysis import jackknife_uncertainty

U4_values = data_L16['U4']
U4_err = jackknife_uncertainty(U4_values, n_blocks=10)
print(f"U₄ uncertainty: ±{U4_err:.4f}")
```

### Quantum Measurements

**Shot noise:**
```python
import numpy as np

shots = 30000
expectation = 0.902

# Standard error
sigma = np.sqrt((1 - expectation**2) / shots)
print(f"Statistical uncertainty: ±{sigma:.4f}")
# Expected: ±0.003
```

**Readout error mitigation:**
- Applied via IBM calibration matrices
- Reduces systematic bias by ~2-3%

---

## Troubleshooting

### Issue: Ising simulation too slow

**Solution:** Reduce system sizes or temperature points
```bash
python scripts/run_ising_simulation.py --sizes 8 12 --n_points 30
```

### Issue: IBM Quantum queue timeout

**Solution:** Use stored data
```python
# All results available in data/raw/
# No hardware access needed for verification
```

### Issue: Different Mermin sign

**Check phase convention:**
```python
# Expected XYY behavior for GHZ
# ⟨XYY⟩_ideal = -1
# If you get +1, apply sign correction (see Supplementary Note 5)
```

### Issue: Figures don't match paper

**Check Matplotlib settings:**
```python
import matplotlib.pyplot as plt
plt.rcParams['font.size'] = 10
plt.rcParams['figure.dpi'] = 300
```

---

## Validation Checklist

Before submitting results, verify:

### Classical
- [ ] Critical temperature within 0.05 of T_c = 2.269
- [ ] U₄ crosses ~0.61 at critical point
- [ ] Critical band width scales as ΔT ∼ L^(-1)

### Quantum
- [ ] S̄ ≥ 0.90 (Structural Coherence Regime)
- [ ] Fidelity F ≥ 0.95
- [ ] Mermin M > 2 (violates local realism)
- [ ] All stabilizers have positive expectation

### Correspondence
- [ ] Classical band [0.55, 0.65] identified
- [ ] Quantum SCR threshold justified
- [ ] Structural isomorphism documented

---

## Contact for Issues

If you encounter problems reproducing results:

1. Check [GitHub Issues](https://github.com/ubunturbo/quantum-stabilizer-correspondence/issues)
2. Email: lemissio@gmail.com
3. Include: error messages, system info, attempted solutions

**Response time:** Typically within 48 hours