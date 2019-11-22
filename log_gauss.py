import numpy as np
import matplotlib.pyplot as plt
import statistics as stats
import random as r


y = np.random.normal(200, 10, 50000)

for i in range(len(y)):
    y[i] = round(y[i])

y_min = min(y)
y_max = max(y)

x = np.linspace(y_min, y_max, (y_max - y_min + 1))

count = [0] * int(y_max - y_min + 1)
# create count array
for e in y:
    count[int(e - y_min)] = count[int(e - y_min)] + 1

print(y)
print(count)

y_new = y
y = np.zeros(len(y))


fig = plt.figure()
ax1 = fig.add_axes([0.1, 0.5, 0.8, 0.4], xticklabels=[])
ax2 = fig.add_axes([0.1, 0.1, 0.8, 0.4])


ax1.plot(x, count)
ax2.plot(np.log(x), count)
plt.show()
