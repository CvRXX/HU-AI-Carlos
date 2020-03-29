from functools import reduce
import random

def individual():
	return [random.randrange(0,2,1) for x in range(0,10)]
def fitness(genoType):
	pile0=0
	pile1=1
	for idx, gene in enumerate(genoType,0):
		if gene:
			pile0 += idx+1
		else:
			pile1 *= idx+1


	return (abs(pile0-36)+abs(pile1-360))

def population(nIndividuals):
	return [individual() for x in range(0,100)]

def grade(population):
	return sum([fitness(x) for x in population])/len(population)

def mutate(individual, nBitsMutated):
	for bit in random.sample(range(0,10),nBitsMutated):
		individual[bit] = int(not individual[bit])
	return individual

def crossOver(male, female):
	child = []
	for x in range(len(male)):
		if x%2:
			child.append(male[x])
		else:
			child.append(female[x])
	return child

def getBest(population):
	graded = [ (fitness(x) ,x) for x in population]
	graded = [ x[1] for x in sorted(graded)]
	return graded[0]

# I tried different configurations and noticed that if mutate_chance of random_select gets to low an fitness of 0 is reached less often.
# I think this is because the algorithm has less chance to escape a local minimum. Especially when there are a lot of individuals with a fitness of 1.
def evolve(population,retain=0.2,random_select=0.05,mutate_chance=0.01):
	graded = [ (fitness(x) ,x) for x in population]
	graded = [ x[1] for x in sorted(graded)]
	retain_length = int(len(graded)*retain)
	parents = graded[:retain_length]
	
	for individual in graded[retain_length:]:
		if random_select>random.random():
			parents.append(individual)

	desired_length = len(population)-len(parents)
	children = []
	while len(children) < desired_length:
		male = random.randint(0,len(parents)-1)
		female = random.randint(0,len(parents)-1)
		if male != female:
			children.append(crossOver(parents[male],parents[female]))

	for individual in children:
		if mutate_chance > random.random():
			mutate(individual,3)
	parents.extend(children)

	return parents

for i in range(0,100): # Try at max 100 populations to get a solution
	testPop = population(500)
	for i in range(0,100): # Do 100 evolutions
		testPop = evolve(testPop)
		if fitness(getBest(testPop)) == 0:
			break
	if fitness(getBest(testPop)) == 0:
		print(getBest(testPop))
		break



