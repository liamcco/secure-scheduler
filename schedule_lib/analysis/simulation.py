from math import gcd
from functools import reduce

# LCM of task periods from list of tasks
def lcm(tasks):
    return reduce(lambda x, y: x*y//gcd(x, y), [task.period for task in tasks])