"""
Unit tests for 2D Ising model implementation
Tests verify:
1. Energy calculations
2. Metropolis acceptance
3. Observable computations
4. Critical temperature detection
"""

import pytest
import numpy as np
import sys
sys.path.insert(0, '../src')

from classical.ising_model import (
    IsingModel2D, 
    SimulationConfig,
    compute_observables,
    identify_critical_band
)


class TestIsingModel2D:
    """Test suite for Ising model implementation"""
    
    @pytest.fixture
    def small_config(self):
        """Create small system for fast testing"""
        return SimulationConfig(
            L=4,
            n_thermalization=100,
            n_sweeps=500,
            sampling_interval=10
        )
    
    def test_initialization(self, small_config):
        """Test proper model initialization"""
        model = IsingModel2D(small_config)
        
        assert model.L == 4
        assert model.N == 16
        assert model.spins.shape == (4, 4)
        assert np.all(np.abs(model.spins) == 1)
    
    def test_ferromagnetic_ground_state(self):
        """Test energy of fully aligned configuration"""
        config = SimulationConfig(L=4)
        model = IsingModel2D(config)
        
        # All spins up
        model.spins = np.ones((4, 4), dtype=int)
        E_ferro = model.total_energy()
        
        # Expected: -J * (2 * L * L) = -32 for L=4
        expected = -2 * 4 * 4
        assert np.isclose(E_ferro, expected)
    
    def test_antiferromagnetic_energy(self):
        """Test energy of checkerboard configuration"""
        config = SimulationConfig(L=4)
        model = IsingModel2D(config)
        
        # Checkerboard pattern
        for i in range(4):
            for j in range(4):
                model.spins[i,j] = 1 if (i+j) % 2 == 0 else -1
        
        E_af = model.total_energy()
        
        # All bonds frustrated: E = +32
        expected = 2 * 4 * 4
        assert np.isclose(E_af, expected)
    
    def test_local_energy_consistency(self):
        """Verify local and global energy calculations agree"""
        config = SimulationConfig(L=4)
        model = IsingModel2D(config)
        
        E_before = model.total_energy()
        
        # Flip spin at (1,1)
        i, j = 1, 1
        dE = model.local_energy_change(i, j)
        model.spins[i,j] *= -1
        
        E_after = model.total_energy()
        
        assert np.isclose(E_after - E_before, dE, atol=1e-10)
    
    def test_metropolis_at_zero_temperature(self):
        """At T→0, only energy-lowering moves should be accepted"""
        config = SimulationConfig(L=4, n_sweeps=100)
        model = IsingModel2D(config)
        
        # Start from random state
        E_initial = model.total_energy()
        
        # Run at very low temperature
        beta = 100.0  # T = 0.01
        for _ in range(10):
            model.metropolis_sweep(beta)
        
        E_final = model.total_energy()
        
        # Energy should decrease or stay same
        assert E_final <= E_initial + 1e-10
    
    def test_high_temperature_limit(self):
        """At T→∞, magnetization should vanish"""
        config = SimulationConfig(L=8, n_thermalization=500, n_sweeps=2000)
        model = IsingModel2D(config)
        
        # Run at very high temperature
        data = model.run_simulation(T=10.0)
        M_mean = np.mean(data['magnetization']) / model.N
        
        # Should be close to zero (random alignment)
        assert abs(M_mean) < 0.15  # Allow some fluctuation
    
    def test_low_temperature_ordering(self):
        """At low T, system should order ferromagnetically"""
        config = SimulationConfig(L=8, n_thermalization=500, n_sweeps=2000)
        model = IsingModel2D(config)
        
        # Run at low temperature
        data = model.run_simulation(T=0.5)
        M_mean = np.mean(data['magnetization']) / model.N
        
        # Should be highly ordered
        assert abs(M_mean) > 0.85


