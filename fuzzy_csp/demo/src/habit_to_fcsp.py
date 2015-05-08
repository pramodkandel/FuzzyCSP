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
		variables = self.get_variables()
		print variables
		domains = self.get_domains()
		print domains
		#for each pair of variables' values, we need to build constraints
		constraints = self.get_desirability_constraints()
		print constraints
		return FuzzyCSProblem(variables, domains, constraints)

	def get_combined_fcsp(self):
		variables = self.get_variables()
		print variables
		domains = self.get_domains()
		print domains
		#for each pair of variables' values, we need to build constraints
		constraints = self.get_combined_constraints()
		print constraints
		return FuzzyCSProblem(variables, domains, constraints)


	#these are binary constraints. change according to
	#whether the constraints are there from habit parser
	def get_availability_constraints(self):
		variables = self.get_variables()
		constraints = []
		var_combos = itertools.combinations(variables, 2)
		for binary_vars in var_combos:												#non_indices will have one element
			fuzzy_constraints = {}
			domain1 = self.habit.get_domain(binary_vars[0])
			domain2 = self.habit.get_domain(binary_vars[1])
			value_combos = itertools.product(list(domain1), list(domain2))
			for values in value_combos:
				score = self.get_pair_availability_score(values)
				indiv_constr = get_instance_tuple_with_vars(binary_vars, values)
				fuzzy_constraints[tuple(indiv_constr)] = score
			if len(fuzzy_constraints)>0:
				constraints.append(fuzzy_constraints)
		return constraints


	def get_desirability_constraints(self):
		variables = self.get_variables()
		constraints = []
		var_combos = itertools.combinations(variables, 2)
		for binary_vars in var_combos:
			fuzzy_constraints = {}
			domain1 = self.habit.get_domain(binary_vars[0])
			domain2 = self.habit.get_domain(binary_vars[1])
			value_combos = itertools.product(list(domain1), list(domain2))
			for values in value_combos:
				score = self.get_pair_desirability_score(binary_vars,values)
				indiv_constr = get_instance_tuple_with_vars(binary_vars, values)

				fuzzy_constraints[tuple(indiv_constr)] = score
			if len(fuzzy_constraints) > 0:
				constraints.append(fuzzy_constraints)
		return constraints

	def get_combined_constraints(self):
		variables = self.get_variables()
		constraints = []
		var_combos = itertools.combinations(variables, 2)
		for binary_vars in var_combos:
			fuzzy_constraints = {}
			domain1 = self.habit.get_domain(binary_vars[0])
			domain2 = self.habit.get_domain(binary_vars[1])
			value_combos = itertools.product(list(domain1), list(domain2))
			for values in value_combos:
				score = self.get_pair_combined_score(binary_vars,values)
				indiv_constr = get_instance_tuple_with_vars(binary_vars, values)

				fuzzy_constraints[tuple(indiv_constr)] = score
			if len(fuzzy_constraints) > 0:
				constraints.append(fuzzy_constraints)
		return constraints

	def get_var_indices(self,variables):
		all_vars = self.get_variables()
		indices = []
		for var in variables:
			indices.append(all_vars.index(var))
		return indices


	def get_pair_desirability_score(variables,values):
		vars_tuple = get_instance_tuple_with_vars(variables,values)
		vars_list = []
		for value in tuple:
			if value == None:
				value = ""
			vars_list.append(value)
		return self.habit_parser.get_preference(vars_list)


	def get_instance_tuple_with_vars(variables, values):
		all_variables = self.get_variables();
		assert(len(all_variables) >= len(variables) and len(variables) == len(values))
		var_indices = self.get_var_indices(variables)	
		indiv_constr = [None]*len(variables)
		for i in range(len(values)):
			var_index = var_indices[i]
			indiv_constr[var_index] = values[i]
		return indiv_constr

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


	def get_pair_combined_score(self, pair_of_items):
		score1 = self.get_availability_score(pair_of_items)
		score2 = self.get_desirability_score(pair_of_items)
		return (score1*score2)**0.5