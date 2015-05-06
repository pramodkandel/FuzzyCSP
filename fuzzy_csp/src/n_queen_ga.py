from pyevolve import *
from random import shuffle

BOARD_SIZE = 64

#set evaluation function
def queens_eval(genome):
   collisions = 0
   for i in xrange(0, BOARD_SIZE):
      if i not in genome: return 0
   for i in xrange(0, BOARD_SIZE):
      col = False
      for j in xrange(0, BOARD_SIZE):
         if (i != j) and (abs(i-j) == abs(genome[j]-genome[i])):
            col = True
      if col == True: collisions +=1
   return BOARD_SIZE-collisions #decrease value for each collision

def queens_init(genome, **args):
   genome.genomeList = range(0, BOARD_SIZE)
   shuffle(genome.genomeList)

def run_main():
   #Genome instance
   genome = G1DList.G1DList(BOARD_SIZE)
   genome.setParams(bestrawscore=BOARD_SIZE, rounddecimal=2)

   #Set initializator
   genome.initializator.set(queens_init)

   #set mutator and crossover
   genome.mutator.set(Mutators.G1DListMutatorSwap)
   genome.crossover.set(Crossovers.G1DListCrossoverCutCrossfill)

   #evaluator function (objective function)
   genome.evaluator.set(queens_eval)

   #Genetic Algorithm Instance
   ga = GSimpleGA.GSimpleGA(genome)
   ga.terminationCriteria.set(GSimpleGA.RawScoreCriteria)
   ga.setMinimax(Consts.minimaxType["maximize"])

   ga.setPopulationSize(100)
   ga.setGenerations(5000)
   ga.setMutationRate(0.02)
   ga.setCrossoverRate(1.0)

   #do evolution
   ga.evolve(freq_stats=10)

   #Best individual
   best = ga.bestIndividual()
   print best
   print "\nBest individual score: %.2f\n" % (best.score,)

if __name__ == "__main__":
   run_main()
