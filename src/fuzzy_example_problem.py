from fuzzy_cs_problem import FuzzyCSProblem

import itertools
import math
import numpy as np

class FuzzyExampleProblem():

	num_variables = 3
	domain_size_per_variable = 2
	num_vars_per_constraint = 2
	tightness = 0.25

	connectivity = .75 #.25,.5,.75

	range_sat_values = [0.5, 1.0]

	def __init__(self, num_variables=num_variables, 
		domain_size_per_variable=domain_size_per_variable, num_vars_per_constraint=num_vars_per_constraint, 
		tightness=tightness, connectivity=connectivity, range_sat_values = range_sat_values):
		self.num_variables = num_variables
		self.domain_size_per_variable = domain_size_per_variable
		self.num_vars_per_constraint = num_vars_per_constraint
		self.tightness = tightness
		self.connectivity = connectivity
		self.range_sat_values = range_sat_values

	#generate and return example problem given the parameters
	def generate_example_problem(self):
		variables, domains = self.generate_variables_and_domains()

		constraints = self.generate_constraints(variables, domains)

	def generate_variables_and_domains(self):
		lowercase_initial = ord('a')
		uppercase_initial = ord('A')
		variables = []
		domains = []
		num_variables = self.num_variables
		domain_size_per_variable = self.domain_size_per_variable
		for i in range(num_variables):
			var = chr(lowercase_initial+i)
			domain = [str(j) for j in range(domain_size_per_variable*i, domain_size_per_variable*(i+1))]
			variables.append(var)
			domains.append(tuple(domain))
		return variables, domains



	def nCr(self,n,r):
		f = math.factorial
		return f(n) / f(r) / f(n-r)

	def generate_constraints(self, variables, domains):
		#create all variable combinations
		all_constraint_vars = itertools.combinations(variables, self.num_vars_per_constraint)
		num_all_constraint_vars = self.nCr(len(variables),self.num_vars_per_constraint)


		return_constraints = []

		connected = True
		combo_i = 0
		for constraint_var in all_constraint_vars:
			if combo_i+1 > num_all_constraint_vars*self.connectivity:
				connected = False
			combo_i +=1

			var_list = list(constraint_var)
			var_ind_list = [variables.index(var) for var in var_list]
			domain_list = [domains[ind] for ind in var_ind_list]

			constraint_dict={}

			all_value_assignments = itertools.product(*domain_list)

			size_all_values = len(domain_list[0])**len(domain_list) #works because each domain size is same
			allowed_size = math.floor(size_all_values*(1-self.tightness)) +1

			satisfaction_values = np.linspace(self.range_sat_values[0],self.range_sat_values[1],allowed_size)[1:]

			disallow = False
			assign_i = 0
			for value_assignment in all_value_assignments:
				if assign_i+1 >size_all_values*(1-self.tightness):
					disallow = True
				
				constraint_key = self.make_constraint_for_fixed_vars(variables, var_list, value_assignment)
				#assign a satisfaction degree to this constraint
				if connected == False:
					constraint_dict[constraint_key] = 1.0
				else:
					if not disallow:
						constraint_dict[constraint_key] = satisfaction_values[assign_i]
					#do it according to tightness

				#print "The var_list and value_list are", var_list, value_list
				assign_i +=1
			return_constraints.append(constraint_dict)
		return return_constraints

	def make_constraint_for_fixed_vars(self, total_variables, fixed_var_list, value_assignment):
		#create constraint key
		constraint_key_list = [None]*len(total_variables)
		for i in range(len(fixed_var_list)):
			var = fixed_var_list[i]
			value = value_assignment[i]
			total_var_ind = total_variables.index(var)
			constraint_key_list[total_var_ind] = value
		constraint_key = tuple(constraint_key_list)
		return constraint_key


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