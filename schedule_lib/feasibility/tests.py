import math

from schedule_lib.priority.priority import task_sorting_operators

class UnfeasibleTaskset(Exception):
    pass

def rm_util_bound(n):
    return n*(2**(1/n) - 1)

def RTA(tasks, priority_policy="RM") -> bool:
    """Analyzes taskset according to priority policy
    tasks: list of Task objects
    priority_policy: string,
    return True if taskset is feasible, False otherwise
    """

    task_sorting_operators[priority_policy](tasks)
    
    approved_tasks = []
    for task in tasks:
        try:
            response_time(task, approved_tasks)
        except UnfeasibleTaskset:
            return False

        approved_tasks.append(task)
    return True

def response_time(task, task_set, include_jitter=True) -> bool:
    """Calculates response time of task in task_set
    task: Task object
    task_set: hp(task)
    return response time of task
    """
    wcrt_guess = task.duration
    while True:
        wcrt = wcrt_guess
        wcrt_guess = task.duration + sum([math.ceil((wcrt+t.max_jitter)/t.period)*t.duration for t in task_set])

        if (wcrt_guess>task.deadline):
            raise UnfeasibleTaskset(f"{task} will miss deadline")

        if wcrt_guess == wcrt:
            break

    return wcrt