from fuzzy_cs_problem import FuzzyCSProblem

class FuzzyExampleProblem():

	num_variables = 0
	num_domain_per_variable = 0
	num_vars_per_constraint = 0
	tightness = 0
	connectivity = 0

	def __init__(self, num_variables=num_variables, 
		num_domain_per_variable=num_domain_per_variable, num_vars_per_constraint=num_vars_per_constraint, 
		tightness=tightness, connectivity=connectivity):
		self.num_variables = num_variables
		self.num_domain_per_variable = num_domain_per_variable
		self.num_vars_per_constraint = num_vars_per_constraint
		self.tightness = tightness
		self.connectivity = connectivity


	#generate and return example problem given the parameters
	def generate_example_problem(self):
		pass


	def get_robot_dressing_problem(self):
	    variables = ['f', 't', 's']

	    domains = [('S', 'C'),('D', 'B', 'G'),('L', 'W')]

	    constraints = [
	               {('S','D', None):1.0, 
	                ('S','B',None):0.4,
	                ('S','G',None):0.2,
	                ('C','G',None):0.8,
	                ('C','B',None):0.5},
	               {('S', None, 'L'):1.0,
	                ('S', None, 'W'):0.7,
	                ('C', None, 'W'):1.0,
	                ('C', None, 'L'):0.1},
	               {(None, 'D', 'W'):1.0,
	                (None, 'D', 'L'):0.7,
	                (None, 'B', 'W'):1.0,
	                (None, 'B', 'L'):0.4,
	                (None, 'G', 'L'):1.0,
	                (None, 'G', 'W'):0.6}
	                ]
	    problem = FuzzyCSProblem(variables,domains, constraints)
	    return problem 

	def get_heuristic_backtracking_problem(self):
	    variables = ['f', 't', 's']
	    domains = [('S', 'C'),('D', 'B', 'G'),('L', 'W')]
	    heuristic_backtrack_constraints =[
	               {('S','D', None):0.5, 
	                ('S','G',None):1.0,
	                ('C','B',None):0.1},
	               {('S', None, 'W'):1.0,
	                ('C', None, 'W'):1.0,
	                ('C', None, 'L'):1.0},
	               {(None, 'B', 'W'):1.0,
	                (None, 'B', 'L'):1.0,
	                (None, 'G', 'L'):1.0,
	                (None, 'D', 'L'):1.0}                 
	                ]
	    return FuzzyCSProblem(variables,domains, heuristic_backtrack_constraints)