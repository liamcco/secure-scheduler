import math

def sort_tasks_by_priority(tasks):
    return sorted(tasks, key=lambda x: x.priority)

def hp_i_of_tasks(task_i, tasks):
    sorted_tasks = sort_tasks_by_priority(list(tasks))
    hpi_index = sorted_tasks.index(task_i)
    return sorted_tasks[:hpi_index]

def lp_i_of_tasks(task_i, tasks):
    sorted_tasks = sort_tasks_by_priority(list(tasks))
    lpi_index = sorted_tasks.index(task_i)
    return sorted_tasks[lpi_index+1:]

def worst_case_response_time(task_i, tasks):
    hp_i = hp_i_of_tasks(task_i, tasks)

    wcrt_guess = task_i.duration
    while True:
        wcrt = wcrt_guess
        wcrt_guess = task_i.duration + sum([math.ceil(wcrt/task.period)*task.duration for task in hp_i])
        if wcrt_guess == wcrt:
            return wcrt

def upper_bound_interference_from_hp(task_i, tasks):
    hp_i = hp_i_of_tasks(task_i, tasks)

    return sum([(math.ceil(task_i.deadline/task.period)+1)*task.duration for task in hp_i])

def worst_case_maximum_inversion_budget(task_i, tasks):
    return task_i.deadline - (task_i.duration + upper_bound_interference_from_hp(task_i, tasks))

def minimum_inversion_priority(task_i, tasks):
    lp_i = lp_i_of_tasks(task_i, tasks)
    considered_tasks = [task for task in lp_i if worst_case_maximum_inversion_budget(task, tasks) < 0]
    if len(considered_tasks) == 0:
        return len(tasks)
    else:
        return min([task.priority for task in considered_tasks])
    
def next_schedule_decision_to_be_made(task_i, ready_queue):
    hp_i = hp_i_of_tasks(task_i, ready_queue)
    return min([worst_case_maximum_inversion_budget(task, hp_i) for task in hp_i])