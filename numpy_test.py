import numpy as np

m=3
s=4
k=2


s = np.full(m, s)
j = np.full(m, k + 1, dtype=int)
sm = np.zeros(m)
pr = np.ones(m)

print(s)
print(j)
print(sm)
print(pr)