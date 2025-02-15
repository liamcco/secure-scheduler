import random

from schedule_lib.feasibility.tests import RTA
from schedule_lib.priority.priority import task_sorting_operators

class PartitionError(Exception):
    pass

def check_partition(cores, tasks):
    if sum([len(core) for core in cores.values()]) != len(tasks):
        raise PartitionError("Partitioning failed")


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
    
    check_partition(cores, tasks)
    
    return cores

def nf(tasks, m, task_order="RM", test=RTA, priority_policy="RM") -> dict:
    """Rate Monotonic Next Fit
    tasks: list of Task objects
    m: number of cores
    test: function that tests the feasibility of a list of tasks
    """

    task_sorting_operators[task_order](tasks)
    cores = {id:[] for id in range(m)}

    current_core = 0
    
    for task in tasks:
        if test(cores[current_core]+[task], priority_policy=priority_policy):
            cores[current_core].append(task)
            current_core = (current_core + 1) % m
    
    check_partition(cores, tasks)
    
    return cores

def bf(tasks, m, task_order="RM", test=RTA, priority_policy="RM") -> dict:
    """Rate Monotonic Best Fit
    tasks: list of Task objects
    m: number of cores
    test: function that tests the feasibility of a list of tasks
    """

    task_sorting_operators[task_order](tasks)
    cores = {id:[] for id in range(m)}

    def get_cores_ordered_by_utilization():
        return sorted(cores.items(), key=lambda x: sum([task.duration/task.period for task in x[1]]))
    
    for task in tasks:
        ordered_cores = get_cores_ordered_by_utilization()
        for (id, tasks) in ordered_cores:
            if test(tasks+[task], priority_policy=priority_policy):
                cores[id].append(task)
                break
    
    check_partition(cores, tasks)
    
    return cores

def wf(tasks, m, task_order="RM", test=RTA, priority_policy="RM") -> dict:
    """Rate Monotonic Best Fit
    tasks: list of Task objects
    m: number of cores
    test: function that tests the feasibility of a list of tasks
    """

    task_sorting_operators[task_order](tasks)
    cores = {id:[] for id in range(m)}

    def get_cores_ordered_by_utilization_reverse():
        return sorted(cores.items(), key=lambda x: sum([task.duration/task.period for task in x[1]]), reverse=True)
    
    for task in tasks:
        ordered_cores = get_cores_ordered_by_utilization_reverse()
        for (id, tasks) in ordered_cores:
            if test(tasks+[task], priority_policy=priority_policy):
                cores[id].append(task)
                break
    
    check_partition(cores, tasks)
    
    return cores

def rndf(tasks, m, task_order="RM", test=RTA, priority_policy="RM") -> dict:
    """Rate Monotonic Best Fit
    tasks: list of Task objects
    m: number of cores
    test: function that tests the feasibility of a list of tasks
    """

    task_sorting_operators[task_order](tasks)
    cores = {id:[] for id in range(m)}

    def get_cores_ordered_randomly():
        return sorted(cores.items(), key=lambda x: random.random())
    
    for task in tasks:
        ordered_cores = get_cores_ordered_randomly()
        for (id, tasks) in ordered_cores:
            if test(tasks+[task], priority_policy=priority_policy):
                cores[id].append(task)
                break
    
    check_partition(cores, tasks)
    
    return cores