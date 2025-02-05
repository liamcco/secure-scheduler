from schedule_lib.taskset.taskset import TaskSet
import schedule_lib
import schedule_lib.scheduler
import schedule_lib.scheduler.utils

def perform_response_time_test(taskset):
    # prioritze taskset
    tasks = sorted(taskset, key=lambda x: x.period)
    for i, task in enumerate(taskset):
        task.priority = i

    # calculate responsetime for all tasks and compare to deadline
    for task in tasks:
        try:
            schedule_lib.scheduler.utils.worst_case_response_time(task, tasks)
        except:
            return False

    return True

def debug_taskset(taskset):
    print("_"*30)
    print()
    print("{")
    for task in taskset:
        print(f"-\tPeriod: {task.period}\t Execution Time: {task.duration}")
    print("}")
    print()
    perform_response_time_test(taskset)

def simulate(taskset):
    scheduler = schedule_lib.Scheduler(taskset)

    simulation = schedule_lib.Simulation(scheduler)

    try:
        simulation.run(3_000*1_00)
    except:
        debug_taskset(taskset)
        return False

    analysis = schedule_lib.Analysis()
    data = simulation.simulation
    totalEntropy = analysis.computeScheduleEntropy(data)

    U = sum([task.duration/task.period for task in taskset])
    n = len(taskset)

    print(f"U = {U:.2f} ==> Entropy = {totalEntropy} (n = {n})")

    return True

for U in TaskSet.utilgroups[9:]:
    for n in TaskSet.numOfTasks:
        for j in range(5):
            while True:
                U_aim = U[0] + (U[1]-U[0])/2
                taskset = TaskSet.generate_task_set(n, U_aim)
                totalU = sum([task.duration/task.period for task in taskset])
                if U[0] <= totalU <= U[1]:
                    if totalU <= TaskSet.rm_util_bound(n) or perform_response_time_test(taskset):
                        simulate(taskset)
                        break