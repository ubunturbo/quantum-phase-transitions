#!/usr/bin/env python3
import json, sys
from pathlib import Path

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    line = '='*70
    print(f"\n{Colors.BOLD}{Colors.BLUE}{line}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{line}{Colors.RESET}")

class DataValidator:
    def __init__(self):
        self.errors, self.warnings, self.successes = [], [], []
    def check_file_exists(self, filepath):
        if not filepath.exists():
            self.errors.append(f'File not found: {filepath}')
            return False
        self.successes.append(f'Found: {filepath.name}')
        return True
    def check_json_validity(self, filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.successes.append(f'Valid JSON: {filepath.name}')
            return True, data
        except Exception as e:
            self.errors.append(f'Error in {filepath}: {e}')
            return False, None

def validate_classical_data(validator):
    print_header('Validating Classical Ising Data')
    data_dir = Path('data/classical')
    all_valid = True
    for filename in ['ising_L8_results.json', 'ising_L12_results.json', 'ising_L16_results.json']:
        filepath = data_dir / filename
        if not validator.check_file_exists(filepath):
            all_valid = False
            continue
        valid, data = validator.check_json_validity(filepath)
        if not valid:
            all_valid = False
            continue
        if isinstance(data, list) and len(data) > 0:
            required_fields = ['T', 'E', 'M', 'C', 'chi', 'U4']
            first_entry = data[0]
            missing = [f for f in required_fields if f not in first_entry]
            if missing:
                validator.errors.append(f'{filename}: Missing fields: {missing}')
                all_valid = False
            else:
                validator.successes.append(f'{filename}: All required fields present')
    return all_valid

def validate_quantum_data(validator):
    print_header('Validating Quantum GHZ Data')
    data_dir = Path('data/quantum')
    all_valid = True
    for filename in ['ghz_raw_results.json', 'ghz_final_corrected.json', 'device_calibration.json']:
        filepath = data_dir / filename
        if not validator.check_file_exists(filepath):
            all_valid = False
            continue
        valid, data = validator.check_json_validity(filepath)
        if not valid:
            all_valid = False
            continue
        if filename == 'ghz_final_corrected.json' and isinstance(data, dict):
            if 'stabilizer_expectations' in data and 'stabilizer_consistency' in data:
                validator.successes.append(f'{filename}: Stabilizer data present')
                sc = data['stabilizer_consistency']
                if isinstance(sc, dict) and 'value' in sc:
                    s_bar = sc['value']
                    if 0.90 <= s_bar <= 1.0:
                        validator.successes.append(f'S_bar = {s_bar:.4f} in SCR [0.90, 1.0]')
                    else:
                        validator.warnings.append(f'S_bar = {s_bar:.4f} outside SCR')
    return all_valid

def validate_paper_consistency(validator):
    print_header('Validating Consistency with Paper Values')
    ghz_path = Path('data/quantum/ghz_final_corrected.json')
    if not ghz_path.exists():
        validator.errors.append('ghz_final_corrected.json not found')
        return False
    with open(ghz_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    paper_values = {
        'XXX': 0.9020,
        'ZZI': 0.9140,
        'IZZ': 0.9240,
        'stabilizer_consistency': 0.9133,
        'fidelity_lower_bound': 0.9510
    }
    
    for key, paper_val in paper_values.items():
        measured_val = None
        if key in ['XXX', 'ZZI', 'IZZ']:
            if 'stabilizer_expectations' in data and key in data['stabilizer_expectations']:
                measured_val = data['stabilizer_expectations'][key]
        elif key == 'stabilizer_consistency':
            if 'stabilizer_consistency' in data:
                sc = data['stabilizer_consistency']
                if isinstance(sc, dict) and 'value' in sc:
                    measured_val = sc['value']
        elif key == 'fidelity_lower_bound':
            if 'fidelity_lower_bound' in data:
                fl = data['fidelity_lower_bound']
                if isinstance(fl, dict) and 'value' in fl:
                    measured_val = fl['value']
        
        if measured_val is not None:
            rel_diff = abs(measured_val - paper_val) / paper_val * 100
            if rel_diff <= 5:
                validator.successes.append(f'{key}: {measured_val:.4f} vs {paper_val:.4f} (delta={rel_diff:.2f}%)')
            else:
                validator.warnings.append(f'{key}: delta={rel_diff:.2f}% > 5%')
        else:
            validator.warnings.append(f'{key}: not found in data')
    
    return True

def print_summary(validator):
    print_header('Validation Summary')
    total = len(validator.successes) + len(validator.warnings) + len(validator.errors)
    print(f'Total checks: {total}')
    print(f'{Colors.GREEN}Successes: {len(validator.successes)}{Colors.RESET}')
    print(f'{Colors.YELLOW}Warnings: {len(validator.warnings)}{Colors.RESET}')
    print(f'{Colors.RED}Errors: {len(validator.errors)}{Colors.RESET}')
    if validator.errors:
        print(f'\n{Colors.RED}Errors:{Colors.RESET}')
        for e in validator.errors:
            print(f'  {e}')
    if validator.warnings:
        print(f'\n{Colors.YELLOW}Warnings:{Colors.RESET}')
        for w in validator.warnings:
            print(f'  {w}')
    line = '='*70
    print(f'\n{line}')
    if len(validator.errors) == 0:
        print(f'{Colors.GREEN}{Colors.BOLD}ALL VALIDATIONS PASSED!{Colors.RESET}')
        print(f'{Colors.GREEN}Data is ready for publication submission.{Colors.RESET}')
    else:
        print(f'{Colors.RED}VALIDATION FAILED - Fix errors before proceeding{Colors.RESET}')
    print(line)

def main():
    print(f'\n{Colors.BOLD}{Colors.BLUE}COMPREHENSIVE DATA VALIDATION{Colors.RESET}')
    validator = DataValidator()
    validate_classical_data(validator)
    validate_quantum_data(validator)
    validate_paper_consistency(validator)
    print_summary(validator)
    sys.exit(1 if len(validator.errors) > 0 else 0)

if __name__ == '__main__':
    main()
