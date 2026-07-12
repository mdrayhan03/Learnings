import time
import multiprocessing
import os
import sys

def cpu_stress_worker(worker_id: int):
    """Generates continuous arithmetic load to maximize CPU core utilization."""
    print(f"[CPU Worker {worker_id}] Stressing core (PID: {os.getpid()})...")
    # Infinite loop executing high-frequency mathematical evaluations
    while True:
        _ = 123456.789 * 987654.321
        _ = 123456789 % 98765

def memory_stress_worker(target_gb: float, speed_mb_per_sec: float = 100):
    """
    Gradually allocates memory blocks into RAM to simulate heavy data payloads.
    WARNING: Keep target_gb within safe limits of your system to prevent OS crashes!
    """
    print(f"[RAM Worker] Target allocation: {target_gb} GB")
    allocated_chunks = []
    target_bytes = int(target_gb * 1024 * 1024 * 1024)
    chunk_size = int(speed_mb_per_sec * 1024 * 1024) # Allocation chunk speed
    
    current_bytes = 0
    try:
        while current_bytes < target_bytes:
            # Allocate a large block of bytes and force it into physical memory
            dummy_data = b"X" * chunk_size
            allocated_chunks.append(dummy_data)
            current_bytes += chunk_size
            
            print(f"  Allocated: {current_bytes / (1024**3):.2f} GB / {target_gb} GB")
            time.sleep(1.0)
            
        print("[RAM Worker] Target reached. Holding memory allocation allocation loop...")
        while True:
            time.sleep(1)
    except MemoryError:
        print("\n❌ CRITICAL: Hit the OS out-of-memory boundary ceiling early!")
    except KeyboardInterrupt:
        print("\nStopping memory stress worker...")

if __name__ == "__main__":
    print("=" * 50)
    print("      DISTRIBUTED SYSTEM STRESS SIMULATOR")
    print("=" * 50)
    print(f"Detected System CPU Cores: {multiprocessing.cpu_count()}")
    print("Options:\n  1. Stress CPU\n  2. Stress RAM\n")
    
    choice = input("Select stress vector (1 or 2): ").strip()
    
    if choice == "1":
        cores_to_stress = multiprocessing.cpu_count()
        print(f"\nSpawning {cores_to_stress} worker processes to saturate CPU...")
        processes = []
        for i in range(cores_to_stress):
            p = multiprocessing.Process(target=cpu_stress_worker, args=(i,))
            p.start()
            processes.append(p)
        
        try:
            for p in processes:
                p.join()
        except KeyboardInterrupt:
            print("\nTerminating CPU workers...")
            for p in processes:
                p.terminate()

    elif choice == "2":
        try:
            target_allocation = float(input("Enter target memory allocation size in GB: "))
            memory_stress_worker(target_allocation)
        except ValueError:
            print("Invalid number input.")