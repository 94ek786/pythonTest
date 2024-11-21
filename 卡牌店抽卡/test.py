import time

def precise_timer(duration=30, interval=0.1):
    start_time = time.perf_counter()  # 記錄開始時間
    elapsed_time = 0
    
    while elapsed_time < duration:
        print(f"Elapsed time: {elapsed_time:.1f} seconds")
        target_time = start_time + elapsed_time + interval
        while time.perf_counter() < target_time:
            pass  # 忙等待到下一個目標時間
        elapsed_time = time.perf_counter() - start_time

precise_timer()