from schedule_lib.feasibility.tests import RTA
from schedule_lib.priority.priority import task_sorting_operators

def ff(tasks, m, task_order="RM", test=RTA, priority_policy="RM") -> dict:
    """Rate Monotonic First Fit
    tasks: list of Task objects
    m: number of cores
    test: function that tests the feasibility of a list of tasks
    """

    task_sorting_operators[task_order](tasks)
    cores = {id:[] for id in range(m)}
    
    for task in tasks:
        for id in range(m):
            if test(cores[id]+[task], priority_policy=priority_policy):
                cores[id].append(task)
                break
    
    if sum([len(core) for core in cores.values()]) != len(tasks):
        raise Exception("Partitioning failed")
    
    return cores