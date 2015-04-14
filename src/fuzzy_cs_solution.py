class FuzzyCSSolution:
	def __init__(self, problem, joint_constraint_type = 'productive', do_pruning = False ):
		self.problem = problem
		self.joint_constraint_type = joint_constraint_type
		self.do_pruning = do_pruning

	def set_joint_constraint_type(self, constraint_type):
		self.joint_constraint_type = constraint_type

	def get_joint_constraint_type(self):
		return self.joint_constraint_type

	def set_pruning(self, boolean):
		self.do_pruning = boolean

	def get_pruning(self):
		return self.do_pruning


######JOINT CONSTRAINT SATISFACTION #########

	def get_joint_satisfaction_degree(self, instantiation):
		#first check that instantiation is the right size
		return self.get_joint_constraint_satisfaction_degree(self.problem.constraints, instantiation)

	#for the new constraint model
	def get_joint_constraint_satisfaction_degree(self, constraints, instantiation):
		#TODO:first check that instantiation is the right size
		joint_satisfaction = 0.
		indiv_satisfaction_list = []
		for constraint in constraints:
			indiv_satisfaction = self.get_constraint_satisfaction_degree(constraint, instantiation)
			indiv_satisfaction_list.append(indiv_satisfaction)

		if len(indiv_satisfaction_list) == 0:
			return 0.

		if self.joint_constraint_type == 'productive':
			#multiply each of them
			joint_satisfaction = 1.0
			for satisfaction in indiv_satisfaction_list:
				joint_satisfaction *= satisfaction
		elif self.joint_constraint_type == 'average':
			for satisfaction in indiv_satisfaction_list:
				joint_satisfaction += satisfaction
			joint_satisfaction = joint_satisfaction/float(len(indiv_satisfaction_list))

		elif self.joint_constraint_type == 'min':
			joint_satisfaction = min(indiv_satisfaction_list)

		else:
			raise FCSSolutionException('Input the correct joint satisfaction type')

		return joint_satisfaction


	#for the new constraint model
	def get_constraint_satisfaction_degree(self,constraint, instantiation):
		#TODO:check that the instantiation is of right length
		satisfaction = 0.
		for fuzzy_assignment in constraint.keys():
			satisfies = True
			for i in range(len(fuzzy_assignment)):
				if fuzzy_assignment[i] != instantiation[i]:
					if fuzzy_assignment[i] != None:
						satisfies = False
						break

			if satisfies == True:
				satisfaction = constraint[fuzzy_assignment]
				break
		return satisfaction


		for i in range(len(constraint)):
			if constraint[i] != instantiation[i]:
				if constraint[i] != None:
					return False
		return True

####### END OF JOINT CONSTRAINT SATISFACTION ###################

######## START OF APPROPRIATENESS VALUE ###################


	def get_all_possible_instantiations(self,fixed_vars, fixed_values):
		import itertools
		instantiations = []
		#TODO: Check if fixed_vars and fixed_values are same length

		#first fix the values of variables
		reduced_domains = self.problem.domains[:]
		for i in range(len(fixed_vars)):
			var = fixed_vars[i]
			value = fixed_values[i]
			var_ind = self.problem.variables.index(var)
			reduced_domains[var_ind] = (value)

		#now use the magic of itertools to get all possible instantiations
		for instance in itertools.product(*reduced_domains):
			instantiations.append(instance)
		return instantiations

	def get_constraints_with_variables(self, variables):
		reduced_constraints = []
		for constraint in self.problem.constraints:
			#if any of the variables have None as their value in the constraint
			constraint_assignment = constraint.keys()[0]; #an example assignment
			all_vars_satisfy = True
			for var in variables:
				var_ind = self.problem.variables.index(var)
				if constraint_assignment[var_ind] == None:
					all_vars_satisfy = False
					break
			if all_vars_satisfy:
				reduced_constraints.append(constraint)
		return reduced_constraints

	#TODO: is there a better way?
	def get_appropriateness(self, variables, values):
		all_instances = self.get_all_possible_instantiations(variables, values)
		all_constraints = self.get_constraints_with_variables(variables)
		#print "All instances for appropriateness are", all_instances
		#print "All constraints for appropriateness are", all_constraints
		best_joint_sat = 0
		for instance in all_instances:
			joint_sat = self.get_joint_constraint_satisfaction_degree(all_constraints, instance)
			if joint_sat > best_joint_sat:
				best_joint_sat = joint_sat
		return best_joint_sat



	#fixed_vars is a dictionary of keys as variables and values as 
	#corresponding fixed values of those variables
	def get_difficulty_and_appr(self, variable, fixed_vars):
		domain = self.problem.get_domain(variable)
		fixed_variables = fixed_vars.keys()
		appr_dict = {}
		difficulty = 0
		for value in domain:
			appr_variables = fixed_variables + [variable]
			appr_values = []
			for fixed_var in fixed_variables:
				fixed_val = fixed_vars[fixed_var]
				appr_values.append(fixed_val)
			appr_values = appr_values + [value]

			appr = self.get_appropriateness(appr_variables, appr_values)
			appr_dict[value] = appr
			difficulty += appr
		return difficulty, appr_dict



	def heuristic_search(self):
		variables = self.problem.variables
		fixed_vars = {}
		while len(fixed_vars)<len(variables):
			best_appr_dict = None
			least_diff = float('inf')
			var_to_set = None
			for variable in variables:
				if variable not in fixed_vars:
					difficulty, appr_dict = self.get_difficulty_and_appr(variable, fixed_vars)
					if difficulty<least_diff:
						least_diff = difficulty
						best_appr_dict = appr_dict
						var_to_set = variable
			if best_appr_dict == None:
				raise FCSSolutionException('Code should not come here. Look at heuristic_search function.')

			#now instantiate the var_to_set
			fixed_vars[var_to_set] = self.get_best_appr_var_assignment(best_appr_dict)
		return fixed_vars

	def get_best_appr_var_assignment(self, best_appr_dict):
		max_appr = 0
		best_assignment = None
		for assignment in best_appr_dict:
			if best_appr_dict[assignment] > max_appr:
				max_appr = best_appr_dict[assignment]
				best_assignment = assignment
		return best_assignment





class FCSSolutionException(Exception):
    def __init__(self, msg):
        self.msg = msg