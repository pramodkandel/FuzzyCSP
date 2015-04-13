class FuzzyCSSolution:
	def __init__(self, problem, joint_constraint_type = 'product', do_pruning = False ):
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



	#The method definition here works for binary CSPs only
	def get_appropriateness(self, variables, values):
		constraints = self.get_individual_constraints(variables, values)
		if len(constraints) == 0:
			return 0
		appr = self.find_best_joint_satisfaction(constraints, var_ind)
		return appr


	#return individual constraints with given variables taking given values
	#both given as a list
	def get_individual_constraints(self, variables, values):
		constraints = []
		for constraint in self.problem.constraints:
			satisfy = True
			for i in range(len(variables)):
				variable = variables[i]
				var_ind = self.problem.variables.index(variable)
				value = values[i]
				satisfy = (constraint[var_ind] == value) and satisfy
				if not(satisfy):
					break
			if satisfy:
				constraints.append(constraint)
		return constraints


	#only works for binary constraints
	def find_best_joint_satisfaction(self, constraints, var_ind):
		best_num_values = [0]*len(constraints[0])
		for constraint in constraints:
			for val_ind in range(len(constraint)):
				var_val = constraint[val_ind]
				if (var_val != None) and (var_val != constraint[var_ind]):
					if var_val > best_num_values[val_ind]:
						best_num_values[val_ind] = var_val

		if self.joint_constraint_type == 'product':
			#multiply each of them
			ret_val = 1
			for val in best_num_values:
				ret_val *= val
			return ret_val
		elif self.joint_constraint_type == 'average':
			ret_val = 0
			for val in best_num_values:
				ret_val += val
			return ret_val/float(len(best_num_values))

		elif self.joint_constraint_type == 'min':
			return min(best_num_values)


	def get_difficulty(self, variable):
		domain = self.problem.get_domain(variable)
		difficulty = 0
		for value in domain:
			appr = self.get_appropriateness(variable, value)
			difficulty += appr
		return difficulty



	def heuristic_search():
		variables = self.problem.get_variables()


	#this is the productive joint satisfaction (may need to change to LOG for big problems because decimals will fade)
	def get_joint_satisfaction_degree(self, instantiation):
		#first check that instantiation is the right size
		if len(instantiation) != len(self.problem.variables):
			raise FCSSolutionException('Instantiation is of different length than the variables.')

		return_score = 1
		valid_instance = False
		for constraint in self.problem.constraints.keys():
			if self.is_constraint_in_instance(constraint, instantiation): #this instantiation has this constraint values
				valid_instance = True
				return_score *= self.problem.constraints[constraint]
		return return_score


	#THIS IS O(N). IS THERE A BETTER WAY?
	def is_constraint_in_instance(self, constraint, instantiation):
		if len(constraint) != len(instantiation):
			raise FCSSolutionException('Instantiation is of different length than the constraint.')

		for i in range(len(constraint)):
			if constraint[i] != instantiation[i]:
				if constraint[i] != None:
					return False
		return True




class FCSSolutionException(Exception):
    def __init__(self, msg):
        self.msg = msg