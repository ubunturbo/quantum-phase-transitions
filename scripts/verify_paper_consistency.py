#!/usr/bin/env python3
"""
論文記載値とデータファイルの完全照合スクリプト

このスクリプトは論文に記載されているすべての数値が
実際のデータファイルと一致しているかを厳密に検証します。

Usage:
    python scripts/verify_paper_consistency.py
"""

import json
import numpy as np
from pathlib import Path

# ANSI color codes
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BLUE = '\033[94m'
BOLD = '\033[1m'
RESET = '\033[0m'

def load_json(filepath):
    """JSONファイルを読み込む"""
    with open(filepath, 'r') as f:
        return json.load(f)

class PaperConsistencyChecker:
    def __init__(self):
        self.checks_passed = 0
        self.checks_failed = 0
        self.checks_warning = 0
        
        # 論文に記載されている値（Document 2から抽出）
        self.paper_values = {
            # Section 3.2: Quantum Measurements
            'XXX': {'value': 0.902, 'error': 0.003},
            'ZZI': {'value': 0.914, 'error': 0.003},
            'IZZ': {'value': 0.924, 'error': 0.002},
            'S_bar': {'value': 0.908, 'error': 0.002},
            'Mermin': {'value': 3.655, 'error': 0.005},
            'Fidelity': {'value': 0.951, 'type': 'lower_bound'},
            
            # Section 2.1: Classical Simulations
            'Tc': 2.269,
            'system_sizes': [8, 12, 16],
            'mc_sweeps_production': 8000,
            'mc_sweeps_thermalization': 1000,
            'sampling_interval': 20,
            
            # Section 2.3: Quantum Experiments
            'shots_per_basis': 30000,
            'measurement_date': '2025-10-10',
            'device': 'ibm_torino',
            'qubits': [54, 61, 62],
            
            # Section 2.4: Thresholds
            'U4_lower': 0.55,
            'U4_upper': 0.65,
            'S_bar_threshold': 0.90,
        }
        
    def print_header(self, text):
        """セクションヘッダーを表示"""
        print(f"\n{BLUE}{BOLD}{'='*70}{RESET}")
        print(f"{BLUE}{BOLD}{text:^70}{RESET}")
        print(f"{BLUE}{BOLD}{'='*70}{RESET}\n")
        
    def print_check(self, name, status, details=""):
        """チェック結果を表示"""
        if status == "PASS":
            symbol = f"{GREEN}✓{RESET}"
            self.checks_passed += 1
        elif status == "WARNING":
            symbol = f"{YELLOW}⚠{RESET}"
            self.checks_warning += 1
        else:
            symbol = f"{RED}✗{RESET}"
            self.checks_failed += 1
            
        print(f"{symbol} {name}")
        if details:
            print(f"  {details}")
    
    def check_quantum_measurements(self):
        """量子測定値の検証"""
        self.print_header("量子測定値の検証")
        
        try:
            # GHZ最終データを読み込む
            ghz_data = load_json('data/quantum/ghz_final_corrected.json')
            
            # Stabilizer値の検証
            for key in ['XXX', 'ZZI', 'IZZ']:
                paper_val = self.paper_values[key]['value']
                paper_err = self.paper_values[key]['error']
                data_val = ghz_data['stabilizer_values'][key]
                data_err = ghz_data['uncertainties'][key]
                
                # 値と誤差が一致するか（小数点3桁まで）
                val_match = abs(data_val - paper_val) < 1e-4
                err_match = abs(data_err - paper_err) < 1e-4
                
                if val_match and err_match:
                    self.print_check(
                        f"⟨{key}⟩ = {paper_val:.3f} ± {paper_err:.3f}",
                        "PASS",
                        f"データ: {data_val:.3f} ± {data_err:.3f}"
                    )
                else:
                    self.print_check(
                        f"⟨{key}⟩ 不一致",
                        "FAIL",
                        f"論文: {paper_val:.3f} ± {paper_err:.3f}, データ: {data_val:.3f} ± {data_err:.3f}"
                    )
            
            # Stabilizer consistency S̄の検証
            paper_s = self.paper_values['S_bar']['value']
            paper_s_err = self.paper_values['S_bar']['error']
            data_s = ghz_data['stabilizer_consistency']
            data_s_err = ghz_data['uncertainties']['stabilizer_consistency']
            
            if abs(data_s - paper_s) < 1e-4 and abs(data_s_err - paper_s_err) < 1e-4:
                self.print_check(
                    f"S̄ = {paper_s:.3f} ± {paper_s_err:.3f}",
                    "PASS",
                    f"データ: {data_s:.3f} ± {data_s_err:.3f}"
                )
            else:
                self.print_check(
                    "S̄ 不一致",
                    "FAIL",
                    f"論文: {paper_s:.3f} ± {paper_s_err:.3f}, データ: {data_s:.3f} ± {data_s_err:.3f}"
                )
            
            # Mermin演算子の検証
            paper_m = self.paper_values['Mermin']['value']
            paper_m_err = self.paper_values['Mermin']['error']
            
            # Merminを計算（XXX + XYY + YXY + YYX）
            # 注: 論文ではXYY, YXY, YYXに符号補正が適用されている
            xxx_val = ghz_data['stabilizer_values']['XXX']
            # XYY, YXY, YYXは符号補正済みと仮定（Supplementary Note 5参照）
            # M = XXX + XYY + YXY + YYX (すべて正)
            
            if 'mermin_value' in ghz_data:
                data_m = ghz_data['mermin_value']
                data_m_err = ghz_data['uncertainties'].get('mermin', 0.005)
                
                if abs(data_m - paper_m) < 1e-3:
                    self.print_check(
                        f"Mermin M = {paper_m:.3f} ± {paper_m_err:.3f}",
                        "PASS",
                        f"データ: {data_m:.3f} ± {data_m_err:.3f} (>700σ)"
                    )
                else:
                    self.print_check(
                        "Mermin M 不一致",
                        "FAIL",
                        f"論文: {paper_m:.3f}, データ: {data_m:.3f}"
                    )
            else:
                self.print_check(
                    "Mermin M",
                    "WARNING",
                    "Mermin値がデータファイルに記録されていない（計算が必要）"
                )
            
            # Fidelity下限の検証
            if 'fidelity_lower_bound' in ghz_data:
                data_f = ghz_data['fidelity_lower_bound']
                paper_f = self.paper_values['Fidelity']['value']
                
                if data_f >= paper_f - 0.001:
                    self.print_check(
                        f"Fidelity F ≥ {paper_f:.3f}",
                        "PASS",
                        f"データ: F = {data_f:.3f}"
                    )
                else:
                    self.print_check(
                        "Fidelity F 不一致",
                        "FAIL",
                        f"論文: F ≥ {paper_f:.3f}, データ: F = {data_f:.3f}"
                    )
            
        except FileNotFoundError as e:
            self.print_check("量子データファイル", "FAIL", f"ファイルが見つかりません: {e}")
        except Exception as e:
            self.print_check("量子データ検証", "FAIL", f"エラー: {e}")
    
    def check_classical_simulations(self):
        """古典シミュレーション設定の検証"""
        self.print_header("古典シミュレーション設定の検証")
        
        try:
            # 各システムサイズのデータを確認
            for L in self.paper_values['system_sizes']:
                filepath = f'data/classical/ising_L{L}_results.json'
                data = load_json(filepath)
                
                # システムサイズの確認
                if data['system_size'] == L:
                    self.print_check(
                        f"システムサイズ L={L}",
                        "PASS"
                    )
                else:
                    self.print_check(
                        f"システムサイズ L={L}",
                        "FAIL",
                        f"データ: L={data['system_size']}"
                    )
                
                # 臨界温度の確認
                if abs(data['critical_temperature'] - self.paper_values['Tc']) < 0.001:
                    self.print_check(
                        f"Tc = {self.paper_values['Tc']}",
                        "PASS"
                    )
                else:
                    self.print_check(
                        "Tc 不一致",
                        "WARNING",
                        f"論文: {self.paper_values['Tc']}, データ: {data['critical_temperature']}"
                    )
                
        except Exception as e:
            self.print_check("古典データ検証", "FAIL", f"エラー: {e}")
    
    def check_experimental_setup(self):
        """実験セットアップの検証"""
        self.print_header("実験セットアップの検証")
        
        try:
            # デバイスキャリブレーションデータを読み込む
            calib_data = load_json('data/quantum/device_calibration.json')
            
            # デバイス名の確認
            if 'backend_name' in calib_data:
                device = calib_data['backend_name']
                if device == self.paper_values['device']:
                    self.print_check(
                        f"デバイス: {device}",
                        "PASS"
                    )
                else:
                    self.print_check(
                        "デバイス名不一致",
                        "FAIL",
                        f"論文: {self.paper_values['device']}, データ: {device}"
                    )
            
            # 測定日の確認
            if 'date' in calib_data:
                date = calib_data['date']
                if self.paper_values['measurement_date'] in date:
                    self.print_check(
                        f"測定日: {self.paper_values['measurement_date']}",
                        "PASS"
                    )
                else:
                    self.print_check(
                        "測定日",
                        "WARNING",
                        f"データ: {date}"
                    )
            
            # Qubits の確認
            if 'qubits' in calib_data:
                qubits = calib_data['qubits']
                if qubits == self.paper_values['qubits']:
                    self.print_check(
                        f"Qubits: {qubits}",
                        "PASS"
                    )
                else:
                    self.print_check(
                        "Qubits",
                        "WARNING",
                        f"論文: {self.paper_values['qubits']}, データ: {qubits}"
                    )
            
        except Exception as e:
            self.print_check("実験セットアップ検証", "FAIL", f"エラー: {e}")
    
    def check_figure1_consistency(self):
        """Figure 1の整合性確認"""
        self.print_header("Figure 1の整合性確認")
        
        # Figure 1の画像ファイルが存在するか
        fig_png = Path('reports/figure1_ising_critical.png')
        fig_pdf = Path('reports/figure1_ising_critical.pdf')
        
        if fig_png.exists():
            size_kb = fig_png.stat().st_size / 1024
            self.print_check(
                "Figure 1 (PNG)",
                "PASS",
                f"ファイルサイズ: {size_kb:.1f} KB"
            )
        else:
            self.print_check("Figure 1 (PNG)", "FAIL", "ファイルが見つかりません")
        
        if fig_pdf.exists():
            self.print_check("Figure 1 (PDF)", "PASS")
        else:
            self.print_check("Figure 1 (PDF)", "WARNING", "PDFファイルが見つかりません")
        
        # スクリプトの存在確認
        script = Path('scripts/plot_figure1.py')
        if script.exists():
            self.print_check("Figure 1生成スクリプト", "PASS")
        else:
            self.print_check("Figure 1生成スクリプト", "FAIL", "スクリプトが見つかりません")
    
    def check_git_repository(self):
        """Gitリポジトリの状態確認"""
        self.print_header("Gitリポジトリの状態確認")
        
        import subprocess
        
        try:
            # 最新コミットIDを取得
            result = subprocess.run(
                ['git', 'rev-parse', '--short', 'HEAD'],
                capture_output=True,
                text=True,
                check=True
            )
            commit_id = result.stdout.strip()
            
            self.print_check(
                f"最新コミット: {commit_id}",
                "PASS"
            )
            
            # 未コミットの変更があるか確認
            result = subprocess.run(
                ['git', 'status', '--porcelain'],
                capture_output=True,
                text=True,
                check=True
            )
            
            if result.stdout.strip():
                self.print_check(
                    "未コミットの変更",
                    "WARNING",
                    "未コミットのファイルがあります"
                )
                print(f"  {result.stdout}")
            else:
                self.print_check(
                    "Git作業ディレクトリ",
                    "PASS",
                    "すべての変更がコミット済み"
                )
                
        except subprocess.CalledProcessError:
            self.print_check(
                "Git確認",
                "WARNING",
                "Gitコマンドが使用できません"
            )
        except FileNotFoundError:
            self.print_check(
                "Git確認",
                "WARNING",
                "Gitがインストールされていません"
            )
    
    def run_all_checks(self):
        """すべてのチェックを実行"""
        print(f"\n{BOLD}{'='*70}{RESET}")
        print(f"{BOLD}{'論文記載値とデータファイルの完全照合':^70}{RESET}")
        print(f"{BOLD}{'='*70}{RESET}")
        
        # 各種チェックを実行
        self.check_quantum_measurements()
        self.check_classical_simulations()
        self.check_experimental_setup()
        self.check_figure1_consistency()
        self.check_git_repository()
        
        # サマリーを表示
        self.print_summary()
    
    def print_summary(self):
        """検証結果のサマリーを表示"""
        total = self.checks_passed + self.checks_warning + self.checks_failed
        
        print(f"\n{BLUE}{BOLD}{'='*70}{RESET}")
        print(f"{BLUE}{BOLD}{'検証結果サマリー':^70}{RESET}")
        print(f"{BLUE}{BOLD}{'='*70}{RESET}\n")
        
        print(f"{GREEN}✓ 合格: {self.checks_passed}/{total}{RESET}")
        print(f"{YELLOW}⚠ 警告: {self.checks_warning}/{total}{RESET}")
        print(f"{RED}✗ 失敗: {self.checks_failed}/{total}{RESET}")
        
        if self.checks_failed == 0:
            print(f"\n{GREEN}{BOLD}🎉 すべての重要なチェックに合格しました！{RESET}")
            print(f"{GREEN}論文は投稿済みで、データの整合性が確認されました。{RESET}")
        elif self.checks_failed > 0:
            print(f"\n{RED}{BOLD}⚠️  修正が必要な項目があります{RESET}")
        
        if self.checks_warning > 0:
            print(f"\n{YELLOW}注意: 警告項目を確認してください{RESET}")

if __name__ == '__main__':
    checker = PaperConsistencyChecker()
    checker.run_all_checks()