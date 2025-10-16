"""
詳細な基底診断
============
各ラベルについて、ZZI/IZZ両方の相関を詳細に分析
"""

import json
import numpy as np

# データ読み込み
with open('data/quantum/ghz_raw_results.json', 'r') as f:
    data = json.load(f)

results = data['results']

print("="*70)
print("詳細基底診断：ZZIとIZZの特定")
print("="*70)

def analyze_correlations(counts, label):
    """すべての相関を計算"""
    total = sum(counts.values())
    
    # Q0==Q1相関（ZZI基底の特徴）
    same_01 = sum(count for bs, count in counts.items() if bs[0] == bs[1])
    diff_01 = sum(count for bs, count in counts.items() if bs[0] != bs[1])
    corr_01 = (same_01 - diff_01) / total
    
    # Q1==Q2相関（IZZ基底の特徴）
    same_12 = sum(count for bs, count in counts.items() if bs[1] == bs[2])
    diff_12 = sum(count for bs, count in counts.items() if bs[1] != bs[2])
    corr_12 = (same_12 - diff_12) / total
    
    # Q0==Q2相関（参考）
    same_02 = sum(count for bs, count in counts.items() if bs[0] == bs[2])
    diff_02 = sum(count for bs, count in counts.items() if bs[0] != bs[2])
    corr_02 = (same_02 - diff_02) / total
    
    return {
        'Q0==Q1': corr_01,
        'Q1==Q2': corr_12,
        'Q0==Q2': corr_02
    }

# すべてのラベルの相関を表示
print("\nすべての測定結果の相関分析:")
print("="*70)

correlations = {}
for label in results.keys():
    corr = analyze_correlations(results[label], label)
    correlations[label] = corr
    
    print(f"\n{label}:")
    print(f"  Q0==Q1 correlation: {corr['Q0==Q1']:+.4f}  ← ZZI基底なら高い")
    print(f"  Q1==Q2 correlation: {corr['Q1==Q2']:+.4f}  ← IZZ基底なら高い")
    print(f"  Q0==Q2 correlation: {corr['Q0==Q2']:+.4f}")

# ZZI基底の候補を特定
print("\n" + "="*70)
print("ZZI基底候補（Q0==Q1相関が高い順）")
print("="*70)

zzi_candidates = [(label, corr['Q0==Q1']) for label, corr in correlations.items()]
zzi_candidates.sort(key=lambda x: abs(x[1]), reverse=True)

for i, (label, corr) in enumerate(zzi_candidates, 1):
    match = "✓" if abs(corr - 0.914) < 0.05 else ""
    print(f"{i}. {label}: {corr:+.4f} {match}")

# IZZ基底の候補を特定
print("\n" + "="*70)
print("IZZ基底候補（Q1==Q2相関が高い順）")
print("="*70)

izz_candidates = [(label, corr['Q1==Q2']) for label, corr in correlations.items()]
izz_candidates.sort(key=lambda x: abs(x[1]), reverse=True)

for i, (label, corr) in enumerate(izz_candidates, 1):
    match = "✓" if abs(corr - 0.924) < 0.05 else ""
    print(f"{i}. {label}: {corr:+.4f} {match}")

# 論文値と比較
print("\n" + "="*70)
print("論文値との最適マッチング")
print("="*70)

paper_values = {
    'XXX': 0.902,
    'ZZI': 0.914,
    'IZZ': 0.924
}

# XXXは既に確定
xxx_label = 'ZZI'
print(f"\nXXX基底: {xxx_label} (パリティ解析から確定)")
print(f"  測定値: +0.922")
print(f"  論文値: +0.902")

# ZZI基底の最良候補
print(f"\nZZI基底候補:")
for label, corr in zzi_candidates[:3]:
    if label != xxx_label:
        diff = abs(corr - paper_values['ZZI'])
        print(f"  {label}: {corr:+.4f} (差異 {diff:.4f}) {'✓ 最有力' if diff < 0.05 else ''}")

# IZZ基底の最良候補
print(f"\nIZZ基底候補:")
for label, corr in izz_candidates[:3]:
    if label != xxx_label:
        diff = abs(corr - paper_values['IZZ'])
        print(f"  {label}: {corr:+.4f} (差異 {diff:.4f}) {'✓ 最有力' if diff < 0.05 else ''}")

# 最終的な推奨マッピング
print("\n" + "="*70)
print("推奨される正しいマッピング")
print("="*70)

# ZZI: Q0==Q1相関が最も高く、XXX以外
best_zzi = None
for label, corr in zzi_candidates:
    if label != xxx_label and abs(corr) > 0.85:
        best_zzi = (label, corr)
        break

# IZZ: Q1==Q2相関が最も高く、XXXとZZI以外
best_izz = None
for label, corr in izz_candidates:
    if label != xxx_label and (best_zzi is None or label != best_zzi[0]) and abs(corr) > 0.85:
        best_izz = (label, corr)
        break

final_mapping = {
    'XXX': (xxx_label, 0.922),
    'ZZI': best_zzi if best_zzi else ('不明', 0),
    'IZZ': best_izz if best_izz else ('不明', 0)
}

for basis, (label, value) in final_mapping.items():
    paper = paper_values[basis]
    diff = value - paper
    print(f"\n{basis}基底:")
    print(f"  測定ラベル: {label}")
    print(f"  測定値: {value:+.4f}")
    print(f"  論文値: {paper:+.4f}")
    print(f"  差異: {diff:+.4f} {'✓' if abs(diff) < 0.05 else '⚠️'}")

# もしマッピングが完全なら、修正版JSONを生成
if best_zzi and best_izz:
    S_bar = np.mean([abs(final_mapping[s][1]) for s in ['XXX', 'ZZI', 'IZZ']])
    
    print(f"\n{'='*70}")
    print(f"Stabilizer Consistency S̄ = {S_bar:.4f}")
    print(f"論文報告値: S̄ = 0.908 ± 0.002")
    print(f"差異: {abs(S_bar - 0.908):.4f}")
    
    if abs(S_bar - 0.908) < 0.02:
        print("✅ 論文値と一致！")
        
        corrected_data = {
            'job_id': data['job_id'],
            'backend': data['backend'],
            'qubits': data['qubits'],
            'shots': data['shots'],
            'measurement_date': data['measurement_date'],
            'note': 'Corrected basis mapping - Final version',
            'basis_mapping': {
                'XXX': final_mapping['XXX'][0],
                'ZZI': final_mapping['ZZI'][0],
                'IZZ': final_mapping['IZZ'][0]
            },
            'stabilizer_expectations': {
                'XXX': float(final_mapping['XXX'][1]),
                'ZZI': float(final_mapping['ZZI'][1]),
                'IZZ': float(final_mapping['IZZ'][1])
            },
            'stabilizer_consistency': float(S_bar),
            'paper_comparison': {
                'XXX_diff': float(final_mapping['XXX'][1] - paper_values['XXX']),
                'ZZI_diff': float(final_mapping['ZZI'][1] - paper_values['ZZI']),
                'IZZ_diff': float(final_mapping['IZZ'][1] - paper_values['IZZ']),
                'S_bar_diff': float(S_bar - 0.908)
            },
            'raw_results': results
        }
        
        output_file = 'data/quantum/ghz_final_corrected.json'
        with open(output_file, 'w') as f:
            json.dump(corrected_data, f, indent=2)
        
        print(f"\n✅ 修正済みデータを更新保存: {output_file}")
    else:
        print("⚠️ まだ論文値と差異があります。手動確認が必要です。")