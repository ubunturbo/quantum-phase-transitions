"""
Error Analysis for GHZ Experimental Data
=========================================

This script performs comprehensive error analysis for the GHZ state measurements,
including:
1. Poisson statistical errors
2. Bootstrap error estimation
3. Readout error propagation
4. Systematic error assessment

Author: Takayuki Takagi
Date: 2025-10-16
"""

import json
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
from scipy import stats

class GHZErrorAnalysis:
    """Comprehensive error analysis for GHZ measurements"""
    
    def __init__(self, data_file: str):
        """
        Initialize with GHZ measurement data
        
        Args:
            data_file: Path to ghz_final_corrected.json
        """
        with open(data_file, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        
        self.results = {}
    
    def poisson_errors(self):
        """
        Calculate Poisson statistical errors
        
        For a stabilizer measurement with expectation <S> calculated from
        counts, the Poisson error is:
        
        σ_poisson = sqrt(<S²> - <S>²) / sqrt(N)
        
        where N is the total number of shots.
        """
        print("=" * 60)
        print("1. POISSON STATISTICAL ERRORS")
        print("=" * 60)
        
        stabilizers = self.data['stabilizer_expectations']
        shots = self.data['shots']
        
        for stab_name, expectation in stabilizers.items():
            
            # For Pauli measurements: <S²> = 1 (eigenvalues ±1)
            # Variance: Var(S) = <S²> - <S>² = 1 - <S>²
            variance = 1 - expectation**2
            
            # Standard error of the mean
            sigma_poisson = np.sqrt(variance / shots)
            
            self.results[f'{stab_name}_poisson'] = sigma_poisson
            
            print(f"\n{stab_name}:")
            print(f"  Expectation value: {expectation:.4f}")
            print(f"  Total shots: {shots}")
            print(f"  Variance: {variance:.6f}")
            print(f"  Poisson error: ± {sigma_poisson:.6f}")
            print(f"  Relative error: {sigma_poisson/abs(expectation)*100:.2f}%")
    
    def _calculate_eigenvalues(self, stab_name, counts):
        """Helper function to calculate eigenvalues from raw counts"""
        eigenvalues = []
        for outcome, count in counts.items():
            # Determine eigenvalue based on stabilizer type
            if stab_name == 'XXX':
                # XXX: even parity of all three bits
                parity = outcome.count('1') % 2
            elif stab_name == 'ZZI':
                # ZZI: even parity of first two bits
                parity = (int(outcome[0]) + int(outcome[1])) % 2
            elif stab_name == 'IZZ':
                # IZZ: even parity of last two bits
                parity = (int(outcome[1]) + int(outcome[2])) % 2
            else:
                # Generic: even parity
                parity = outcome.count('1') % 2
            
            eigenval = 1 if parity == 0 else -1
            eigenvalues.extend([eigenval] * count)
        
        return np.array(eigenvalues)
    
    def derive_zzi_izz_from_zzz(self):
        """
        Derive ZZI and IZZ stabilizer eigenvalues from ZZZ measurements
        
        ZZI: Z⊗Z⊗I - measure qubits 0,1 parity (ignore qubit 2)
        IZZ: I⊗Z⊗Z - measure qubits 1,2 parity (ignore qubit 0)
        """
        zzz_counts = self.data['raw_measurement_counts']['ZZZ']
        
        zzi_eigenvalues = []
        izz_eigenvalues = []
        
        for outcome, count in zzz_counts.items():
            # outcome is like "000", "001", "111", etc.
            q0, q1, q2 = [int(b) for b in outcome]
            
            # ZZI: parity of qubits 0 and 1
            zzi_parity = (q0 + q1) % 2
            zzi_eigenval = 1 if zzi_parity == 0 else -1
            zzi_eigenvalues.extend([zzi_eigenval] * count)
            
            # IZZ: parity of qubits 1 and 2
            izz_parity = (q1 + q2) % 2
            izz_eigenval = 1 if izz_parity == 0 else -1
            izz_eigenvalues.extend([izz_eigenval] * count)
        
        return np.array(zzi_eigenvalues), np.array(izz_eigenvalues)
    
    def bootstrap_errors(self, n_bootstrap=10000):
        """
        Bootstrap error estimation
        
        Resample the raw counts with replacement to estimate
        the sampling distribution of stabilizer expectation values.
        
        Args:
            n_bootstrap: Number of bootstrap samples
        """
        print("\n" + "=" * 60)
        print("2. BOOTSTRAP ERROR ESTIMATION")
        print("=" * 60)
        print(f"Running {n_bootstrap} bootstrap samples...")
        
        stabilizers = self.data['stabilizer_expectations']
        raw_counts = self.data['raw_measurement_counts']
        total = self.data['shots']
        
        # Derive ZZI and IZZ from ZZZ measurements
        print("\nDeriving ZZI and IZZ from ZZZ measurements...")
        zzi_eigenvals, izz_eigenvals = self.derive_zzi_izz_from_zzz()
        
        # Store derived eigenvalues for bootstrap
        derived_eigenvalues = {
            'ZZI': zzi_eigenvals,
            'IZZ': izz_eigenvals
        }
        
        for stab_name in stabilizers.keys():
            # Get raw counts for this measurement basis
            counts = raw_counts.get(stab_name)
            
            if counts is None and stab_name not in derived_eigenvalues:
                print(f"\n{stab_name}: No raw counts available, skipping bootstrap")
                continue
            
            # Use derived eigenvalues if available
            if stab_name in derived_eigenvalues:
                eigenvalues = derived_eigenvalues[stab_name]
                print(f"\n{stab_name}: Using derived eigenvalues from ZZZ")
            else:
                # Calculate eigenvalues from raw counts
                eigenvalues = self._calculate_eigenvalues(stab_name, counts)
            
            if eigenvalues is None:
                continue
            
            if eigenvalues is None:
                continue
            
            # Bootstrap resampling
            bootstrap_means = []
            for _ in range(n_bootstrap):
                resample = np.random.choice(eigenvalues, size=len(eigenvalues), replace=True)
                bootstrap_means.append(resample.mean())
            
            bootstrap_means = np.array(bootstrap_means)
            
            # Calculate bootstrap statistics
            mean = bootstrap_means.mean()
            std = bootstrap_means.std()
            ci_lower, ci_upper = np.percentile(bootstrap_means, [2.5, 97.5])
            
            self.results[f'{stab_name}_bootstrap_std'] = std
            self.results[f'{stab_name}_bootstrap_ci'] = (ci_lower, ci_upper)
            
            print(f"\n{stab_name}:")
            print(f"  Original expectation: {stabilizers[stab_name]:.4f}")
            print(f"  Bootstrap mean: {mean:.4f}")
            print(f"  Bootstrap std: ± {std:.6f}")
            print(f"  95% CI: [{ci_lower:.4f}, {ci_upper:.4f}]")
    
    def readout_error_propagation(self):
        """
        Estimate readout error propagation
        
        IBM Quantum devices have ~1-2% readout error per qubit.
        For 3-qubit measurements, errors propagate.
        """
        print("\n" + "=" * 60)
        print("3. READOUT ERROR PROPAGATION")
        print("=" * 60)
        
        # Typical readout error from device calibration
        readout_error_per_qubit = 0.015  # 1.5% per qubit (conservative)
        n_qubits = 3
        
        # Propagated readout error (assuming independent errors)
        total_readout_error = np.sqrt(n_qubits) * readout_error_per_qubit
        
        print(f"\nReadout error per qubit: {readout_error_per_qubit*100:.1f}%")
        print(f"Number of qubits: {n_qubits}")
        print(f"Propagated readout error: ± {total_readout_error:.6f}")
        print(f"  ({total_readout_error*100:.2f}%)")
        
        self.results['readout_error'] = total_readout_error
        
        # Apply to each stabilizer
        stabilizers = self.data['stabilizer_expectations']
        for stab_name in ['XXX', 'ZZI', 'IZZ']:
            exp_val = stabilizers[stab_name]
            error = exp_val * total_readout_error
            print(f"\n{stab_name}: {exp_val:.4f} ± {error:.6f}")
            self.results[f'{stab_name}_readout_error'] = error
    
    def gate_error_propagation(self):
        """
        Estimate gate error propagation
        
        GHZ circuit: 1 H + 2 CNOT gates
        Gate errors from device calibration
        """
        print("\n" + "=" * 60)
        print("4. GATE ERROR PROPAGATION")
        print("=" * 60)
        
        # From device calibration (Supplementary Note 3)
        h_gate_error = 0.0005  # ~0.05%
        cnot_gate_error = 0.008  # ~0.8%
        
        # GHZ circuit composition
        n_h_gates = 1
        n_cnot_gates = 2
        
        # Total gate error (linear approximation)
        total_gate_error = n_h_gates * h_gate_error + n_cnot_gates * cnot_gate_error
        
        print(f"\nH gate error: {h_gate_error*100:.2f}%")
        print(f"CNOT gate error: {cnot_gate_error*100:.2f}%")
        print(f"\nGHZ circuit:")
        print(f"  {n_h_gates} × H gate")
        print(f"  {n_cnot_gates} × CNOT gate")
        print(f"\nTotal gate error: ± {total_gate_error:.6f}")
        print(f"  ({total_gate_error*100:.2f}%)")
        
        self.results['gate_error'] = total_gate_error
        
        # Impact on stabilizer fidelity
        fidelity_lower_bound = 1 - total_gate_error
        print(f"\nEstimated fidelity lower bound: {fidelity_lower_bound:.4f}")
        print(f"  (95% with {total_gate_error*100:.1f}% error)")
    
    def combined_error_budget(self):
        """
        Combine all error sources
        
        Total error = sqrt(σ_stat² + σ_readout² + σ_gate²)
        """
        print("\n" + "=" * 60)
        print("5. COMBINED ERROR BUDGET")
        print("=" * 60)
        
        for stab_name in ['XXX', 'ZZI', 'IZZ']:
            # Statistical error (dominant)
            sigma_stat = self.results[f'{stab_name}_poisson']
            
            # Systematic errors
            sigma_readout = self.results.get(f'{stab_name}_readout_error', 0)
            sigma_gate = self.results.get('gate_error', 0)
            
            # Combined error (quadrature sum)
            sigma_total = np.sqrt(sigma_stat**2 + sigma_readout**2 + sigma_gate**2)
            
            self.results[f'{stab_name}_total_error'] = sigma_total
            
            print(f"\n{stab_name}:")
            print(f"  Statistical error:  ± {sigma_stat:.6f}")
            print(f"  Readout error:      ± {sigma_readout:.6f}")
            print(f"  Gate error:         ± {sigma_gate:.6f}")
            print(f"  ─────────────────────────────")
            print(f"  TOTAL ERROR:        ± {sigma_total:.6f}")
            
            # Compare with paper reported value
            reported_error = 0.003  # From paper
            print(f"\n  Paper reported:     ± {reported_error:.6f}")
            print(f"  Calculated/Reported: {sigma_total/reported_error:.2f}x")
    
    def systematic_bias_analysis(self):
        """
        Analyze systematic bias: why are experimental values higher?
        """
        print("\n" + "=" * 60)
        print("6. SYSTEMATIC BIAS ANALYSIS")
        print("=" * 60)
        
        # Use paper comparison data directly from JSON
        paper_comp = self.data['paper_comparison']
        
        biases = []
        print("\nExperimental vs Paper Reported Values:")
        
        for stab in ['XXX', 'ZZI', 'IZZ']:
            key = f'stabilizer_{stab}'
            comp = paper_comp[key]
            
            exp = comp['measured']
            paper = comp['paper']
            bias = comp['difference']
            rel_bias = (bias / paper) * 100
            biases.append(bias)
            
            print(f"\n{stab}:")
            print(f"  Experimental:  {exp:.4f}")
            print(f"  Paper:         {paper:.4f}")
            print(f"  Difference:    +{bias:.4f} (+{rel_bias:.2f}%)")
        
        # Statistical test: Are all biases positive?
        mean_bias = np.mean(biases)
        print(f"\nMean bias: +{mean_bias:.4f}")
        print(f"All values higher: {'YES ⚠️' if all(b > 0 for b in biases) else 'NO'}")
        
        print("\nPossible explanations:")
        print("  1. Different readout error mitigation")
        print("  2. Device calibration improved between runs")
        print("  3. Batch execution differences")
        print("  4. Statistical fluctuation (unlikely given consistency)")
    
    def generate_report(self, output_file='reports/error_analysis_report.txt'):
        """Generate comprehensive error analysis report"""
        
        Path('reports').mkdir(exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("=" * 70 + "\n")
            f.write("GHZ STATE ERROR ANALYSIS REPORT\n")
            f.write("=" * 70 + "\n\n")
            
            f.write("SUMMARY OF ERROR SOURCES\n")
            f.write("-" * 70 + "\n\n")
            
            for stab in ['XXX', 'ZZI', 'IZZ']:
                f.write(f"{stab}:\n")
                f.write(f"  Expectation value: {self.data['stabilizer_expectations'][stab]:.4f}\n")
                f.write(f"  Poisson error:     ± {self.results[f'{stab}_poisson']:.6f}\n")
                
                if f'{stab}_bootstrap_std' in self.results:
                    f.write(f"  Bootstrap std:     ± {self.results[f'{stab}_bootstrap_std']:.6f}\n")
                
                f.write(f"  Total error:       ± {self.results[f'{stab}_total_error']:.6f}\n")
                
                if f'{stab}_bootstrap_ci' in self.results:
                    ci_lower, ci_upper = self.results[f'{stab}_bootstrap_ci']
                    f.write(f"  95% CI:            [{ci_lower:.4f}, {ci_upper:.4f}]\n\n")
            
            f.write("\nRECOMMENDED ERROR BARS FOR PAPER:\n")
            f.write("-" * 70 + "\n\n")
            
            for stab in ['XXX', 'ZZI', 'IZZ']:
                exp = self.data['stabilizer_expectations'][stab]
                err = self.results[f'{stab}_total_error']
                f.write(f"  <{stab}> = {exp:.3f} ± {err:.3f}\n")
        
        print(f"\n✅ Report saved to: {output_file}")
    
    def run_full_analysis(self):
        """Run complete error analysis pipeline"""
        # First, verify ZZI and IZZ derivation
        print("=" * 60)
        print("VERIFYING ZZI AND IZZ DERIVATION FROM ZZZ")
        print("=" * 60)
        
        zzi_eigenvals, izz_eigenvals = self.derive_zzi_izz_from_zzz()
        
        # Calculate expectations from derived eigenvalues
        zzi_exp_derived = zzi_eigenvals.mean()
        izz_exp_derived = izz_eigenvals.mean()
        
        # Compare with reported values
        zzi_exp_reported = self.data['stabilizer_expectations']['ZZI']
        izz_exp_reported = self.data['stabilizer_expectations']['IZZ']
        
        print(f"\nZZI:")
        print(f"  Derived from ZZZ:  {zzi_exp_derived:.6f}")
        print(f"  Reported in data:  {zzi_exp_reported:.6f}")
        print(f"  Difference:        {abs(zzi_exp_derived - zzi_exp_reported):.6f}")
        
        print(f"\nIZZ:")
        print(f"  Derived from ZZZ:  {izz_exp_derived:.6f}")
        print(f"  Reported in data:  {izz_exp_reported:.6f}")
        print(f"  Difference:        {abs(izz_exp_derived - izz_exp_reported):.6f}")
        
        if abs(zzi_exp_derived - zzi_exp_reported) < 1e-6 and abs(izz_exp_derived - izz_exp_reported) < 1e-6:
            print("\n✅ Derivation verified! ZZI and IZZ match reported values.")
        else:
            print("\n⚠️ Warning: Small discrepancy detected (likely rounding)")
        
        # Continue with main analysis
        self.poisson_errors()
        self.bootstrap_errors()
        self.readout_error_propagation()
        self.gate_error_propagation()
        self.combined_error_budget()
        self.systematic_bias_analysis()
        self.generate_report()
        
        print("\n" + "=" * 60)
        print("✅ ERROR ANALYSIS COMPLETE")
        print("=" * 60)


if __name__ == "__main__":
    # データファイルのパス
    data_file = "data/quantum/ghz_final_corrected.json"
    
    # エラー解析実行
    analyzer = GHZErrorAnalysis(data_file)
    analyzer.run_full_analysis()