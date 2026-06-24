import threading
import time
import random

class NaiveLogProcessor:
    def process_log(self, log_msg):
        # Simulate log parsing and writing to disk/S3
        time.sleep(random.uniform(0.01, 0.05))
        print(f"💾 [PROCESSED] {log_msg}")

    def ingest_stream(self):
        # Simulating a massive incoming spike of logs
        for i in range(1, 10001):
            # ⚠️ CRITICAL FLAW: Spawning raw threads on the fly!
            # 10,000 threads will overwhelm the OS scheduler and memory limits.
            t = threading.Thread(target=self.process_log, args=(f"Log-Event-ID-{i}",))
            t.start()

# --- Simulation Run ---
processor = NaiveLogProcessor()
# processor.ingest_stream() # Running this will cause a massive resource lag or system freeze!