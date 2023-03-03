import datetime
import platform


def perf_test_compute() -> float:
    """How many millions additions per second can this interpreter perform?"""
    cnt_op = 10 ** 6
    time_start = datetime.datetime.now(datetime.timezone.utc)
    for i in range(cnt_op):
        i += 1
    time_end = datetime.datetime.now(datetime.timezone.utc)
    compute_speed = round(cnt_op / (time_end - time_start).total_seconds() / 1e6, 1)
    return compute_speed


def system_info() -> str:
    return f"{platform.python_implementation()} {platform.python_version()} on {platform.system()} {platform.machine()}"
