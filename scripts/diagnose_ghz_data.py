"""
GHZデータの診断スクリプト
========================
どの結果がどの測定基底に対応するか推測
"""

import json

# データ読み込み
with open('data/quantum/ghz_raw_results.json', 'r') as f:
    data = json.load(f)

print("="*70)
print("GHZデータ診断")
print("="*70)

results = data['results']

def analyze_distribution(counts, label):
    """測定結果の分布を解析"""
    total = sum(counts.values())
    sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    
    print(f"\n{label}:")
    print(f"  Total shots: {total}")
    print(f"  Top 4 outcomes:")
    for bitstring, count in sorted_counts[:4]:
        percentage = count/total*100
        print(f"    {bitstring}: {count:5d} ({percentage:5.2f}%)")
    
    # GHZ特徴: |000⟩ + |111⟩ が多い
    ghz_pop = (counts.get('000', 0) + counts.get('111', 0)) / total
    print(f"  |000⟩ + |111⟩ population: {ghz_pop:.3f}")
    
    # パリティチェック（XXX用）
    even_parity = sum(count for bs, count in counts.items() if bs.count('1') % 2 == 0)
    odd_parity = sum(count for bs, count in counts.items() if bs.count('1') % 2 == 1)
    parity_asymmetry = (even_parity - odd_parity) / total
    print(f"  Parity asymmetry (even-odd)/total: {parity_asymmetry:+.3f}")
    
    # 最初の2qubitの相関（ZZI用）
    same_first_two = sum(count for bs, count in counts.items() if bs[0] == bs[1])
    diff_first_two = sum(count for bs, count in counts.items() if bs[0] != bs[1])
    correlation_01 = (same_first_two - diff_first_two) / total
    print(f"  Q0==Q1 correlation: {correlation_01:+.3f}")
    
    # 最後の2qubitの相関（IZZ用）
    same_last_two = sum(count for bs, count in counts.items() if bs[1] == bs[2])
    diff_last_two = sum(count for bs, count in counts.items() if bs[1] != bs[2])
    correlation_12 = (same_last_two - diff_last_two) / total
    print(f"  Q1==Q2 correlation: {correlation_12:+.3f}")
    
    return {
        'ghz_pop': ghz_pop,
        'parity_asymmetry': parity_asymmetry,
        'corr_01': correlation_01,
        'corr_12': correlation_12
    }

# すべての基底を解析
print("\n" + "="*70)
print("各測定基底の特徴分析")
print("="*70)

features = {}
for label in results.keys():
    features[label] = analyze_distribution(results[label], label)

# マッピング推測
print("\n" + "="*70)
print("測定基底の推測")
print("="*70)

print("\n期待される特徴:")
print("  XXX基底: GHZ population ≈ 0.95, Parity asymmetry 高")
print("  ZZI基底: Q0==Q1 correlation 高")
print("  IZZ基底: Q1==Q2 correlation 高")
print("  ZZZ基底: GHZ population ≈ 0.95")

print("\n推測結果:")

# XXX基底候補
xxx_candidates = [(label, feat['ghz_pop'], feat['parity_asymmetry']) 
                  for label, feat in features.items()]
xxx_candidates.sort(key=lambda x: x[1], reverse=True)
print(f"\nXXX基底候補（GHZ populationが高い順）:")
for label, ghz_pop, parity in xxx_candidates[:2]:
    print(f"  {label}: GHZ={ghz_pop:.3f}, Parity={parity:+.3f}")

# ZZI基底候補
zzi_candidates = [(label, feat['corr_01']) for label, feat in features.items()]
zzi_candidates.sort(key=lambda x: abs(x[1]), reverse=True)
print(f"\nZZI基底候補（Q0==Q1 correlationが高い順）:")
for label, corr in zzi_candidates[:2]:
    print(f"  {label}: Correlation={corr:+.3f}")

# IZZ基底候補
izz_candidates = [(label, feat['corr_12']) for label, feat in features.items()]
izz_candidates.sort(key=lambda x: abs(x[1]), reverse=True)
print(f"\nIZZ基底候補（Q1==Q2 correlationが高い順）:")
for label, corr in izz_candidates[:2]:
    print(f"  {label}: Correlation={corr:+.3f}")

print("\n" + "="*70)
print("推奨される正しいマッピング:")
print("="*70)

# 最も可能性の高いマッピングを提案
mapping_proposal = {}

# XXXは明らかにGHZ populationが高いもの
for label, ghz_pop, _ in xxx_candidates:
    if ghz_pop > 0.9:
        mapping_proposal['XXX'] = label
        break

# ZZIはQ0==Q1相関が高いもの（XXX以外）
for label, corr in zzi_candidates:
    if label not in mapping_proposal.values() and abs(corr) > 0.8:
        mapping_proposal['ZZI'] = label
        break

# IZZはQ1==Q2相関が高いもの（XXX, ZZI以外）
for label, corr in izz_candidates:
    if label not in mapping_proposal.values() and abs(corr) > 0.8:
        mapping_proposal['IZZ'] = label
        break

print("\n提案されるマッピング:")
for true_basis, measured_label in mapping_proposal.items():
    print(f"  {true_basis} → {measured_label}")

print("\n未割り当ての測定結果:")
for label in results.keys():
    if label not in mapping_proposal.values():
        print(f"  {label}")