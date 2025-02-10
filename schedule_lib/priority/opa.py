from schedule_lib.priority.priority import task_sorting_operators

def OPA(tasks, task_order="RM") -> list:
    """Orders task set according to priority policy
    tasks: list of Task objects
    task_order: string,
    return list of Task objects
    """
    prioritzed_tasks = []
    #task_sorting_operators[task_order](tasks)

    for _ in range(len(tasks)):
        candidates = []
        for task in tasks:
            if task.is_ready():
                candidates.append(task)

    return prioritzed_tasks.reverse()