class TestObservables:
    """Test observable computations"""
    
    def test_heat_capacity_positive(self):
        """Heat capacity should be positive"""
        # Generate mock data with energy fluctuations
        data = {
            'energy': np.random.normal(0, 10, size=1000),
            'magnetization': np.random.normal(0, 5, size=1000)
        }
        
        obs = compute_observables(data, T=2.0, N=64)
        
        assert obs['C'] > 0
        assert obs['chi'] > 0
    
    def test_binder_cumulant_bounds(self):
        """Binder cumulant should satisfy theoretical bounds"""
        # Generate mock magnetization data
        data = {
            'energy': np.zeros(1000),
            'magnetization': np.random.normal(0, 10, size=1000)
        }
        
        obs = compute_observables(data, T=2.0, N=64)
        U4 = obs['U4']
        
        # Theoretical bounds: 0 ≤ U4 ≤ 2/3 for Ising
        assert 0 <= U4 <= 0.67
    
    def test_ordered_phase_binder(self):
        """Binder cumulant in ordered phase should approach 0"""
        # Perfect ferromagnet: M = constant
        M0 = 60
        data = {
            'energy': np.zeros(1000),
            'magnetization': M0 + np.random.normal(0, 0.1, size=1000)
        }
        
        obs = compute_observables(data, T=0.5, N=64)
        
        # U4 → 0 in ordered phase
        assert obs['U4'] < 0.1
    
    def test_disordered_phase_binder(self):
        """Binder cumulant in disordered phase should approach 2/3"""
        # Random magnetization (Gaussian)
        data = {
            'energy': np.zeros(1000),
            'magnetization': np.random.normal(0, 10, size=1000)
        }
        
        obs = compute_observables(data, T=5.0, N=64)
        
        # U4 → 2/3 for Gaussian distribution
        assert abs(obs['U4'] - 2/3) < 0.1


class TestCriticalBandIdentification:
    """Test critical band detection"""
    
    def test_band_within_valid_range(self):
        """Critical band should contain exact Tc"""
        T_c_exact = 2.0 / np.log(1 + np.sqrt(2))
        
        # Mock U4 curve
        T_values = np.linspace(2.0, 2.5, 100)
        U4_values = 0.61 + 0.05 * np.tanh(10 * (T_values - T_c_exact))
        
        T_low, T_high = identify_critical_band(U4_values, T_values)
        
        assert T_low < T_c_exact < T_high
    
    def test_band_narrowing_with_size(self):
        """Critical band width should decrease with L"""
        # This would require full simulations
        # Placeholder for integration test
        pass
    
    def test_no_critical_band_found(self):
        """Handle case where U4 never enters critical region"""
        T_values = np.linspace(1.0, 1.5, 50)
        U4_values = np.ones(50) * 0.1  # Always ordered
        
        T_low, T_high = identify_critical_band(U4_values, T_values)
        
        assert T_low is None
        assert T_high is None


class TestNumericalStability:
    """Test numerical stability and edge cases"""
    
    def test_large_system_size(self):
        """Ensure code handles larger systems without overflow"""
        config = SimulationConfig(L=32, n_sweeps=100)
        model = IsingModel2D(config)
        
        # Should not raise exceptions
        E = model.total_energy()
        assert np.isfinite(E)
    
    def test_extreme_temperature_stability(self):
        """Check stability at extreme temperatures"""
        config = SimulationConfig(L=4, n_sweeps=100)
        model = IsingModel2D(config)
        
        # Very low temperature (high beta)
        try:
            data_low = model.run_simulation(T=0.001)
            assert len(data_low['energy']) > 0
        except OverflowError:
            pytest.fail("Overflow at low temperature")
        
        # Very high temperature (low beta)
        data_high = model.run_simulation(T=100.0)
        assert len(data_high['energy']) > 0


# Integration test
def test_full_simulation_pipeline():
    """End-to-end test of complete workflow"""
    from classical.ising_model import scan_temperature_range
    
    # Run minimal simulation
    T_array, results = scan_temperature_range(
        L=8,
        T_min=2.0,
        T_max=2.5,
        n_points=10
    )
    
    # Verify output structure
    assert len(T_array) == 10
    assert 'C' in results
    assert 'chi' in results
    assert 'U4' in results
    assert all(len(v) == 10 for v in results.values())
    
    # Check critical behavior
    idx_peak = np.argmax(results['C'])
    T_peak = T_array[idx_peak]
    T_c_exact = 2.0 / np.log(1 + np.sqrt(2))
    
    # Should be within 10% of exact Tc
    assert abs(T_peak - T_c_exact) / T_c_exact < 0.1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])