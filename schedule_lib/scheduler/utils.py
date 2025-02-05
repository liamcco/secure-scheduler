import math
import random

def hp_i_of_tasks(task_i, tasks):
    """Filters `tasks` to return a list of tasks with priority higher than `task_i`
    --> Requires that all tasks has a priority attribute <--
    """
    return [task for task in tasks if task.priority < task_i.priority]

def lp_i_of_tasks(task_i, tasks):
    """Filters `tasks` to return a list of tasks with priority less than `task_i`
    --> Requires that all tasks has a priority attribute <-- 
    """
    return [task for task in tasks if task.priority > task_i.priority]

def upper_bound_interference_from_hp(task_i, tasks) -> int:
    """Calculates the upper bound of interference from higher priority tasks"""
    hp_i = hp_i_of_tasks(task_i, tasks)
    return sum([(math.ceil(task_i.deadline/task.period)+1)*task.duration for task in hp_i])

def worst_case_maximum_inversion_budget(task_i, tasks) -> int:
    """Calculates the worst case maximum inversion budget of `task_i`"""
    return task_i.deadline - (task_i.duration + upper_bound_interference_from_hp(task_i, tasks))

def minimum_inversion_priority(task_i, tasks) -> int:
    """Calculates the minimum inversion priority of `task_i`"""
    lp_i = lp_i_of_tasks(task_i, tasks)
    considered_tasks = [task for task in lp_i if worst_case_maximum_inversion_budget(task, tasks) < 0]
    if len(considered_tasks) == 0:
        return math.inf # Arbitrarily low priority
    else:
        return min([task.priority for task in considered_tasks]) # max priority

def next_schedule_decision_to_be_made(task_s, ready_tasks) -> int:
    """Calculates the next schedule decision to be made"""
    hp_s = hp_i_of_tasks(task_s, ready_tasks)
    max = min([task.remaining_inversion_budget for task in hp_s])
    remaining = task_s.remaining_execution_time
    new_max = min(max, remaining)

    return random.randint(1, new_max)