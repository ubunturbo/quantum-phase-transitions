"""
2D Ising Model Monte Carlo Simulation
Implements Metropolis-Hastings algorithm for classical phase transition analysis
"""

import numpy as np
from typing import Tuple, Dict
from dataclasses import dataclass

@dataclass
class SimulationConfig:
    """Configuration parameters for Ising simulation"""
    L: int                    # Linear system size
    J: float = 1.0           # Coupling constant
    n_thermalization: int = 1000
    n_sweeps: int = 8000
    sampling_interval: int = 20
    
class IsingModel2D:
    """
    2D Ising model with periodic boundary conditions
    
    Hamiltonian: H = -J * sum_{<i,j>} sigma_i * sigma_j
    """
    
    def __init__(self, config: SimulationConfig):
        self.config = config
        self.L = config.L
        self.N = config.L ** 2
        self.J = config.J
        
        # Initialize random spin configuration
        self.spins = np.random.choice([-1, 1], size=(self.L, self.L))
        
    def total_energy(self) -> float:
        """Calculate total energy of current configuration"""
        E = 0.0
        for i in range(self.L):
            for j in range(self.L):
                # Periodic boundary conditions
                right = self.spins[i, (j+1) % self.L]
                down = self.spins[(i+1) % self.L, j]
                E += -self.J * self.spins[i,j] * (right + down)
        return E
    
    def local_energy_change(self, i: int, j: int) -> float:
        """
        Calculate energy change if spin at (i,j) is flipped
        Uses only nearest neighbors for efficiency
        """
        s = self.spins[i, j]
        neighbors_sum = (
            self.spins[i, (j+1) % self.L] +
            self.spins[i, (j-1) % self.L] +
            self.spins[(i+1) % self.L, j] +
            self.spins[(i-1) % self.L, j]
        )
        return 2 * self.J * s * neighbors_sum
    
    def metropolis_sweep(self, beta: float) -> None:
        """
        Perform one Monte Carlo sweep (N single-spin flip attempts)
        
        Args:
            beta: Inverse temperature 1/T
        """
        for _ in range(self.N):
            # Random spin selection
            i = np.random.randint(0, self.L)
            j = np.random.randint(0, self.L)
            
            dE = self.local_energy_change(i, j)
            
            # Metropolis acceptance criterion
            if dE <= 0 or np.random.random() < np.exp(-beta * dE):
                self.spins[i, j] *= -1
    
    def magnetization(self) -> float:
        """Calculate total magnetization"""
        return np.abs(np.sum(self.spins))
    
    def run_simulation(self, T: float) -> Dict[str, np.ndarray]:
        """
        Run complete simulation at temperature T
        
        Returns:
            Dictionary containing sampled energies and magnetizations
        """
        beta = 1.0 / T
        
        # Thermalization
        for _ in range(self.config.n_thermalization):
            self.metropolis_sweep(beta)
        
        # Measurement phase
        energies = []
        magnetizations = []
        
        for sweep in range(self.config.n_sweeps):
            self.metropolis_sweep(beta)
            
            if sweep % self.config.sampling_interval == 0:
                energies.append(self.total_energy())
                magnetizations.append(self.magnetization())
        
        return {
            'energy': np.array(energies),
            'magnetization': np.array(magnetizations)
        }


def compute_observables(data: Dict[str, np.ndarray], T: float, N: int) -> Dict[str, float]:
    """
    Compute thermodynamic observables from simulation data
    
    Args:
        data: Dictionary with 'energy' and 'magnetization' arrays
        T: Temperature
        N: System size (L^2)
    
    Returns:
        Dictionary with heat capacity C, susceptibility chi, and Binder cumulant U4
    """
    beta = 1.0 / T
    E = data['energy']
    M = data['magnetization']
    
    # Heat capacity
    E_mean = np.mean(E)
    E2_mean = np.mean(E**2)
    C = beta**2 * N * (E2_mean - E_mean**2)
    
    # Magnetic susceptibility
    M_mean = np.mean(M)
    M2_mean = np.mean(M**2)
    chi = beta * N * (M2_mean - M_mean**2)
    
    # Binder cumulant
    M4_mean = np.mean(M**4)
    U4 = 1.0 - M4_mean / (3 * M2_mean**2)
    
    return {
        'C': C,
        'chi': chi,
        'U4': U4,
        'E_mean': E_mean / N,
        'M_mean': M_mean / N
    }


def scan_temperature_range(
    L: int,
    T_min: float = 1.8,
    T_max: float = 2.8,
    n_points: int = 50
) -> Tuple[np.ndarray, Dict[str, np.ndarray]]:
    """
    Scan temperature range and compute observables
    
    Args:
        L: Linear system size
        T_min, T_max: Temperature range
        n_points: Number of temperature points
    
    Returns:
        Tuple of (temperatures, observables_dict)
    """
    config = SimulationConfig(L=L)
    temperatures = np.linspace(T_min, T_max, n_points)
    
    results = {
        'C': np.zeros(n_points),
        'chi': np.zeros(n_points),
        'U4': np.zeros(n_points)
    }
    
    for idx, T in enumerate(temperatures):
        print(f"L={L}, T={T:.3f} ({idx+1}/{n_points})")
        
        model = IsingModel2D(config)
        data = model.run_simulation(T)
        obs = compute_observables(data, T, model.N)
        
        results['C'][idx] = obs['C']
        results['chi'][idx] = obs['chi']
        results['U4'][idx] = obs['U4']
    
    return temperatures, results


# Critical band identification
def identify_critical_band(U4_values: np.ndarray, T_values: np.ndarray) -> Tuple[float, float]:
    """
    Identify temperature range where 0.55 <= U4 <= 0.65
    
    Returns:
        (T_lower, T_upper) defining the critical band
    """
    mask = (U4_values >= 0.55) & (U4_values <= 0.65)
    if np.any(mask):
        T_critical = T_values[mask]
        return T_critical.min(), T_critical.max()
    else:
        return None, None


if __name__ == "__main__":
    # Reproduce Figure 1 data
    for L in [8, 12, 16]:
        T_array, obs = scan_temperature_range(L)
        
        # Save results
        np.savez(
            f'data/classical/ising_L{L}_data.npz',
            temperatures=T_array,
            **obs
        )
        
        # Identify critical band
        T_low, T_high = identify_critical_band(obs['U4'], T_array)
        print(f"L={L}: Critical band [{T_low:.3f}, {T_high:.3f}]")