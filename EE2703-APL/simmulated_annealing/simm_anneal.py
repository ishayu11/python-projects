import numpy as np
import matplotlib.pyplot as plt

# Open a pointer to the dataset file

f = open("tsp40.txt")

lines = f.readlines()
N = int(lines[0])
lines.remove(lines[0])

citys = []

for line in lines:
    coord = line.split()
    city = (float(coord[0]), float(coord[1]))
    citys.append(city)
citys = np.array(citys)


# calculates distance between two cities
def dist(x1, y1, x2, y2):
    return np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


# calculate distance travelled by the salesman given a particular order
def distance(cities, cityorder):
    totaldistance = 0
    for i in range(len(cityorder)):
        totaldistance += dist(cities[cityorder[i - 1]][0], cities[cityorder[i - 1]][1], cities[cityorder[i]][0],
                              cities[cityorder[i]][1])
    return totaldistance


def tsp(cities):
    T = 2000.0
    decayrate = 0.999
    # Set up some large value for the best cost found so far

    # Generating a random order of the cities for our initial guess
    rand_order = np.arange(N)
    np.random.shuffle(rand_order)
    rand_order = np.append(rand_order, rand_order[0])
    num_iter = 1

    bestcost = distance(cities, rand_order)
    initial = bestcost  # distance travelled in the initial guess

    while num_iter <= 30000:

        tour = cities[rand_order]

        # Generate two random indices to swap

        while (1):
            i = np.random.randint(N)
            j = np.random.randint(N)
            if i != j:
                break

        # Make the swap

        rand_order[i], rand_order[j] = rand_order[j], rand_order[i]
        rand_order[N] = rand_order[0]

        y = distance(cities, rand_order)

        if y < bestcost:
            bestcost = y
        else:
            toss = np.random.random_sample()
            if toss < np.exp(-(y - bestcost) / T):
                bestcost = y
            else:
                # revert the swap, if cost is worse and it doesn't satisfy the probability requirement
                rand_order[i], rand_order[j] = rand_order[j], rand_order[i]
                rand_order[N] = rand_order[0]

        T = T * decayrate
        num_iter = num_iter + 1

    # Calculate improvement from initial guess
    imp = (abs(initial - bestcost) / initial) * 100

    cityorder = rand_order
    print("Optimum distance travelled = ", bestcost)
    print(f"Percentage Improvement = {imp} %")
    return cityorder


optimized_order = tsp(citys)
print(optimized_order)

# Array containing co-ordinates of cities in the most optimum way to visit them
best_tour = citys[optimized_order]


xplot = best_tour[:, 0]
yplot = best_tour[:, 1]

plt.clf()
plt.plot(xplot, yplot, 'o-')
plt.savefig("path.png")
plt.show()

