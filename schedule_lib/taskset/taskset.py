import random
import math

import numpy as np

from schedule_lib.task.jittertask import JitterTask
from schedule_lib.taskset.utils import get_divisors

class TaskSet:
    """A class to generate task sets."""

    def u_uni_fast(n, U):
        """Generates a set of n utilizations that sum to U 
        using the UUniFast algorithm.
        """
        
        sumU = U
        utils = []
        for i in range(n - 1):
            nextSumU = sumU * random.random() ** (1 / (n - i))
            utils.append(sumU - nextSumU)
            sumU = nextSumU
        utils.append(sumU)  # Last task gets remaining utilization
        return utils

    def generate_task_set(n, U=0.5, hyper_period=3000, execution_time_range=(1, 50), jitter_amount=0):
        """Generates a task set with a given:
        - number of tasks, n
        - total utilization, U
        - hyper period, hyper_period (optional),
        - range of execution time, duration_range (optional)
        """
        
        # Generate task utilizations
        # utils = TaskSet.u_uni_fast(n, U)
        utils = TaskSet.randfixedsum(n, U)
        
        # Get valid periods (must be a divisor of period_limit)
        valid_periods = get_divisors(hyper_period)
        
        task_set = []
        
        for util in utils:
            # Randomly choose the execution time
            execution_time = random.randint(*execution_time_range)
            
            # Calculate the required period to satisfy U = C / T => T = C / U
            period = round(execution_time / util)
            
            # Find the closest valid period (must be a divisor of period_limit)
            period = min(valid_periods, key=lambda p: abs(p - period))
            
            task_set.append(JitterTask(period,execution_time, jitter_amount=jitter_amount))
        
        return task_set

    def randfixedsum(n,u,m=1,a=0,b=1): # -> [x]

        # [x,v] = randfixedsum(n,m,s,a,b)
        #
        #   This generates an n by m array x, each of whose m columns
        # contains n random values lying in the interval [a,b], but
        # subject to the condition that their sum be equal to s.  The
        # scalar value s must accordingly satisfy n*a <= s <= n*b.  The
        # distribution of values is uniform in the sense that it has the
        # conditional probability distribution of a uniform distribution
        # over the whole n-cube, given that the sum of the x's is s.
        #
        #   The scalar v, if requested, returns with the total
        # n-1 dimensional volume (content) of the subset satisfying
        # this condition.  Consequently if v, considered as a function
        # of s and divided by sqrt(n), is integrated with respect to s
        # from s = a to s = b, the result would necessarily be the
        # n-dimensional volume of the whole cube, namely (b-a)^n.
        #
        #   This algorithm does no "rejecting" on the sets of x's it
        # obtains.  It is designed to generate only those that satisfy all
        # the above conditions and to do so with a uniform distribution.
        # It accomplishes this by decomposing the space of all possible x
        # sets (columns) into n-1 dimensional simplexes.  (Line segments,
        # triangles, and tetrahedra, are one-, two-, and three-dimensional
        # examples of simplexes, respectively.)  It makes use of three
        # different sets of 'rand' variables, one to locate values
        # uniformly within each type of simplex, another to randomly
        # select representatives of each different type of simplex in
        # proportion to their volume, and a third to perform random
        # permutations to provide an even distribution of simplex choices
        # among like types.  For example, with n equal to 3 and s set at,
        # say, 40% of the way from a towards b, there will be 2 different
        # types of simplex, in this case triangles, each with its own
        # area, and 6 different versions of each from permutations, for
        # a total of 12 triangles, and these all fit together to form a
        # particular planar non-regular hexagon in 3 dimensions, with v
        # returned set equal to the hexagon's area.
        #
        # Roger Stafford - Jan. 19, 2006

        # Check the arguments.
        if (m != round(m)) | (n != round(n)) | (m < 0) | (n < 1):
            raise ValueError('n must be a whole number and m a non-negative integer.')
        elif (u < n*a) | (u > n*b) | (a >= b):
            raise ValueError('Inequalities n*a <= s <= n*b and a < b must hold.')

        # Rescale to a unit cube: 0 <= x(i) <= 1
        u = (u - n*a) / (b - a)

        # Construct the transition probability table, t.
        # t(i,j) will be utilized only in the region where j <= i + 1.
        k = max(min(math.floor(u), n-1), 0) # Must have 0 <= k <= n-1
        u = max(min(u, k+1), k) # Must have k <= s <= k+1
        u1 = u - np.arange(k, k - n, -1)  # u1 & u2 will never be negative
        u2 = np.arange(k + n, k, -1) - u

        # Initialize probability table
        w = np.zeros((n, n + 1))
        w[0, 1] = np.finfo(float).max  # Equivalent of MATLAB's realmax
        t = np.zeros((n - 1, n))

        # Compute transition probabilities
        tiny = 2 ** -1074  # Smallest positive float

        for i in range(1, n):
            tmp1 = w[i - 1, 1:i + 1] * u1[:i] / (i + 1)
            tmp2 = w[i - 1, :i] * u2[n - i:n] / (i + 1)
            w[i, 1:i + 1] = tmp1 + tmp2
            tmp3 = w[i, 1:i + 1] + tiny  # Avoid division by zero
            tmp4 = (u2[n - i:] > u1[:i])
            t[i - 1, :i] = (tmp2 / tmp3) * tmp4 + (1 - tmp1 / tmp3) * (~tmp4)

        # Derive the polytope volume v from the appropriate
        # element in the bottom row of w.
        #   v = (n ** (3 / 2)) * (w[n - 1, k + 1] / np.finfo(float).max) * (b - a) ** (n - 1)

        # Now compute the matrix x.
        # Generate random numbers
        x = np.zeros((n, m))
        if m == 0:
            return x #, v  # Return empty array if m is zero
        rt = np.random.rand(n - 1, m)  # Random selection of simplex type
        ru = np.random.rand(n - 1, m)  # Random location within simplex
        u = np.full(m, u)
        j = np.full(m, k + 1, dtype=int) # For indexing in the t table
        um = np.zeros(m) 
        pr = np.ones(m) # Start with sum zero & product 1

        for i in range(n - 1, 0, -1): # Work backwards in the t table
            e = (rt[n - i - 1, :] <= t[i - 1, j - 1])  # Use rt to choose a transition
            ux = ru[n - i - 1, :] ** (1 / i)  # Use rs to compute next simplex coord.
            um += (1 - ux) * pr * u / (i + 1) # Update sum
            pr *= ux  # Update product
            x[n - i - 1, :] = um + pr * e  # Calculate x using simplex coords.
            u -= e
            j -= e  # Transition adjustment

        x[n - 1, :] = um + pr * u  # Compute the last x

        # Randomly permute the order in the columns of x and rescale.
        rp = np.random.rand(n, m)  # Use rp to carry out a matrix 'randperm'
        p = np.argsort(rp, axis=0)  # Get sorted indices

        x = (b - a) * np.take_along_axis(x, p, axis=0) + a  # Permute & rescale x

        if m == 1:
            x = x.flatten()

        return x #, v