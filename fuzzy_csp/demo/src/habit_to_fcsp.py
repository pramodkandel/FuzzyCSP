from habit_parser import HabitParser
import math
import itertools
from fuzzy_csp.src.fuzzy_cs_problem import FuzzyCSProblem

class HabitToFCSP:
	def __init__(self, habit_parser):
		self.habit = habit_parser
		self.variables = habit_parser.get_variables()
		self.domains = habit_parser.get_domains()


	def get_variables(self):
		return self.variables

	def get_domains(self):
		return self.domains

	def get_availability_fcsp(self):
		variables = self.get_variables()
		print variables
		domains = self.get_domains()
		print domains
		#for each pair of variables' values, we need to build constraints
		constraints = self.get_availability_constraints()
		print constraints
		return FuzzyCSProblem(variables, domains, constraints)


	def get_desirability_fcsp(self):
		pass

	def get_combined_fcsp(self):
		pass


	#these are binary constraints. change according to
	#whether the constraints are there from habit parser
	def get_availability_constraints(self):
		variables = self.get_variables()
		constraints = []
		var_combos = itertools.combinations(variables, 2)
		for binary_vars in var_combos:
			#none_indices = get_none_indices(binary_vars, variables) #in our specific case, 
			var_indices = self.get_var_indices(binary_vars)													#non_indices will have one element
			fuzzy_constraints = {}
			domain1 = self.habit.get_domain(binary_vars[0])
			domain2 = self.habit.get_domain(binary_vars[1])
			value_combos = itertools.product(list(domain1), list(domain2))
			for values in value_combos:
				score = self.get_pair_availability_score(values)
				indiv_constr = [None]*len(variables)
				for i in range(len(values)):
					var_index = var_indices[i]
					indiv_constr[var_index] = values[i]
				fuzzy_constraints[tuple(indiv_constr)] = score
			constraints.append(fuzzy_constraints)
		return constraints


	def get_desirability_constraints(self):
		pass

	def get_combined_constraints(self):
		pass

	def get_var_indices(self,variables):
		all_vars = self.get_variables()
		indices = []
		for var in variables:
			indices.append(all_vars.index(var))
		return indices

	def get_availability_score(self, item):
		freq = self.habit.get_frequency([item])
		ttl = self.habit.time_to_last_item(item)
		if freq == 0:
			return 0
		return 1 - (ttl/float(freq));


	#TODO: What does it return when the pair isn't there?
	def get_pair_availability_score(self, pair_of_items):
		i1 = pair_of_items[0]
		i2 = pair_of_items[1]
		score1 = self.get_availability_score(i1)
		score2 = self.get_availability_score(i2)
		return (score1*score2)**0.5

