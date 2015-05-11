from pyevolve import *

#set evaluation function
def eval_func(ind):
   score = 0.0
   
   var_x1 = int(ind[0])
   var_x2 = int(ind[1])
   var_x3 = int(ind[2])
   C1 = 0.0
   C2 = 0.0
   C3 = 0.0
   C4 = 0.0
   
   #constraints C1
   if var_x1+var_x2+var_x3 == 7:
       C1 = 1.0
   else:
       C1 = 0.0
   #C2
   if var_x3 == 2:
       C2 = 1.0
   elif var_x3 == 1 or var_x3 ==3:
       C2 = 0.75
   else:
       C2 = 0.0

   #C3
   if var_x2 == 3 or var_x2 == 4:
       C3 = 1.0
   else:
       C3 = 0.5

   #C4
   if var_x1 == 4:
       C4 = 1.0
   elif var_x1 == 3 or var_x1 ==5:
       C4 = 0.75
   else:
       C4 = 0.25
    
   var_z = min(C1, C2, C3,C4)
   return var_z


def run_main():
   # Genome instance
   genome = G1DList.G1DList(3)
   genome.setParams(rangemin=0, rangemax=7, rounddecimal=2)

   # Change the initializator to Integer/Real values
   genome.initializator.set(Initializators.G1DListInitializatorInteger) #integer encoding
   #genome.initializator.set(Initializators.G1DListInitializatorReal)
   #real encoding   

   #set Mutator and Crossover
   genome.mutator.set(Mutators.G1DListMutatorRealGaussian)
   genome.crossover.set(Crossovers.G1DListCrossoverCutCrossfill)
   
   # The evaluator function (objective function)
   genome.evaluator.set(eval_func)

   # Genetic Algorithm Instance
   ga = GSimpleGA.GSimpleGA(genome)
   ga.setMinimax(Consts.minimaxType["maximize"])

   ga.setPopulationSize(20)
   ga.setGenerations(500)
   ga.setMutationRate(0.1)
   ga.setCrossoverRate(0.6)
   ga.selector.set(Selectors.GRouletteWheel)
   pop = ga.getPopulation()
   pop.scaleMethod.set(Scaling.SigmaTruncScaling)
   
   # Do the evolution
   ga.evolve(10)

   #Best individual
   best = ga.bestIndividual()
   best_int = []
   for i in best:
       best_int.append(int(i))
       
   print best, best_int
   

  
if __name__ == "__main__":
   run_main()
