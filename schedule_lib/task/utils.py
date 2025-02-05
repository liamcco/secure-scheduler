import math

def calculate_hyperperiod(tasks) -> int:
    """Calculates the hyperperiod of a set of tasks"""
    periods = [task.period for task in tasks]
    hyperPeriod = 1
    for period in periods:
        hyperPeriod *= period//math.gcd(period, hyperPeriod)
    return hyperPeriod