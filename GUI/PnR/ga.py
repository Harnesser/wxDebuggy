#! /usr/bin/env python
""" Generic Genetic Algorithm Class"""

import random
import types

class ga:
    """A Generic Genetic Algorithm Class.

    A generic GA class which implements breeding through crossovers and 
    random mutations.  Uses integers, not binary strings.
    
    Usage
    --------------------------------------------------------------------
      Initialise an instance of this class with the desired population 
    size, etc and a fitness function.  Then call the 'evolve' method to
    run the GA, which will return the fittest chromosome on completion
    of the algorithm.
    
      Passing 'gen_file=True' as an argument to the 'evolve' method will
    enable the creation of a stats file for the GA run.  This may be 
    useful for fine-tuning the GA configuration to solve the problem at
    hand.

    A Note on the Fitness Function:
    --------------------------------------------------------------------
      As every application will have its own measure of fitness, the
    fitness function cannot be generalised. Therefore to use this class,
    a fitness function specific to the task at hand must be written and
    passed to this class on instantiation.  An Assertion will check that
    a valid function is supplied.
    """

    def __init__(self,
                 num_generations=10, population_size=10, 
                 num_genes=2,
                 mutation_rate=0.01, num_crossovers=2,
                 fitness_function=None, num_parents=6,
                 num_elite=2,
                 max_range=127,
                 mutation_max_deviation = 5,
                 debug=False):
        """  """

        self.num_generations = num_generations
        self.population_size = population_size
        self.num_genes = num_genes
        self.mutation_rate = mutation_rate
        self.num_crossovers = num_crossovers
        self.debug = debug
        self.num_parents = num_parents
        self.num_elite = num_elite
        self.num_random_souls = 0
        self.max_range = max_range
        self.mutation_max_deviation = mutation_max_deviation
        
        # A few derived sizes
        max_distance = self.max_range
        self.max_fitness = self.num_genes * max_distance
        
        # Check that we've a fitness function defined.
        assert type(fitness_function) == types.FunctionType
        self.fitness_function = fitness_function

        # A few sanity checks before we proceed
        assert self.population_size >= self.num_parents
        assert self.population_size >= self.num_elite
        assert self.mutation_rate >= 0.0 and self.mutation_rate <= 1.0
        assert self.max_range > 0
        assert self.mutation_max_deviation < self.max_range
        assert ( self.num_crossovers >= 1 and 
                 self.num_crossovers <= self.num_genes) 

        # Population List
        # This is a list of lists: [ <fitness>, [<chromosome_list>] ]
        # we can sort this by fitness easy...
        self.population = []
        
        self.hGA = None  # GA info file handle
        self.gen = 0     # generation counter
        
        
    def evolve(self,debug=False, gen_file=False):
        """Run Evolution."""

        if gen_file:
            self.hGA = open("fitnesses.csv","w")
            self.hGA.write("Generation, Min Fitness, Max Fitness, Average Fitness\n")
            
        if debug:
            x = 20
            print "+" + (" -" * x ) + " +"
            print "|" + "Y-Placement GA".center(x*2+1) + "|"
            print "+" + (" -" * x ) + " +"
        
        # Initial Population
        self.population = self._initial_population()
        self.offspring  = list(self.population)  # holding pen for offspring
        
        # Play $diety, run evolution...
        for self.gen in range(self.num_generations):

            ## Calculate fitness of each member of the population
            self._sort_population(gen_file)    
        
            #  Write results to file? Useful for debug or determining GA config for
            # specific problems
            if gen_file:
                min_fitness, max_fitness, avg_fitness = self._get_stats()
                self.hGA.write("%d,%d,%d,%f\n" % (
                    self.gen, min_fitness, max_fitness, avg_fitness ) )
                print "Generation %d, max=%d, avg=%f" % (
                    self.gen, max_fitness, avg_fitness )      
                
            # Print the fittest...
            self.fitness_function( self.population[0][1],
                                   max_fitness=self.max_fitness,
                                   display=True )
                      
            # Breeding
            self._new_generation()
              
            ##  Keep randomness in population by creating a few random souls each
            # generation. I'm not sure how effective of necessary this is.
            random_souls_start_index = self.population_size - self.num_random_souls
            for j in range( random_souls_start_index, self.population_size ):
                self.population[j][1] = self._random_chromosome()
                
            ## Introduce some mutations (and hope we don't get zombies...)
            self._mutation()


            
        # ---------------------------------------------------- End of generations loop
 
        # Print the fittest...
        self.fitness_function( self.population[0][1],
                               display=True,
                               max_fitness=self.max_fitness )    
           
        # Now choose the fittest as our result...
        self._sort_population(gen_file)
        
        return self.population[0][1]     
        
        
    def show_summary(self):
        """Print out a summary of the GA settings and results."""
        
        lhs_gap = 25
        
        print "-"*80
        print "GA Summary"
        print "-"*80
        print "  Generations".ljust(lhs_gap) ,": ", self.num_generations      
        print "  Population size".ljust(lhs_gap) ,": ", self.population_size
        print "  Number of genes".ljust(lhs_gap) ,": ", self.num_genes
        print "  Crossovers".ljust(lhs_gap) ,": ", self.num_crossovers
        print "  Parents".ljust(lhs_gap) ,": ", self.num_parents
        print "  Elite".ljust(lhs_gap) ,": ", self.num_elite
        print "  Mutation Rate".ljust(lhs_gap) ,": ", self.mutation_rate, "%"
        print "   "
        min_fitness,max_fitness,avg_fitness = self._get_stats()
        if self.max_fitness:
            print "  Maximum Fitness".ljust(lhs_gap) ,": ",max_fitness, \
                " ( of ", self.max_fitness, ")"
        else:
            print "  Maximum Fitness".ljust(lhs_gap) ,": ",max_fitness
        print "  Average Fitness".ljust(lhs_gap) ,": ",avg_fitness
        print "-"*80
               
        return
        
        
