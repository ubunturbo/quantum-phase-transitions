"""
Quantum circuit implementation for GHZ state preparation and stabilizer measurements
Compatible with IBM Quantum hardware
"""

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService, Session, SamplerV2
import numpy as np
from typing import Dict, List, Tuple

class GHZStateExperiment:
    """
    Three-qubit GHZ state preparation and stabilizer measurements
    
    Target state: |GHZ⟩ = (|000⟩ + |111⟩)/√2
    Stabilizers: {XXX, ZZI, IZZ}
    """
    
    def __init__(self, backend_name: str = 'ibm_torino'):
        """
        Initialize quantum experiment
        
        Args:
            backend_name: IBM Quantum device name
        """
        self.service = QiskitRuntimeService()
        self.backend = self.service.backend(backend_name)
        self.n_qubits = 3
        
    def create_ghz_circuit(self) -> QuantumCircuit:
        """
        Create circuit for GHZ state preparation
        
        Circuit:
            H on q0: |0⟩ → (|0⟩ + |1⟩)/√2
            CNOT q0→q1, q0→q2: entangle all qubits
        """
        qc = QuantumCircuit(self.n_qubits)
        
        # Hadamard on first qubit
        qc.h(0)
        
        # CNOT gates to entangle
        qc.cx(0, 1)
        qc.cx(0, 2)
        
        return qc
    
    def create_stabilizer_circuits(self) -> Dict[str, QuantumCircuit]:
        """
        Create circuits for stabilizer measurements
        
        Returns:
            Dictionary mapping stabilizer labels to circuits
        """
        circuits = {}
        
        # XXX measurement: Hadamard all qubits before Z measurement
        qc_xxx = self.create_ghz_circuit()
        qc_xxx.h([0, 1, 2])
        qc_xxx.measure_all()
        qc_xxx.name = "XXX"
        circuits['XXX'] = qc_xxx
        
        # ZZI measurement: measure q0, q1 in Z basis
        qc_zzi = self.create_ghz_circuit()
        qc_zzi.measure_all()
        qc_zzi.name = "ZZI"
        circuits['ZZI'] = qc_zzi
        
        # IZZ measurement: measure q1, q2 in Z basis
        qc_izz = self.create_ghz_circuit()
        qc_izz.measure_all()
        qc_izz.name = "IZZ"
        circuits['IZZ'] = qc_izz
        
        # ZZZ (computational basis) for fidelity estimation
        qc_zzz = self.create_ghz_circuit()
        qc_zzz.measure_all()
        qc_zzz.name = "ZZZ"
        circuits['ZZZ'] = qc_zzz
        
        return circuits
    
    def create_mermin_circuits(self) -> Dict[str, QuantumCircuit]:
        """
        Create circuits for Mermin operator measurement
        
        M = ⟨XXX⟩ - ⟨XYY⟩ - ⟨YXY⟩ - ⟨YYX⟩
        
        Y-basis: S†H (where S = phase gate)
        """
        circuits = {}
        
        # XXX already in stabilizer circuits
        qc_xxx = self.create_ghz_circuit()
        qc_xxx.h([0, 1, 2])
        qc_xxx.measure_all()
        circuits['XXX'] = qc_xxx
        
        # XYY: q0 in X, q1,q2 in Y
        qc_xyy = self.create_ghz_circuit()
        qc_xyy.h(0)
        qc_xyy.sdg(1)
        qc_xyy.h(1)
        qc_xyy.sdg(2)
        qc_xyy.h(2)
        qc_xyy.measure_all()
        circuits['XYY'] = qc_xyy
        
        # YXY: q1 in X, q0,q2 in Y
        qc_yxy = self.create_ghz_circuit()
        qc_yxy.sdg(0)
        qc_yxy.h(0)
        qc_yxy.h(1)
        qc_yxy.sdg(2)
        qc_yxy.h(2)
        qc_yxy.measure_all()
        circuits['YXY'] = qc_yxy
        
        # YYX: q2 in X, q0,q1 in Y
        qc_yyx = self.create_ghz_circuit()
        qc_yyx.sdg(0)
        qc_yyx.h(0)
        qc_yyx.sdg(1)
        qc_yyx.h(1)
        qc_yyx.h(2)
        qc_yyx.measure_all()
        circuits['YYX'] = qc_yyx
        
        return circuits
    
    def run_experiment(
        self, 
        circuits: Dict[str, QuantumCircuit],
        shots: int = 30000
    ) -> Dict[str, Dict[str, int]]:
        """
        Execute circuits on IBM Quantum hardware
        
        Args:
            circuits: Dictionary of quantum circuits
            shots: Number of measurement shots per circuit
            
        Returns:
            Dictionary mapping circuit names to measurement counts
        """
        # Transpile circuits for target backend
        pm = generate_preset_pass_manager(
            optimization_level=3,
            backend=self.backend
        )
        
        transpiled_circuits = [pm.run(qc) for qc in circuits.values()]
        
        # Execute with SamplerV2
        with Session(backend=self.backend) as session:
            sampler = SamplerV2(session=session)
            job = sampler.run(transpiled_circuits, shots=shots)
            result = job.result()
        
        # Extract counts
        counts_dict = {}
        for idx, name in enumerate(circuits.keys()):
            pub_result = result[idx]
            counts_dict[name] = pub_result.data.meas.get_counts()
        
        return counts_dict


