import random
from schedule_lib.task.task import Task

class TaskSet:

    hyperperiod = 3000
    numOfTasks = [5, 7, 9, 11, 13, 15]
    utilgroups = [(0.02+0.1*i, 0.08+0.1*i) for i in range(10)]
    periods = sorted({d for i in range(1, int(3000**0.5) + 1) if 3000 % i == 0 for d in (i, 3000 // i)})

    def rm_util_bound(n):
        return n*(2**(1/n) - 1)

    def get_divisors(n):
        """Returns all divisors of n."""
        return sorted({d for i in range(1, int(n**0.5) + 1) if n % i == 0 for d in (i, n // i)})

    def u_uni_fast(n, U):
        """Generates a set of n utilizations that sum to U using the UUniFast algorithm."""
        sumU = U
        utils = []
        for i in range(n - 1):
            nextSumU = sumU * random.random() ** (1 / (n - i))
            utils.append(sumU - nextSumU)
            sumU = nextSumU
        utils.append(sumU)  # Last task gets remaining utilization
        return utils

    def generate_task_set(n, U, period_limit=3000, duration_range=(1, 50)):
        """Generates a task set where execution times are randomly chosen, and periods are calculated."""
        
        # Generate task utilizations
        utils = TaskSet.u_uni_fast(n, U)
        
        # Get valid periods (must be a divisor of period_limit)
        valid_periods = TaskSet.get_divisors(period_limit)
        
        task_set = []
        
        for util in utils:
            # Randomly choose an execution time (duration) within the range
            execution_time = random.randint(*duration_range)
            
            # Calculate the required period to satisfy U = C / T => T = C / U
            period = round(execution_time / util)
            
            # Find the closest valid period (must be a divisor of period_limit)
            period = min(valid_periods, key=lambda p: abs(p - period))
            valid_periods.remove(period)
            
            task_set.append(Task(period,execution_time))
        
        return task_set







