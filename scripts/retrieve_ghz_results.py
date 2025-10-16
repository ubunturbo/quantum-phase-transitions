"""
IBM Quantum Job結果取得スクリプト
================================
Job ID: d3kfathfk6qs73emfrb0 からGHZ測定結果を取得
"""

import json
from qiskit_ibm_runtime import QiskitRuntimeService

# IBM Quantum接続
print("🔐 IBM Quantumに接続中...")
service = QiskitRuntimeService()

# Job ID指定
job_id = "d3kfathfk6qs73emfrb0"

try:
    # Jobを取得
    print(f"📡 Job {job_id} を取得中...")
    job = service.job(job_id)
    
    status = job.status()
    print(f"✓ Job ステータス: {status}")
    
    # 結果取得
    # job.status() は既に文字列を返す（Qiskit Runtime の新API）
    if status == "DONE":
        print("✓ Job完了 - 結果を取得中...")
        result = job.result()
        
        # 測定結果の構造を確認
        print("\n" + "="*70)
        print("結果の構造確認:")
        print("="*70)
        
        # Qiskit Runtime の新しいAPI対応
        # result は PrimitiveResult または PubResult のリスト
        print(f"Result type: {type(result)}")
        print(f"Number of pub results: {len(result)}")
        
        # 各回路の結果を取得
        all_counts = []
        
        for i, pub_result in enumerate(result):
            print(f"\n--- Circuit {i} ---")
            print(f"Data type: {type(pub_result.data)}")
            
            # DataBin から counts を取得する新しい方法
            # Qiskit Runtime 0.15+ では data.c または data.meas の代わりに
            # 直接 data 属性から BitArray を取得
            try:
                # 方法1: BitArray から counts を生成
                if hasattr(pub_result.data, 'c'):
                    bit_array = pub_result.data.c
                    counts = bit_array.get_counts()
                    print(f"✓ Counts (method 1): {counts}")
                    all_counts.append(counts)
                # 方法2: meas 属性を試す
                elif hasattr(pub_result.data, 'meas'):
                    bit_array = pub_result.data.meas
                    counts = bit_array.get_counts()
                    print(f"✓ Counts (method 2): {counts}")
                    all_counts.append(counts)
                # 方法3: 直接 BitArray を取得
                else:
                    # すべての属性をチェック
                    print(f"Available attributes: {dir(pub_result.data)}")
                    
                    # 最初の BitArray 属性を見つける
                    for attr_name in dir(pub_result.data):
                        if not attr_name.startswith('_'):
                            attr = getattr(pub_result.data, attr_name)
                            if hasattr(attr, 'get_counts'):
                                counts = attr.get_counts()
                                print(f"✓ Counts (method 3, attr={attr_name}): {counts}")
                                all_counts.append(counts)
                                break
            
            except Exception as e:
                print(f"⚠️ Error getting counts for circuit {i}: {e}")
                # デバッグ情報
                print(f"Data attributes: {dir(pub_result.data)}")
        
        # 結果を保存
        if all_counts:
            print("\n" + "="*70)
            print("📊 測定結果サマリー:")
            print("="*70)
            
            basis_labels = ["XXX", "ZZI", "IZZ", "XYY+YXY+YYX", "ZZZ"]
            
            for i, (label, counts) in enumerate(zip(basis_labels, all_counts)):
                print(f"\n{label} basis:")
                # 上位5件を表示
                sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
                for bitstring, count in sorted_counts[:5]:
                    print(f"  {bitstring}: {count} ({count/30000*100:.2f}%)")
            
            # JSON保存
            output_data = {
                "job_id": job_id,
                "backend": "ibm_torino",
                "qubits": [54, 61, 62],
                "shots": 30000,
                "measurement_date": job.creation_date.isoformat(),
                "results": {
                    basis_labels[i]: counts 
                    for i, counts in enumerate(all_counts)
                }
            }
            
            output_file = "data/quantum/ghz_raw_results.json"
            with open(output_file, 'w') as f:
                json.dump(output_data, f, indent=2)
            
            print(f"\n✅ 結果を保存: {output_file}")
            
        else:
            print("\n⚠️ カウントデータを取得できませんでした")
            print("結果の生データを確認してください:")
            print(result)
    
    elif status in ["QUEUED", "RUNNING"]:
        print(f"⏳ Job実行中... ステータス: {status}")
        print("後でもう一度実行してください")
    
    else:
        print(f"⚠️ Job ステータス異常: {status}")
        print("詳細:", job.error_message() if hasattr(job, 'error_message') else "N/A")

except Exception as e:
    print(f"❌ エラー発生: {e}")
    print("\n詳細:")
    import traceback
    traceback.print_exc()
    
    print("\n💡 トラブルシューティング:")
    print("1. Job IDが正しいか確認")
    print("2. IBM Quantum認証が有効か確認")
    print("3. Jobの保存期限が切れていないか確認（通常180日）")

print("\n" + "="*70)
print("実行完了")
print("="*70)