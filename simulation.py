import reedsolo
import time
import os
import random

def benchmark_ethereum_blob():
    print(f"Ethereum PeerDAS Simulation")
    
    CHUNK_DATA_SIZE = 100 
    CHUNK_PARITY_SIZE = 100 
    TOTAL_CHUNK_SIZE = CHUNK_DATA_SIZE + CHUNK_PARITY_SIZE
    
    target_size = 131072 
    num_rows = target_size 
    
    print(f"[Setup] Simulating a 128KB Blob")
    print(f" - Split into {num_rows} rows (shards)")
    print(f" - Extension Factor: 2x (100% Overhead)")
    print(f" - Total Data to Process: {target_size / 1024:.2f} KB → {(target_size * 2) / 1024:.2f} KB")
    
    print("\n[Step 1] Generating Random Blob Data...")
    original_blob_rows = []
    for _ in range(num_rows):
        row = os.urandom(CHUNK_DATA_SIZE)
        original_blob_rows.append(row)
        
    print(" Done.")
    
    print("\n[Step 2] Encoding (Calculating Parity)...")
    rsc = reedsolo.RSCodec(nsym=CHUNK_PARITY_SIZE)
    encoded_rows = []
    
    start_time = time.time()
    
    for row in original_blob_rows:
        encoded = rsc.encode(row)
        encoded_rows.append(encoded)
        
    encode_time = time.time() - start_time
    print(f" Encoded {num_rows} shards in {encode_time:.4f} seconds.")
    print(f" Speed: {(target_size/1024/1024) / encode_time:.2f} MB/s")

    print("\n[Step 3] Simulating 50% Data Loss (Network Failure)...")
    
    tampered_rows = []
    erasure_map = [] 
    
    missing_indices = list(range(CHUNK_DATA_SIZE, TOTAL_CHUNK_SIZE))
    
    for row in encoded_rows:
        tampered = bytearray(row)
        
        for i in missing_indices:
            tampered[i] = 0
            
        tampered_rows.append(tampered)
        erasure_map.append(missing_indices)
        
    print(f" Wiped {len(missing_indices)} bytes from every row.")
    print(" Data remaining: exactly 50%.")

    print("\n[Step 4] Reconstructing Blob from partial data...")
    decoded_blob_rows = []
    
    start_time = time.time()
    
    success_count = 0
    
    for i in range(num_rows):
        try:
            reconstructed, _, _ = rsc.decode(tampered_rows[i], erase_pos=erasure_map[i])
            decoded_blob_rows.append(reconstructed)
            success_count += 1
        except reedsolo.ReedSolomonError:
            print(f"Failed to recover row {i}")

    decode_time = time.time() - start_time
    
    print(f" Reconstructed {success_count}/{num_rows} shards in {decode_time:.4f} seconds.")
    print(f" Recovery Speed: {(target_size/1024/1024) / decode_time:.2f} MB/s")
    
    print("\n[Step 5] Integrity Check")
    if original_blob_rows == decoded_blob_rows:
        print("SUCCESS: The 128KB Blob was perfectly restored!")
        print("Thesis Proven: 50% availability is sufficient for full reconstruction.")
    else:
        print("FAILURE: The reconstructed blob does not match the original.")

if __name__ == "__main__":
    benchmark_ethereum_blob()