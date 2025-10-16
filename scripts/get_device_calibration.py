#!/usr/bin/env python3
"""IBM Quantum デバイス較正データ取得スクリプト"""

from qiskit_ibm_runtime import QiskitRuntimeService
import json
from datetime import datetime
import sys
import os

def get_device_calibration(backend_name='ibm_torino', qubits=[54, 61, 62]):
    """デバイス較正データを取得"""
    
    print("=" * 70)
    print("IBM QUANTUM DEVICE CALIBRATION DATA RETRIEVAL")
    print("=" * 70)
    
    service = QiskitRuntimeService(channel="ibm_quantum_platform")
    backend = service.backend(backend_name)
    properties = backend.properties()
    configuration = backend.configuration()
    
    print(f"\n✓ Connected to: {backend_name}")
    print(f"✓ Last update: {properties.last_update_date}")
    
    calibration_data = {
        "metadata": {
            "backend": backend_name,
            "retrieval_date": datetime.now().isoformat(),
            "last_calibration": properties.last_update_date.isoformat(),
            "basis_gates": configuration.basis_gates,
            "n_qubits": configuration.n_qubits
        },
        "qubits": {},
        "gates": {}
    }
    
    print(f"\n📊 Extracting calibration data for qubits: {qubits}")
    
    for qubit in qubits:
        print(f"\n  Qubit {qubit}:")
        
        try:
            t1 = properties.t1(qubit)
            t2 = properties.t2(qubit)
            readout_error = properties.readout_error(qubit)
            readout_length = properties.readout_length(qubit)
            
            print(f"    T1: {t1*1e6:.2f} µs")
            print(f"    T2: {t2*1e6:.2f} µs")
            print(f"    Readout error: {readout_error:.4f}")
            
            qubit_data = {
                "T1": t1,
                "T2": t2,
                "readout_error": readout_error,
                "readout_length": readout_length,
                "gates": {}
            }
            
            # Frequency（オプション）
            try:
                frequency = properties.frequency(qubit)
                qubit_data["frequency"] = frequency
                print(f"    Frequency: {frequency/1e9:.4f} GHz")
            except:
                print(f"    Frequency: Not available")
            
            calibration_data["qubits"][f"Q{qubit}"] = qubit_data
            
            # Single-qubit gate errors
            for gate in ['sx', 'x', 'rz']:
                try:
                    gate_error = properties.gate_error(gate, qubit)
                    gate_length = properties.gate_length(gate, qubit)
                    calibration_data["qubits"][f"Q{qubit}"]["gates"][gate] = {
                        "error": gate_error,
                        "length": gate_length
                    }
                    print(f"    {gate.upper()} gate error: {gate_error:.6f}")
                except:
                    pass
                    
        except Exception as e:
            print(f"    ⚠️ Error: {e}")
            continue
    
    print(f"\n📊 Two-qubit gate calibration:")
    coupling_map = configuration.coupling_map
    for i, qubit1 in enumerate(qubits):
        for qubit2 in qubits[i+1:]:
            if [qubit1, qubit2] in coupling_map or [qubit2, qubit1] in coupling_map:
                try:
                    ecr_error = properties.gate_error('ecr', [qubit1, qubit2])
                    ecr_length = properties.gate_length('ecr', [qubit1, qubit2])
                    
                    gate_key = f"ECR_Q{qubit1}_Q{qubit2}"
                    calibration_data["gates"][gate_key] = {
                        "qubits": [qubit1, qubit2],
                        "error": ecr_error,
                        "length": ecr_length
                    }
                    
                    print(f"  ECR Q{qubit1}-Q{qubit2}:")
                    print(f"    Error: {ecr_error:.6f}")
                    print(f"    Length: {ecr_length*1e9:.2f} ns")
                except Exception as e:
                    print(f"  ECR Q{qubit1}-Q{qubit2}: Not available")
    
    return calibration_data


def save_calibration_data(data, filename="device_calibration.json"):
    """較正データをJSONファイルに保存"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"\n✓ Calibration data saved to: {filename}")


def create_table(data):
    """表を生成"""
    print("\n" + "=" * 70)
    print("DEVICE CALIBRATION TABLE")
    print("=" * 70)
    
    print(f"\nDevice: {data['metadata']['backend']}")
    print(f"Calibration date: {data['metadata']['last_calibration']}")
    
    print("\nQubit Properties:")
    print("-" * 70)
    print(f"{'Qubit':<10} {'T₁ (µs)':<12} {'T₂ (µs)':<12} {'Readout Error':<15}")
    print("-" * 70)
    
    for qubit_name, props in data['qubits'].items():
        t1_us = props['T1'] * 1e6
        t2_us = props['T2'] * 1e6
        ro_error = props['readout_error']
        print(f"{qubit_name:<10} {t1_us:<12.2f} {t2_us:<12.2f} {ro_error:<15.4f}")
    
    print("\n" + "=" * 70)


def main():
    """メイン実行関数"""
    
    try:
        print("\n🔐 IBM Quantum 認証確認中...")
        service = QiskitRuntimeService(channel="ibm_quantum_platform")
        print("✓ IBM Quantum 認証成功")
        
        print("\n📡 デバイス較正データ取得中...")
        calibration_data = get_device_calibration(
            backend_name='ibm_torino',
            qubits=[54, 61, 62]
        )
        
        os.makedirs("data/quantum", exist_ok=True)
        
        save_calibration_data(
            calibration_data,
            filename="data/quantum/device_calibration.json"
        )
        
        create_table(calibration_data)
        
        print("\n" + "=" * 70)
        print("✅ DEVICE CALIBRATION DATA SUCCESSFULLY RETRIEVED!")
        print("=" * 70)
        print("\n次のステップ:")
        print("  1. ファイル確認: data\\quantum\\device_calibration.json")
        print("  2. Git コミット")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ エラー: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())