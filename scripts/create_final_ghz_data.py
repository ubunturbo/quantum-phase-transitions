"""
最終版GHZデータファイル作成
=======================
元の実験結果JSONから論文用データを生成
"""

import json
import shutil

# 元の実験結果を読み込み
source_file = 'C:/Users/hmbc0/ghz_experiment/ghz_torino_result_20251010_211841.json'
with open(source_file, 'r', encoding='utf-8') as f:
    original_data = json.load(f)

print("="*70)
print("最終版GHZデータファイル作成")
print("="*70)
print(f"ソース: {source_file}")
print()

# 論文用の最終データ構造
final_data = {
    "job_id": original_data['job_id'],
    "backend": original_data['backend'],
    "qubits": original_data['layout'],
    "shots": original_data['shots'],
    "measurement_date": "2025-10-10T21:00:54.978368+09:00",
    
    "note": "GHZ state measurement data for Nature Communications submission",
    "paper_reference": "NCOMMS-25-82293",
    
    "measurement_bases": {
        "computational": "ZZZ",
        "xxx_pauli": "XXX", 
        "mermin_bases": ["XYY", "YXY", "YYX"]
    },
    
    "stabilizer_expectations": {
        "XXX": original_data['results']['mermin']['E_xxx'],
        "ZZI": original_data['results']['stabilizers']['ZZI'],
        "IZZ": original_data['results']['stabilizers']['IZZ']
    },
    
    "stabilizer_consistency": {
        "value": (abs(original_data['results']['mermin']['E_xxx']) + 
                 abs(original_data['results']['stabilizers']['ZZI']) + 
                 abs(original_data['results']['stabilizers']['IZZ'])) / 3,
        "note": "S̄ = (|⟨XXX⟩| + |⟨ZZI⟩| + |⟨IZZ⟩|) / 3"
    },
    
    "mermin_operator": {
        "value": original_data['results']['mermin']['M'],
        "components": {
            "XXX": original_data['results']['mermin']['E_xxx'],
            "XYY": original_data['results']['mermin']['E_xyy'],
            "YXY": original_data['results']['mermin']['E_yxy'],
            "YYX": original_data['results']['mermin']['E_yyx']
        },
        "formula": "M = ⟨XXX⟩ - ⟨XYY⟩ - ⟨YXY⟩ - ⟨YYX⟩",
        "classical_bound": 2.0,
        "quantum_bound": 4.0,
        "violation_sigma": "~730σ"
    },
    
    "state_fidelity": {
        "lower_bound": original_data['results']['fidelity_lower_bound'],
        "method": "Direct estimation from computational basis",
        "ghz_population": original_data['results']['ghz_index']
    },
    
    "raw_measurement_counts": original_data['raw_counts'],
    
    "paper_comparison": {
        "stabilizer_XXX": {
            "measured": original_data['results']['mermin']['E_xxx'],
            "paper": 0.902,
            "difference": original_data['results']['mermin']['E_xxx'] - 0.902
        },
        "stabilizer_ZZI": {
            "measured": original_data['results']['stabilizers']['ZZI'],
            "paper": 0.914,
            "difference": original_data['results']['stabilizers']['ZZI'] - 0.914
        },
        "stabilizer_IZZ": {
            "measured": original_data['results']['stabilizers']['IZZ'],
            "paper": 0.924,
            "difference": original_data['results']['stabilizers']['IZZ'] - 0.924
        },
        "mermin": {
            "measured": original_data['results']['mermin']['M'],
            "paper": 3.655,
            "difference": original_data['results']['mermin']['M'] - 3.655
        },
        "fidelity": {
            "measured": original_data['results']['fidelity_lower_bound'],
            "paper": 0.951,
            "difference": original_data['results']['fidelity_lower_bound'] - 0.951
        }
    },
    
    "structural_coherence_regime": {
        "threshold": 0.90,
        "measured": (abs(original_data['results']['mermin']['E_xxx']) + 
                    abs(original_data['results']['stabilizers']['ZZI']) + 
                    abs(original_data['results']['stabilizers']['IZZ'])) / 3,
        "status": "Within SCR" if ((abs(original_data['results']['mermin']['E_xxx']) + 
                                   abs(original_data['results']['stabilizers']['ZZI']) + 
                                   abs(original_data['results']['stabilizers']['IZZ'])) / 3) >= 0.90 else "Below threshold"
    }
}

# データの検証
print("データ検証:")
print("-"*70)
print(f"⟨XXX⟩: {final_data['stabilizer_expectations']['XXX']:.4f} (論文: 0.902)")
print(f"⟨ZZI⟩: {final_data['stabilizer_expectations']['ZZI']:.4f} (論文: 0.914)")
print(f"⟨IZZ⟩: {final_data['stabilizer_expectations']['IZZ']:.4f} (論文: 0.924)")
print(f"S̄: {final_data['stabilizer_consistency']['value']:.4f} (論文: 0.908)")
print(f"M: {final_data['mermin_operator']['value']:.4f} (論文: 3.655)")
print(f"F: {final_data['state_fidelity']['lower_bound']:.4f} (論文: 0.951)")

# すべての値が論文と±5%以内か確認
all_match = True
checks = [
    ("XXX", final_data['stabilizer_expectations']['XXX'], 0.902),
    ("ZZI", final_data['stabilizer_expectations']['ZZI'], 0.914),
    ("IZZ", final_data['stabilizer_expectations']['IZZ'], 0.924),
    ("Mermin", final_data['mermin_operator']['value'], 3.655),
    ("Fidelity", final_data['state_fidelity']['lower_bound'], 0.951)
]

print("\n" + "="*70)
print("論文値との整合性チェック:")
print("="*70)
for name, measured, paper in checks:
    diff = abs(measured - paper)
    percent = (diff / paper) * 100
    status = "✓" if percent < 5 else "⚠️"
    print(f"{name}: {percent:.2f}% 差異 {status}")
    if percent >= 5:
        all_match = False

if all_match:
    print("\n✅ すべての測定値が論文報告値と整合的です")
else:
    print("\n⚠️ 一部の値に大きな差異があります")

# ファイル保存
output_file = 'data/quantum/ghz_final_corrected.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(final_data, f, indent=2, ensure_ascii=False)

print(f"\n{'='*70}")
print(f"✅ 最終版データを保存: {output_file}")
print("="*70)

print("\n次のステップ:")
print("1. このファイルを論文のデータリポジトリに追加")
print("2. README.mdを更新してデータの説明を追加")
print("3. Gitコミット＆プッシュ")