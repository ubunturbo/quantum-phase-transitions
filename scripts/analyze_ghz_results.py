"""
GHZ測定結果の解析スクリプト
===========================
論文の報告値と比較
"""

import json
import numpy as np

# データ読み込み
with open('data/quantum/ghz_raw_results.json', 'r') as f:
    data = json.load(f)

print("="*70)
print("GHZ測定結果解析")
print("="*70)
print(f"Job ID: {data['job_id']}")
print(f"Backend: {data['backend']}")
print(f"測定日: {data['measurement_date']}")
print(f"Shots: {data['shots']}")
print()

results = data['results']

def calculate_stabilizer_expectation(counts, stabilizer_name):
    """
    スタビライザー期待値を計算
    
    GHZ状態のスタビライザー:
    - XXX: 偶数パリティで+1, 奇数パリティで-1
    - ZZI: |00⟩, |11⟩ on first two qubits → +1, |01⟩, |10⟩ → -1
    - IZZ: |00⟩, |11⟩ on last two qubits → +1, |01⟩, |10⟩ → -1
    """
    total = sum(counts.values())
    
    if stabilizer_name == "XXX":
        # XXX: 偶数個の1で+1, 奇数個の1で-1
        plus_one = sum(count for bitstring, count in counts.items() 
                       if bitstring.count('1') % 2 == 0)
        minus_one = sum(count for bitstring, count in counts.items() 
                        if bitstring.count('1') % 2 == 1)
    
    elif stabilizer_name == "ZZI":
        # ZZI: Z⊗Z⊗I
        # +1: 00X, 11X (最初の2qubitが同じ)
        # -1: 01X, 10X (最初の2qubitが異なる)
        plus_one = sum(count for bitstring, count in counts.items() 
                       if bitstring[0] == bitstring[1])
        minus_one = sum(count for bitstring, count in counts.items() 
                        if bitstring[0] != bitstring[1])
    
    elif stabilizer_name == "IZZ":
        # IZZ: I⊗Z⊗Z
        # +1: X00, X11 (最後の2qubitが同じ)
        # -1: X01, X10 (最後の2qubitが異なる)
        plus_one = sum(count for bitstring, count in counts.items() 
                       if bitstring[1] == bitstring[2])
        minus_one = sum(count for bitstring, count in counts.items() 
                        if bitstring[1] != bitstring[2])
    
    expectation = (plus_one - minus_one) / total
    error = np.sqrt(total) / total  # Poisson統計誤差
    
    return expectation, error, plus_one, minus_one

# スタビライザー期待値計算
print("="*70)
print("スタビライザー期待値")
print("="*70)

stabilizers = {
    "XXX": "XXX",
    "ZZI": "ZZI", 
    "IZZ": "IZZ"
}

measured_expectations = {}

for basis_name, stab_name in stabilizers.items():
    if basis_name in results:
        exp, err, plus, minus = calculate_stabilizer_expectation(
            results[basis_name], stab_name
        )
        measured_expectations[stab_name] = exp
        
        print(f"\n⟨{stab_name}⟩:")
        print(f"  測定値: {exp:+.4f} ± {err:.4f}")
        print(f"  +1 eigenvalue counts: {plus}")
        print(f"  -1 eigenvalue counts: {minus}")
        print(f"  合計: {plus + minus}")

# 論文報告値との比較
print("\n" + "="*70)
print("論文報告値との比較")
print("="*70)

paper_values = {
    "XXX": 0.902,
    "ZZI": 0.914,
    "IZZ": 0.924
}

print(f"\n{'Stabilizer':<10} {'測定値':<12} {'論文値':<12} {'差異':<12}")
print("-"*50)
for stab in ["XXX", "ZZI", "IZZ"]:
    measured = measured_expectations.get(stab, 0)
    paper = paper_values.get(stab, 0)
    diff = measured - paper
    match = "✓" if abs(diff) < 0.02 else "⚠️"
    print(f"{stab:<10} {measured:+.4f}      {paper:+.4f}      {diff:+.4f}  {match}")

# Stabilizer consistency
S_bar = np.mean([abs(measured_expectations[s]) for s in ["XXX", "ZZI", "IZZ"]])
print(f"\nStabilizer Consistency S̄ = {S_bar:.4f}")
print(f"論文報告値: S̄ = 0.908 ± 0.002")
print(f"閾値: S̄ ≥ 0.90 (Structural Coherence Regime)")
print(f"判定: {'✓ SCR内' if S_bar >= 0.90 else '⚠️ SCR外'}")

# State fidelity下限推定
print("\n" + "="*70)
print("状態忠実度推定")
print("="*70)

zzz_counts = results.get("ZZZ", {})
if zzz_counts:
    total = sum(zzz_counts.values())
    ghz_population = (zzz_counts.get('000', 0) + zzz_counts.get('111', 0)) / total
    
    print(f"\n計算基底測定:")
    print(f"  |000⟩: {zzz_counts.get('000', 0)} ({zzz_counts.get('000', 0)/total*100:.2f}%)")
    print(f"  |111⟩: {zzz_counts.get('111', 0)} ({zzz_counts.get('111', 0)/total*100:.2f}%)")
    print(f"  GHZ部分空間: {ghz_population:.4f}")
    print(f"  忠実度下限: F ≥ {ghz_population:.4f}")
    print(f"  論文報告値: F ≥ 0.951")

# Mermin operator (もしXYY+YXY+YYXデータがあれば)
print("\n" + "="*70)
print("Mermin演算子")
print("="*70)

# Merminの各項を計算
# M = ⟨XXX⟩ - ⟨XYY⟩ - ⟨YXY⟩ - ⟨YYX⟩
# ただし、測定は "XYY+YXY+YYX" として一括で行われた可能性

if "XYY+YXY+YYX" in results:
    print("\n注意: XYY+YXY+YYXデータは複合測定の可能性")
    print("詳細な解析には個別の測定データが必要")
    
    # 仮にXXXだけから推定
    xxx_exp = measured_expectations.get("XXX", 0)
    print(f"\n⟨XXX⟩ = {xxx_exp:+.4f}")
    print(f"論文報告: M = 3.655 ± 0.005")
    print(f"理想GHZ: M = 4.000")

print("\n" + "="*70)
print("解析完了")
print("="*70)
print("\n次のステップ:")
print("1. 測定値が論文値と一致するか確認")
print("2. 必要に応じて符号補正を適用")
print("3. ghz_final_corrected.json を生成")