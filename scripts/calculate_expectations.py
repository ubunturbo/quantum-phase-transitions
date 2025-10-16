#!/usr/bin/env python3
"""
GHZ生データから安定化子期待値を計算

生データ（ghz_raw_results.json）から各安定化子の期待値を計算し、
論文記載値およびghz_final_corrected.jsonの値と比較します。
"""

import json
import numpy as np

# ANSI color codes
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BLUE = '\033[94m'
BOLD = '\033[1m'
RESET = '\033[0m'

def load_raw_data():
    """生データを読み込む"""
    with open('data/quantum/ghz_raw_results.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def calculate_xxx_expectation(counts):
    """XXX安定化子の期待値を計算
    
    XXX演算子は全qubitsにXを適用
    - |000⟩, |111⟩ → 固有値 +1
    - その他 → 固有値 -1
    """
    total = sum(counts.values())
    
    # +1固有値に対応するビット列
    plus_one = counts.get('000', 0) + counts.get('111', 0)
    
    # -1固有値に対応するビット列（その他すべて）
    minus_one = total - plus_one
    
    expectation = (plus_one - minus_one) / total
    
    return {
        'expectation': expectation,
        'plus_one_counts': plus_one,
        'minus_one_counts': minus_one,
        'total': total
    }

def calculate_zzi_expectation(counts):
    """ZZI安定化子の期待値を計算
    
    ZZI = Z_0 ⊗ Z_1 ⊗ I_2
    
    IBM Qiskitのビット順序：Little-endian
    ビット列 "abc" → qubit_2=a, qubit_1=b, qubit_0=c (右がLSB)
    
    Z演算子の固有値：
    - |0⟩ → +1
    - |1⟩ → -1
    
    ZZI = Z_0 ⊗ Z_1 ⊗ I_2 の固有値：
    - q0=0, q1=0 → (+1)(+1) = +1: ビット列 "?00"
    - q0=0, q1=1 → (+1)(-1) = -1: ビット列 "?01"  
    - q0=1, q1=0 → (-1)(+1) = -1: ビット列 "?10"
    - q0=1, q1=1 → (-1)(-1) = +1: ビット列 "?11"
    
    ここで ? は qubit_2 の値（I演算子なので無視）
    """
    total = sum(counts.values())
    
    # +1固有値: 下2ビットが "00" または "11"
    plus_one = (counts.get('000', 0) + counts.get('100', 0) +  # q1=0, q0=0
                counts.get('011', 0) + counts.get('111', 0))   # q1=1, q0=1
    
    # -1固有値: 下2ビットが "01" または "10"
    minus_one = (counts.get('001', 0) + counts.get('101', 0) +  # q1=0, q0=1
                 counts.get('010', 0) + counts.get('110', 0))   # q1=1, q0=0
    
    expectation = (plus_one - minus_one) / total
    
    return {
        'expectation': expectation,
        'plus_one_counts': plus_one,
        'minus_one_counts': minus_one,
        'total': total,
        'detail': f"+1: ?00,?11 | -1: ?01,?10"
    }

def calculate_izz_expectation(counts):
    """IZZ安定化子の期待値を計算
    
    IZZ = I_0 ⊗ Z_1 ⊗ Z_2
    
    IBM Qiskitのビット順序：Little-endian
    ビット列 "abc" → qubit_2=a, qubit_1=b, qubit_0=c (右がLSB)
    
    IZZ = I_0 ⊗ Z_1 ⊗ Z_2 の固有値：
    - q1=0, q2=0 → (+1)(+1) = +1: ビット列 "00?"
    - q1=0, q2=1 → (+1)(-1) = -1: ビット列 "10?"
    - q1=1, q2=0 → (-1)(+1) = -1: ビット列 "01?"
    - q1=1, q2=1 → (-1)(-1) = +1: ビット列 "11?"
    
    ここで ? は qubit_0 の値（I演算子なので無視）
    """
    total = sum(counts.values())
    
    # +1固有値: 上2ビットが "00" または "11"
    plus_one = (counts.get('000', 0) + counts.get('001', 0) +  # q2=0, q1=0
                counts.get('110', 0) + counts.get('111', 0))   # q2=1, q1=1
    
    # -1固有値: 上2ビットが "01" または "10"
    minus_one = (counts.get('010', 0) + counts.get('011', 0) +  # q2=0, q1=1
                 counts.get('100', 0) + counts.get('101', 0))   # q2=1, q1=0
    
    expectation = (plus_one - minus_one) / total
    
    return {
        'expectation': expectation,
        'plus_one_counts': plus_one,
        'minus_one_counts': minus_one,
        'total': total,
        'detail': f"+1: 00?,11? | -1: 01?,10?"
    }

def print_comparison(label, raw_calc, corrected_val, paper_val):
    """計算結果を比較表示"""
    print(f"\n{BLUE}{BOLD}{'='*70}{RESET}")
    print(f"{BLUE}{BOLD}{label:^70}{RESET}")
    print(f"{BLUE}{BOLD}{'='*70}{RESET}\n")
    
    exp = raw_calc['expectation']
    
    print(f"生データからの計算:")
    print(f"  +1固有値カウント: {raw_calc['plus_one_counts']:,}")
    print(f"  -1固有値カウント: {raw_calc['minus_one_counts']:,}")
    print(f"  期待値: {GREEN}{exp:.6f}{RESET}")
    
    print(f"\n比較:")
    print(f"  生データ計算:           {exp:.6f}")
    print(f"  ghz_final_corrected:    {corrected_val:.6f}  (差: {corrected_val - exp:+.6f})")
    print(f"  論文記載値:             {paper_val:.6f}  (差: {paper_val - exp:+.6f})")
    
    # 差の分析
    diff_corrected = abs(corrected_val - exp)
    diff_paper = abs(paper_val - exp)
    
    if diff_corrected < 0.001:
        print(f"\n{GREEN}✓ ghz_final_corrected は生データ計算と一致{RESET}")
    else:
        print(f"\n{YELLOW}⚠ ghz_final_corrected は生データと {diff_corrected:.4f} ({diff_corrected/exp*100:.2f}%) 異なる{RESET}")
    
    if diff_paper < 0.001:
        print(f"{GREEN}✓ 論文値は生データ計算と一致{RESET}")
    else:
        print(f"{RED}⚠ 論文値は生データと {diff_paper:.4f} ({diff_paper/exp*100:.2f}%) 異なる{RESET}")

def main():
    print(f"\n{BOLD}{'='*70}{RESET}")
    print(f"{BOLD}{'GHZ生データから安定化子期待値を計算':^70}{RESET}")
    print(f"{BOLD}{'='*70}{RESET}")
    
    # データ読み込み
    raw_data = load_raw_data()
    
    # ghz_final_corrected.jsonから値を取得
    with open('data/quantum/ghz_final_corrected.json', 'r', encoding='utf-8') as f:
        corrected_data = json.load(f)
    
    corrected_xxx = corrected_data['stabilizer_expectations']['XXX']
    corrected_zzi = corrected_data['stabilizer_expectations']['ZZI']
    corrected_izz = corrected_data['stabilizer_expectations']['IZZ']
    
    # 論文記載値
    paper_xxx = 0.902
    paper_zzi = 0.914
    paper_izz = 0.924
    
    # 各安定化子の計算
    xxx_result = calculate_xxx_expectation(raw_data['results']['XXX'])
    print_comparison('⟨XXX⟩', xxx_result, corrected_xxx, paper_xxx)
    
    zzi_result = calculate_zzi_expectation(raw_data['results']['ZZI'])
    print_comparison('⟨ZZI⟩', zzi_result, corrected_zzi, paper_zzi)
    
    izz_result = calculate_izz_expectation(raw_data['results']['IZZ'])
    print_comparison('⟨IZZ⟩', izz_result, corrected_izz, paper_izz)
    
    # 安定化子一貫性の計算
    print(f"\n{BLUE}{BOLD}{'='*70}{RESET}")
    print(f"{BLUE}{BOLD}{'安定化子一貫性 S̄':^70}{RESET}")
    print(f"{BLUE}{BOLD}{'='*70}{RESET}\n")
    
    s_bar_raw = (xxx_result['expectation'] + zzi_result['expectation'] + izz_result['expectation']) / 3
    s_bar_corrected = corrected_data['stabilizer_consistency']['value']
    s_bar_paper = 0.908
    
    print(f"生データから: S̄ = {s_bar_raw:.6f}")
    print(f"ghz_final_corrected: S̄ = {s_bar_corrected:.6f}  (差: {s_bar_corrected - s_bar_raw:+.6f})")
    print(f"論文記載値: S̄ = {s_bar_paper:.6f}  (差: {s_bar_paper - s_bar_raw:+.6f})")
    
    # 閾値との比較
    print(f"\n{BOLD}閾値との比較:{RESET}")
    threshold = 0.90
    print(f"  論文の閾値: S̄ ≥ {threshold}")
    
    if s_bar_raw >= threshold:
        print(f"  {GREEN}✓ 生データ計算 ({s_bar_raw:.3f}) は閾値を満たす{RESET}")
    if s_bar_corrected >= threshold:
        print(f"  {GREEN}✓ 補正後データ ({s_bar_corrected:.3f}) は閾値を満たす{RESET}")
    if s_bar_paper >= threshold:
        print(f"  {GREEN}✓ 論文記載値 ({s_bar_paper:.3f}) は閾値を満たす{RESET}")
    
    # サマリー
    print(f"\n{BLUE}{BOLD}{'='*70}{RESET}")
    print(f"{BLUE}{BOLD}{'結論':^70}{RESET}")
    print(f"{BLUE}{BOLD}{'='*70}{RESET}\n")
    
    # 生データとghz_final_correctedの一致度
    avg_diff_corrected = (abs(xxx_result['expectation'] - corrected_xxx) +
                          abs(zzi_result['expectation'] - corrected_zzi) +
                          abs(izz_result['expectation'] - corrected_izz)) / 3
    
    # 生データと論文値の一致度  
    avg_diff_paper = (abs(xxx_result['expectation'] - paper_xxx) +
                      abs(zzi_result['expectation'] - paper_zzi) +
                      abs(izz_result['expectation'] - paper_izz)) / 3
    
    print(f"生データ計算 vs ghz_final_corrected: 平均差 {avg_diff_corrected:.6f} ({avg_diff_corrected/s_bar_raw*100:.2f}%)")
    print(f"生データ計算 vs 論文記載値:          平均差 {avg_diff_paper:.6f} ({avg_diff_paper/s_bar_raw*100:.2f}%)")
    
    if avg_diff_corrected < 0.001:
        print(f"\n{GREEN}✓ ghz_final_corrected.json は生データから正しく計算されています{RESET}")
    else:
        print(f"\n{YELLOW}⚠ ghz_final_corrected.json は生データと異なります（追加処理が適用されている可能性）{RESET}")
    
    if avg_diff_paper > 0.01:
        print(f"{RED}⚠ 論文記載値は生データと約{avg_diff_paper/s_bar_raw*100:.1f}%異なります{RESET}")
        print(f"{RED}  → Readout error mitigation などの補正が適用されている可能性があります{RESET}")
        print(f"{RED}  → この補正方法を文書化する必要があります{RESET}")

if __name__ == '__main__':
    main()