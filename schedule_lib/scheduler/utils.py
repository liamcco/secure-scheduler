import math
import random

# Filters `tasks` to return a list of tasks with priority higher than `task_i`
def hp_i_of_tasks(task_i, tasks):
    hp_i = [task for task in tasks if task.priority < task_i.priority]
    return hp_i

# Filters `tasks` to return a list of tasks with priority less than `task_i`
def lp_i_of_tasks(task_i, tasks):
    lp_i = [task for task in tasks if task.priority > task_i.priority]
    return lp_i

# Iterately calculates the worst case response time of `task_i` until it converges
def worst_case_response_time(task_i, tasks):
    hp_i = hp_i_of_tasks(task_i, tasks)

    wcrt_guess = task_i.duration
    while True:
        wcrt = wcrt_guess
        wcrt_guess = task_i.duration + sum([math.ceil(wcrt/task.period)*task.duration for task in hp_i])
        if wcrt_guess == wcrt:
            return wcrt

# Calculates the upper bound of interference from higher priority tasks
def upper_bound_interference_from_hp(task_i, tasks):
    hp_i = hp_i_of_tasks(task_i, tasks)

    return sum([(math.ceil(task_i.deadline/task.period)+1)*task.duration for task in hp_i])

# Calculates the worst case maximum inversion budget of `task_i`
def worst_case_maximum_inversion_budget(task_i, tasks):
    return task_i.deadline - (task_i.duration + upper_bound_interference_from_hp(task_i, tasks))

# Calculates the minimum inversion priority of `task_i`
def minimum_inversion_priority(task_i, tasks):
    lp_i = lp_i_of_tasks(task_i, tasks)
    considered_tasks = [task for task in lp_i if worst_case_maximum_inversion_budget(task, tasks) < 0]
    if len(considered_tasks) == 0:
        return math.inf # Arbitrarily low priority
    else:
        return min([task.priority for task in considered_tasks])

# Determines when the next schedule decision should be made
def next_schedule_decision_to_be_made(task_s, ready_tasks):
    hp_s = hp_i_of_tasks(task_s, ready_tasks)
    # ? Doesn't take remaining execution time into account -> Sqews the random selection
    max = min([task.remaining_inversion_budget for task in hp_s])
    return random.randint(1, max)

# Calculates the hyperperiod of tasks in `tasks`
def calculate_hyperperiod(tasks):
    periods = [task.period for task in tasks]
    hyperPeriod = 1
    for period in periods:
        hyperPeriod *= period//math.gcd(period, hyperPeriod)
    return hyperPeriod