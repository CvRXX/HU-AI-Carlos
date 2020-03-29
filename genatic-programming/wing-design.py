from functools import reduce
import random
import math
def individual():
	return [random.randrange(0,63,1) for x in range(0,4)]
def fitness(genoType):
	a = genoType[0]
	b = genoType[1]
	c = genoType[2]
	d = genoType[3]

	return 100000 - ((a-b)**2 + (c+d)**2 - (a-30)**3 - (c-40)**3)

def population(nIndividuals):
	return [individual() for x in range(0,100)]

def grade(population):
	return sum([fitness(x) for x in population])/len(population)

def mutate(individual, nBitsMutated):
	for gene in random.sample(range(0,4),nBitsMutated):
		value = individual.pop(gene)
		individual.insert(random.randrange(0,4,1),value)
	return individual

def crossOver(male, female):
	return [male[0],female[1],male[2],female[3]]

def getBest(population):
	graded = [ (fitness(x) ,x) for x in population]
	graded = [ x[1] for x in sorted(graded)]
	return graded[0]

def evolve(population,retain=0.2,random_select=0.10,mutate_chance=0.15):
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
			mutate(individual,1)
	parents.extend(children)

	return parents

testPop = population(50000)
for i in range(0,10000):
	testPop = evolve(testPop)
print(grade(testPop))
print(getBest(testPop))
print(fitness(getBest(testPop)))
for i in range(0,100):
	testPop = evolve(testPop)
print()
print(grade(testPop))
print(getBest(testPop))
print(fitness(getBest(testPop)))


# The variance is very low, almost nothing. This is because the chance is low that a newer higher fit individual is mutated. 