#######################################################################################
####  'Private' methods
#######################################################################################


### - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
###  Population Initialisation
### - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def _initial_population(self, debug=False):
        """Create an initial random population."""

        # Set up the array to hold the genome of the population
        chromosome_size = self.num_genes
        population = [0] * self.population_size
        for i in range( self.population_size ):
            new_chromosome = self._random_chromosome( self.max_range )
            population[i] = [ 0, new_chromosome ]           
            
        if debug:
            for soul in population:
                print soul
         
        return population
               
            
    def _random_chromosome(self, max_range):
        """Return a random chromosome."""
        
        chromosome = []
        for i in range( self.num_genes ):
            chromosome.append( random.randrange(0, max_range) )

        return chromosome
        

### - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
###  Population Ranking
### - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def _sort_population(self, gen_file=False, debug=False):
        """Sort the population based on fitness.
        
        This assumes that the bigger the fitness number, the fitter the soul.
        """

        # First, calc the fitness of each soul in the population
        self._calc_fitnesses()
                        
        # Sort population
        self.population.sort()
        self.population.reverse()            

        if debug:
            self._print_population()
        
        return
        

    def _calc_fitnesses(self):
        """Calculate the fitness level of each member of the population.
        
         This uses the fitness function supplied to the class instance to 
        get a number for the fitness of each soul in the population.
        """

        for j in range( len(self.population) ):
            fitness = self.fitness_function( self.population[j][1], # pick the chromo part
                                             max_fitness=self.max_fitness ) 
                                             
            self.population[j][0] = fitness # we'll sort by this index

        return
   

### - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
###  Breeding
### - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def _new_generation(self, debug=False):
        """Breed a new generation of souls.
        
          Now that the population is sorted in order of fitness, we'll replace
        most of the non-breeding (unfit) souls with a offspring of the top ones.
        One of the potential parents is taken from the top 'self.num_parents' of
        the population.  The other parent is taken from anywhere in the population.
        
          The bottom 'self.num_random_souls' of the population will be replaced with 
        random population members.  All other souls will be replaced with the 
        offspring of parents.            
        """
            
        random_souls_start_index = self.population_size - self.num_random_souls

        total_fitness = 0
        for i in range(self.population_size):
            total_fitness += self.population[i][0]
            
        for j in range(0, random_souls_start_index, 2):
            
            ## Select two parents...
            parent1 = self._select_parent(self.num_parents)
            parent2 = self._select_parent(self.num_parents)

            # ... and store the products of their loving
            offspring1,offspring2 = self._breed(parent1, parent2)
            self.offspring[j] = [ 0, offspring1 ]
            if self.population_size != j+1:
                self.offspring[j+1] = [ 0, offspring2 ]            
        
        
        # Now update the population with the new generation
        if debug:
            print "-"*60
            self._print_population()
            self._print_offspring()
            
        num_offspring = self.population_size - self.num_elite   
        self.population[self.num_elite:] = self.offspring[:num_offspring]
        
        if debug:  
            self._print_population()
        
        return
    
    
    def _select_parent(self, upper_limit=10 ):
        """Choose parent using rank."""
        
        parent_index = random.randrange( upper_limit )
        parent = self.population[parent_index][1]
        return parent


    
    def _select_parent_fitness_proportional(self, total_fitness ):
        """Choose parent using fitness proporitional selection.
        
        See Coley, page 24
        """
        
        if total_fitness == 0:
            total_fitness = 1
        
        target = random.randrange( total_fitness )
        running_total = 0
        for i in range( 0, self.population_size ):
            running_total += self.population[i][0]
            if running_total >= target:
                return self.population[i][1]
        
        
        
    def _breed(self, parent1, parent2, debug=False ):
        """Breed two parents."""

        # Calculate crossover points. 
        #   I have to make sure their in assending order, eg: [2, 23 ] is good 
        # and [14,2] is bad.
        #  To this end, I'll keep the value of the previous calculated crossover 
        # point and pick a random number from this to the length of the chromosome 
        crossover_indexes = []
        prev_crossover = 0 # lower limit for crossover range
        for i in range( self.num_crossovers ):
            xindex = random.randrange(prev_crossover, self.num_genes) 
            crossover_indexes.append( xindex )
            prev_crossover = xindex

        babie1 = []
        babie2 = []

        # babies
        cross = True
        cl = 0

        if debug:
            print "- " * 20
            print "Parent1:", parent1
            print "Parent2:", parent2

        for ci in crossover_indexes:

            if cross:            
                babie1.extend(parent1[cl:ci])
                babie2.extend(parent2[cl:ci])
            else:
                babie1.extend(parent2[cl:ci])
                babie2.extend(parent1[cl:ci])
        
            if debug:
                print "crossover point:", ci
                print "Babie1:", babie1
                print "Babie2:", babie2

            cl = ci
            cross = not cross


        if cross:            
            babie1.extend(parent1[cl:])
            babie2.extend(parent2[cl:])
        else:
            babie1.extend(parent2[cl:])
            babie2.extend(parent1[cl:])
         
        if debug:
            print "Babie1: ", babie1
            print "Babie2: ", babie2
       
        assert len(babie1) == self.num_genes
        assert len(babie2) == self.num_genes

        return babie1, babie2


### - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
###  Mutation
### - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def _mutation(self, debug=False):
        """Mutation.
        
         Each gene of each member of the population has 'self.mutation_rate'
        chance of being mutated.
        """
           
        for i in range( len(self.population) ):
        
            #  Build a vector to mutate bits in the chromosome. A 'True' in this 
            # vector will mutate the corresponding gene in the current chromosome.
            mutate_if_one = [0] *  self.num_genes
            mutate_if_one = [ self._flag_mutation(i) for i in mutate_if_one ]

            # Now write the (possibly mutated) soul back into the population
            a = map( self._mutate, self.population[i][1], mutate_if_one )
            
            if debug:
                mutation_count = 0
                for x in mutate_if_one:
                    if x:
                        mutation_count += 1
                print "Mutations:", mutation_count

            self.population[i][1] = a
            
        return
        
        
    def _flag_mutation(self, dummy):
        """ Return a random True or False based on the mutation rate."""
        return random.random() <= self.mutation_rate
        
    
    def _mutate(self, soul, mutate_if_one, debug=False):
        """Used in map operation to mutate bits in the chromosome.
        
          Mutation, in the case of integers, is defined here as adding
        or subtracting a random number in the range self.mutation_max_deviation
        
        """
        
        if mutate_if_one:
        
            if debug: print soul, 
                
            mutation_amount = ( random.randrange( self.mutation_max_deviation * 2 ) -
                                self.mutation_max_deviation )
           
            if debug: print mutation_amount,
            
            soul += mutation_amount
            # bounds checking    
            if soul > self.max_range:
                soul = self.max_range
            elif soul < 0:
                soul = 0            

            if debug: print soul
            
        return soul





### - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
###  Reporting 
### - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def _get_stats(self):
        """Collect some stats for the current population"""
        
        fitnesses = []
        for fitness,soul in self.population:
            fitnesses.append(fitness)
            
        assert len(fitnesses) == self.population_size
        
        max_fitness = max(fitnesses)
        min_fitness = min(fitnesses)
        avg_fitness = sum(fitnesses,0.0) / len( fitnesses )
        
        return min_fitness,max_fitness,avg_fitness


    def _print_population(self):
        """Print out the population, each on a newline"""
        print "Population"
        for soul in self.population:
            print soul
        
        
    def _print_offspring(self):
        """Print out the offspring, each on a newline"""
        print "Offspring"
        for soul in self.offspring:
            print soul
        
        
        
        
### - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
### 
###   M A I N  
### 
### - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
if __name__ == '__main__':


    def fitness_function( soul, debug=False, display=False):
        
        fitness = 0
        for i in soul:
            if i == 1:
                fitness += 1

        if debug:
            print fitness, ":", soul

        return fitness


    def ascii_distance( soul, max_fitness=0, debug=False, display=False ):
        """ Fitness is the distance away from the string.

        """
  
        match_this = 'This is a string of length 50 characters. Honestly'
        
        string = ""
        distance = 0
        fitness = 0
            
        for i in range( len(match_this ) ):

            ga_ord = soul[i]
            
            if ga_ord >= 32:
                string += chr(ga_ord)             
            else:
                string += '.'
                
            distance += abs( ga_ord - ord(match_this[i]) )

            # it seems that if you try to display chr(14), the terminal
            # screws up...
            if debug:
                print '   "%d"' % ( soul[i] ), ga_ord, string[-1]
                print "   Match '%s' (%d) with '%s' (%d): Distance: %d" % (
                     match_this[i], ord(match_this[i]),
                     string[-1], ga_ord , 
                     abs( ga_ord - ord(match_this[i]) )
                     ) 
                print "  ", string

                    
            if match_this[i] == chr(ga_ord):
                fitness += 1
               
                       
        if True:           
            # Calculate fitness - higher is better
            fitness = max_fitness - distance
           
        if display:
            print string, fitness
            #myGA.hGA.write(":'%s'\n" % ( string ) )   
            
        assert fitness >= 0
        return fitness
    
    
    import cProfile
    #import pstats
    
    myGA = ga(fitness_function=ascii_distance, 
              num_genes=50,
              num_generations=100,
              population_size=1000,
              num_crossovers=1,
              num_parents=750,
              num_elite=10,
              mutation_rate=0.1,
              mutation_max_deviation=20)
   

    if False:
        import cProfile
        import pstats

        cProfile.run( 'myGA.evolve(gen_file=True)', 'ga.prof' )             
        p = pstats.Stats('ga.prof')
        
        p.strip_dirs().sort_stats(-1).print_stats()
        p.sort_stats('cumulative').print_stats(10)
        
        p.sort_stats('time', 'cum').print_stats(.5, 'init')
        
        p.sort_stats('time').print_stats()
    else:    
        myGA.evolve(gen_file=True)
        
   
    myGA.show_summary()
    

    
