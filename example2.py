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

def perform_response_time_test(taskset):
    # calculate responsetime for all tasks and compare to deadline
    return RTA(taskset, priority_policy="RM")

def debug_taskset(taskset):
    print("_"*30)
    print()
    print("{")
    for task in taskset:
        print(f"-\tPeriod: {task.period}\t Execution Time: {task.duration}")
    print("}")
    print()

def simulate(taskset):
    processor = Processor(1, scheduler=TaskShufflerScheduler)
    processor.load_tasks(taskset)

    success = processor.run(3_000*1_000)
    
    if not success:
        debug_taskset(taskset)
        return False

    analysis = Analysis(processor.simulation[0])
    totalEntropy = analysis.computeScheduleEntropy()

    U = sum([task.duration/task.period for task in taskset])
    n = len(taskset)

    print(f"U = {U:.2f} ==> Entropy = {totalEntropy} (n = {n})")

    return True

for U in utilgroups:
    for n in numOfTasks:
        for j in range(5):
            while True:
                U_aim = U[0] + (U[1]-U[0])/2
                taskset = TaskSet.generate_task_set(n, U_aim)
                totalU = sum([task.duration/task.period for task in taskset])
                if U[0] <= totalU <= U[1]:
                    if totalU <= rm_util_bound(n) or perform_response_time_test(taskset):
                        simulate(taskset)
                        break