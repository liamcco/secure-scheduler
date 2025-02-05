import math

from schedule_lib.priority.priority import task_sorting_operators

def RTA(tasks, priority_policy="RM") -> bool:
    """Analyzes taskset according to priority policy
    tasks: list of Task objects
    priority_policy: string,
    return True if taskset is feasible, False otherwise
    """

    task_sorting_operators[priority_policy](tasks)
    
    approved_tasks = []
    for task in tasks:
        wcrt_guess = task.duration
        while True:
            wcrt = wcrt_guess
            wcrt_guess = task.duration + sum([math.ceil(wcrt/task.period)*task.duration for task in approved_tasks])

            if (wcrt_guess>task.deadline):
                print(f"{task} will miss deadline")
                return False
            
            if wcrt_guess == wcrt:
                break

        approved_tasks.append(task)
    return True