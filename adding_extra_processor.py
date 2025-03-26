import random
import multiprocessing

from schedule_lib.taskset.taskset import TaskSet
from schedule_lib.taskset.utils import get_divisors
from schedule_lib.processor import Processor
from schedule_lib.scheduler import TaskShufflerScheduler
from schedule_lib.analysis import Analysis
from schedule_lib.partition.algorithms import PartitionError

hyperperiod = 3000
periods = get_divisors(hyperperiod)

numOfTasksPerCore = [5, 7, 9, 11, 13, 15]

utilgroupsPerCore = [(0.02+0.1*i, 0.08+0.1*i) for i in range(9)]

numOfCores = [4]

def create_taskset(m):
    n = random.choice(numOfTasksPerCore)
    U = random.choice(utilgroupsPerCore)

    U_aim_core = random.uniform(U[0], U[1])
    U_aim = U_aim_core * m

    while True:
        taskset = TaskSet.generate_task_set(n*m, U_aim)
        totalU = sum([task.duration/task.period for task in taskset])
        if U[0] <= totalU/m <= U[1]:
            return taskset

def sub_main():
    while True:
        try:
            m = random.choice(numOfCores)
            taskset = create_taskset(m)
            processor = Processor(m, scheduler=TaskShufflerScheduler)
            processor.load_tasks(taskset)
            break
        except PartitionError:
            pass

    success = processor.run(3_000*10)
    
    if not success:
        return False
    
    processor_extended = Processor(m+1, scheduler=TaskShufflerScheduler)
    processor_extended.load_tasks(taskset)
    success = processor_extended.run(3_000*500)

    analysis = Analysis(processor)
    totalEntropy = analysis.computeMultiCoreScheduleEntropy()
    analysis_extended = Analysis(processor_extended)
    totalEntropy_extended = analysis_extended.computeMultiCoreScheduleEntropy()

    entropy_change = totalEntropy_extended / totalEntropy

    U = sum([task.duration/task.period for task in taskset])
    n = len(taskset)
    m = len(processor.cores)

    print(f"{U/m:.2f},{entropy_change:.2f},{n},{m}")
    return True

def main():
    processes = []
    num_workers = multiprocessing.cpu_count()  # Use all CPU cores
    print(f"Using {num_workers} workers")

    with multiprocessing.Pool(processes=num_workers) as pool:
        for i in range(50):
            processes.append(pool.apply_async(sub_main))

        pool.close()  # Prevent new tasks from being submitted
        pool.join()

if __name__ == '__main__':
    main()