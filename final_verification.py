import json

print("="*70)
print("README.md FINAL VERIFICATION")
print("="*70)

# データ読み込み
with open('data/correspondence_results.json', 'r') as f:
    corr_data = json.load(f)

with open('data/classical/ising_reproduction_results.json', 'r') as f:
    ising_data = json.load(f)

with open('data/quantum/tstt_results.json', 'r') as f:
    quantum_data = json.load(f)

# 1. 相関係数の検証
print("\n1. CORRESPONDENCE STATISTICS:")
print("   " + "-"*60)
stats = corr_data['statistics']
print(f"   README claims: r = 0.999999")
print(f"   Actual value:  r = {stats['pearson_correlation']:.7f}")
print(f"   Match: {'✓' if abs(stats['pearson_correlation'] - 0.999999) < 0.000001 else '✗'}")
print()
print(f"   README claims: R² = 99.9999%")
print(f"   Actual value:  R² = {stats['r_squared']*100:.6f}%")
print(f"   Match: {'✓' if abs(stats['r_squared'] - 0.999999) < 0.000001 else '✗'}")
print()
print(f"   README claims: p-value < 10⁻⁵⁰")
print(f"   Actual value:  p-value = {stats['pearson_pvalue']:.2e}")
print(f"   Match: {'✓' if stats['pearson_pvalue'] < 1e-50 else '✗'}")

# 2. 古典Isingの検証
print("\n2. CLASSICAL ISING MODEL:")
print("   " + "-"*60)
classical = corr_data['classical']
print(f"   README claims: Tc = 2.250")
print(f"   Actual value:  Tc = {classical['critical_temperature']:.3f}")
print(f"   Match: {'✓' if abs(classical['critical_temperature'] - 2.250) < 0.001 else '✗'}")
print()
print(f"   README claims: Onsager error = 0.85%")
print(f"   Actual value:  Error = {classical['deviation_percent']:.2f}%")
print(f"   Match: {'✓' if abs(classical['deviation_percent'] - 0.85) < 0.01 else '✗'}")

# 3. 量子TSTTの検証
print("\n3. QUANTUM TSTT CIRCUITS:")
print("   " + "-"*60)
mermin = quantum_data['results']['mermin_operator']
print(f"   README claims: Mermin 0 → 4.0")
print(f"   Actual value:  Mermin {min(mermin):.1f} → {max(mermin):.1f}")
print(f"   Match: {'✓' if min(mermin) < 0.1 and max(mermin) > 3.9 else '✗'}")

# 4. 図ファイルの検証
print("\n4. REQUIRED FIGURES:")
print("   " + "-"*60)
import os
required_figures = [
    'classical_phase_transition.png',
    'quantum_stabilizer_measurements.png',
    'correspondence_phase_diagram.png',
    'correspondence_correlation.png'
]

all_exist = True
for fig in required_figures:
    path = f'figures/{fig}'
    exists = os.path.exists(path)
    status = "✓" if exists else "✗"
    print(f"   {status} {fig}")
    if not exists:
        all_exist = False

# 5. 総合判定
print("\n" + "="*70)
print("SUMMARY:")
print("="*70)

checks = [
    ("Pearson correlation r = 0.999999", abs(stats['pearson_correlation'] - 0.999999) < 0.000001),
    ("R-squared = 99.9999%", abs(stats['r_squared'] - 0.999999) < 0.000001),
    ("p-value < 10⁻⁵⁰", stats['pearson_pvalue'] < 1e-50),
    ("Tc = 2.250", abs(classical['critical_temperature'] - 2.250) < 0.001),
    ("Error = 0.85%", abs(classical['deviation_percent'] - 0.85) < 0.01),
    ("Mermin 0 → 4.0", min(mermin) < 0.1 and max(mermin) > 3.9),
    ("All figures exist", all_exist)
]

passed = sum([1 for _, check in checks if check])
total = len(checks)

for description, check in checks:
    status = "✓" if check else "✗"
    print(f"{status} {description}")

print("\n" + "="*70)
if passed == total:
    print(f"✅ ALL CHECKS PASSED ({passed}/{total})")
    print("README.md is ACCURATE and ready for publication!")
else:
    print(f"⚠️  SOME CHECKS FAILED ({passed}/{total})")
    print("Please review and correct README.md")
print("="*70)