from schedule_lib.feasibility.tests import response_time
from schedule_lib.feasibility.tests import UnfeasibleTaskset

def OPA(tasks) -> list:
    """Orders task set according to priority policy
    tasks: list of Task objects
    return ordered list of Task objects
    """
    prioritzed_tasks = []
    tasks = tasks[:]

    for _ in range(len(tasks)):
        for task_to_try in tasks:
            # Create task set
            set_to_test = tasks[:]
            set_to_test.remove(task_to_try)
            try:
                response_time(set_to_test[task_to_try])
            except UnfeasibleTaskset:
                continue
            prioritzed_tasks.append(task_to_try)
            tasks.remove(task_to_try)
            break

    return prioritzed_tasks.reverse()