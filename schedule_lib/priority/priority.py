

task_sorting_operators = {
    "RM": lambda task_set: task_set.sort(key=lambda t: t.period),
    "RRM": lambda task_set: task_set.sort(key=lambda t: t.period, reverse=True),
    "DM": lambda task_set: task_set.sort(key=lambda t: t.deadline),
    "IU": lambda task_set: task_set.sort(key=lambda t: t.duration/t.period),
    "DU": lambda task_set: task_set.sort(key=lambda t: t.duration/t.period, reverse=True),
    "SlackMonotonic": lambda task_set: task_set.sort(key=lambda t: t.period - t.duration),
    "RevSlackMonotonic": lambda task_set: task_set.sort(key=lambda t: t.period - t.duration, reverse=True),
}