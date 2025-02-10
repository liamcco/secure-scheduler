def get_divisors(n):
    """Returns all divisors of n."""
    return sorted({d for i in range(1, int(n**0.5) + 1) if n % i == 0 for d in (i, n // i)})