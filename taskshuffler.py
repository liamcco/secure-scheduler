import random
import multiprocessing

from schedule_lib.taskset.taskset import TaskSet
from schedule_lib.taskset.utils import get_divisors
from schedule_lib.feasibility.tests import RTA, rm_util_bound
from schedule_lib.processor import Processor
from schedule_lib.scheduler import TaskShufflerScheduler
from schedule_lib.analysis import Analysis

hyperperiod = 3000
periods = get_divisors(hyperperiod)

numOfTasks = [5, 7, 9, 11, 13, 15]

utilgroups = [(0.02+0.1*i, 0.08+0.1*i) for i in range(10)]

def create_taskset(U, n):
    while True:
        # Generate taskset with n tasks, pick util random from interval U

        U_aim = random.uniform(U[0], U[1])
        taskset = TaskSet.generate_task_set(n, U_aim, jitter_amount=0.1)
        totalU = sum([task.duration/task.period for task in taskset])
        if U[0] <= totalU <= U[1]:
            if totalU <= rm_util_bound(n) or RTA(taskset, priority_policy="RM"):
                return taskset

def simulate(taskset):
    processor = Processor(1, scheduler=TaskShufflerScheduler)
    processor.load_tasks(taskset)

    success = processor.run(3_000*1000)
    
    if not success:
        return False

    analysis = Analysis(processor)
    totalEntropy = analysis.computeMultiCoreScheduleEntropy()

    U = sum([task.duration/task.period for task in taskset])
    n = len(taskset)

    print(f"{U:.2f},{totalEntropy:.2f},{n}")
    return True

def sub_main(U, n):
    for _ in range(10):
        # Create taskset
        taskset = create_taskset(U, n)

        # Simulate taskset
        simulate(taskset)

def main():
    processes = []
    num_workers = multiprocessing.cpu_count()  # Use all CPU cores
    print(f"Using {num_workers} workers")

    with multiprocessing.Pool(processes=num_workers) as pool:
        for U in utilgroups:
            for n in numOfTasks:
                processes.append(pool.apply_async(sub_main, (U, n)))

        pool.close()  # Prevent new tasks from being submitted
        pool.join()

if __name__ == '__main__':
    main()