#!/usr/bin/env python3
import json
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

DATA_DIR = Path('data/classical')
OUTPUT_DIR = Path('reports')
OUTPUT_DIR.mkdir(exist_ok=True)

T_CRITICAL = 2.0 / np.log(1 + np.sqrt(2))
U4_LOWER = 0.55
U4_UPPER = 0.65
SIZES = [8, 12, 16]
COLORS = ['#E74C3C', '#3498DB', '#2ECC71']

def load_data(system_size):
    filepath = DATA_DIR / f'ising_L{system_size}_results.json'
    with open(filepath, 'r') as f:
        data = json.load(f)
    T = np.array([d['T'] for d in data])
    C = np.array([d['C'] for d in data])
    chi = np.array([d['chi'] for d in data])
    U4 = np.array([d['U4'] for d in data])
    return T, C, chi, U4

def create_figure():
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))
    fig.suptitle('Figure 1: Critical behavior of 2D Ising model. DMZ band (U₄ ∈ [0.55, 0.65]) shown in gray.', fontsize=11, y=1.02)
    panel_labels = ['A. Heat Capacity', 'B. Susceptibility', 'C. Binder Cumulant']
    
    for i, L in enumerate(SIZES):
        T, C, chi, U4 = load_data(L)
        axes[0].plot(T, C, 'o-', color=COLORS[i], label=f'L = {L}', linewidth=2, markersize=4, markeredgewidth=0)
        axes[1].plot(T, chi, 'o-', color=COLORS[i], label=f'L = {L}', linewidth=2, markersize=4, markeredgewidth=0)
        axes[2].plot(T, U4, 'o-', color=COLORS[i], label=f'L = {L}', linewidth=2, markersize=4, markeredgewidth=0)
    
    axes[0].set_xlabel('Temperature T', fontsize=11)
    axes[0].set_ylabel('C', fontsize=11)
    axes[0].set_title(panel_labels[0], fontsize=12, pad=10)
    axes[0].axvline(T_CRITICAL, color='gray', linestyle='--', linewidth=1, alpha=0.7)
    axes[0].set_xlim(1.8, 3.0)
    axes[0].grid(True, alpha=0.2)
    axes[0].legend(loc='upper right', fontsize=9, framealpha=0.9)
    
    axes[1].set_xlabel('Temperature T', fontsize=11)
    axes[1].set_ylabel('χ', fontsize=11)
    axes[1].set_title(panel_labels[1], fontsize=12, pad=10)
    axes[1].axvline(T_CRITICAL, color='gray', linestyle='--', linewidth=1, alpha=0.7)
    axes[1].set_xlim(1.8, 3.0)
    axes[1].grid(True, alpha=0.2)
    axes[1].legend(loc='upper right', fontsize=9, framealpha=0.9)
    
    axes[2].set_xlabel('Temperature T', fontsize=11)
    axes[2].set_ylabel('U₄', fontsize=11)
    axes[2].set_title(panel_labels[2], fontsize=12, pad=10)
    axes[2].axvline(T_CRITICAL, color='gray', linestyle='--', linewidth=1, alpha=0.7)
    axes[2].axhspan(U4_LOWER, U4_UPPER, color='gray', alpha=0.25, label='DMZ')
    axes[2].set_xlim(1.8, 3.0)
    axes[2].set_ylim(0.36, 0.92)
    axes[2].grid(True, alpha=0.2)
    legend_elements = [plt.Line2D([0], [0], color=COLORS[i], linewidth=2, label=f'L = {L}') for i, L in enumerate(SIZES)]
    axes[2].legend(handles=legend_elements, loc='lower right', fontsize=9, framealpha=0.9, title='System Size')
    axes[2].text(T_CRITICAL + 0.05, 0.38, f'Tc = {T_CRITICAL:.3f}', fontsize=9, color='gray', verticalalignment='bottom')
    plt.tight_layout()
    return fig

def main():
    print('='*60)
    print('Generating Figure 1: Critical behavior of 2D Ising model')
    print('='*60)
    for L in SIZES:
        filepath = DATA_DIR / f'ising_L{L}_results.json'
        if not filepath.exists():
            raise FileNotFoundError(f'Data file not found: {filepath}')
        print(f'✓ Found data: {filepath.name}')
    print('\n📊 Creating figure...')
    fig = create_figure()
    formats = {'png': {'dpi': 300, 'bbox_inches': 'tight'}, 'pdf': {'bbox_inches': 'tight'}}
    for fmt, kwargs in formats.items():
        output_path = OUTPUT_DIR / f'figure1_ising_critical.{fmt}'
        fig.savefig(output_path, **kwargs)
        print(f'✓ Saved: {output_path}')
    print(f'\n✅ Figure 1 generation complete!')
    print(f'   Critical temperature: Tc = {T_CRITICAL:.6f}')
    print(f'   Critical band: {U4_LOWER} ≤ U₄ ≤ {U4_UPPER}')
    print('='*60)

if __name__ == '__main__':
    main()
