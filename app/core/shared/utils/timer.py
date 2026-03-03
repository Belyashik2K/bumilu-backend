import time


def start_timer() -> float:
    return time.perf_counter()


def stop_timer(start_time: float) -> int:
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    return int(elapsed_time * 1000)