class StabilizerAnalysis:
    """Analyze stabilizer measurement outcomes"""
    
    @staticmethod
    def compute_expectation(counts: Dict[str, int], operator: str) -> float:
        """
        Compute expectation value from measurement counts
        
        Args:
            counts: Measurement outcome counts
            operator: Stabilizer operator (e.g., 'XXX', 'ZZI')
        
        Returns:
            Expectation value in [-1, +1]
        """
        total_shots = sum(counts.values())
        expectation = 0.0
        
        for bitstring, count in counts.items():
            # Convert bitstring to eigenvalue
            parity = bitstring.count('1') % 2
            eigenvalue = 1 if parity == 0 else -1
            expectation += eigenvalue * count
        
        return expectation / total_shots
    
    @staticmethod
    def compute_stabilizer_consistency(
        stabilizer_expectations: Dict[str, float]
    ) -> float:
        """
        Compute mean stabilizer consistency S̄
        
        S̄ = (1/3) * Σ |⟨Si⟩|
        
        Args:
            stabilizer_expectations: Dict with 'XXX', 'ZZI', 'IZZ' values
        
        Returns:
            Stabilizer consistency value
        """
        values = [
            abs(stabilizer_expectations['XXX']),
            abs(stabilizer_expectations['ZZI']),
            abs(stabilizer_expectations['IZZ'])
        ]
        return np.mean(values)
    
    @staticmethod
    def estimate_fidelity(counts_zzz: Dict[str, int]) -> float:
        """
        Estimate lower bound on state fidelity from computational basis
        
        F_lower = P(|000⟩) + P(|111⟩)
        
        Args:
            counts_zzz: Measurement counts in computational basis
        
        Returns:
            Conservative fidelity lower bound
        """
        total_shots = sum(counts_zzz.values())
        ghz_counts = counts_zzz.get('000', 0) + counts_zzz.get('111', 0)
        return ghz_counts / total_shots
    
    @staticmethod
    def compute_mermin_operator(
        mermin_expectations: Dict[str, float]
    ) -> float:
        """
        Compute Mermin operator value
        
        M = ⟨XXX⟩ - ⟨XYY⟩ - ⟨YXY⟩ - ⟨YYX⟩
        
        Args:
            mermin_expectations: Dict with measurement expectations
        
        Returns:
            Mermin operator value
        """
        M = (
            mermin_expectations['XXX']
            - mermin_expectations['XYY']
            - mermin_expectations['YXY']
            - mermin_expectations['YYX']
        )
        return M


def run_full_experiment(backend_name: str = 'ibm_torino') -> Dict:
    """
    Run complete GHZ state experiment and analysis
    
    Returns:
        Dictionary with all experimental results
    """
    exp = GHZStateExperiment(backend_name)
    analyzer = StabilizerAnalysis()
    
    # Run stabilizer measurements
    print("Running stabilizer measurements...")
    stabilizer_circuits = exp.create_stabilizer_circuits()
    stabilizer_counts = exp.run_experiment(stabilizer_circuits)
    
    # Run Mermin measurements
    print("Running Mermin operator measurements...")
    mermin_circuits = exp.create_mermin_circuits()
    mermin_counts = exp.run_experiment(mermin_circuits)
    
    # Analyze results
    stabilizer_exp = {
        'XXX': analyzer.compute_expectation(stabilizer_counts['XXX'], 'XXX'),
        'ZZI': analyzer.compute_expectation(stabilizer_counts['ZZI'], 'ZZI'),
        'IZZ': analyzer.compute_expectation(stabilizer_counts['IZZ'], 'IZZ')
    }
    
    mermin_exp = {
        key: analyzer.compute_expectation(mermin_counts[key], key)
        for key in ['XXX', 'XYY', 'YXY', 'YYX']
    }
    
    S_bar = analyzer.compute_stabilizer_consistency(stabilizer_exp)
    fidelity = analyzer.estimate_fidelity(stabilizer_counts['ZZZ'])
    mermin_value = analyzer.compute_mermin_operator(mermin_exp)
    
    print(f"\n=== Results ===")
    print(f"Stabilizer Consistency: S̄ = {S_bar:.4f}")
    print(f"State Fidelity (lower bound): F ≥ {fidelity:.4f}")
    print(f"Mermin Operator: M = {mermin_value:.4f}")
    print(f"Structural Coherence Regime: {'YES' if S_bar >= 0.90 else 'NO'}")
    
    return {
        'stabilizer_expectations': stabilizer_exp,
        'mermin_expectations': mermin_exp,
        'S_bar': S_bar,
        'fidelity': fidelity,
        'mermin_value': mermin_value,
        'raw_counts': {
            'stabilizer': stabilizer_counts,
            'mermin': mermin_counts
        }
    }


if __name__ == "__main__":
    results = run_full_experiment()
    
    # Save results
    import json
    with open('data/raw/quantum_experiment_results.json', 'w') as f:
        json.dump(results, f, indent=2)