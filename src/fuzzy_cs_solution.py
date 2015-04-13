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
		print "Getting appropriateness for variables", variables, "and values", values
		constraints = self.get_individual_constraints(variables, values)
		
		if len(constraints) == 0:
			return 0
		var_indices = []
		for variable in variables:
			var_ind = self.problem.variables.index(variable)
			var_indices.append(var_ind)
		appr = self.find_best_joint_satisfaction(constraints, var_indices)
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


	#works for binary, but can be extended later on
	def find_best_joint_satisfaction(self, constraints, var_indices):
		print "Matched constraints are", constraints
		#print "Var indices fixed for joint_satisfaction are", var_indices

		num_vars_per_constraint = self.problem.get_num_vars_per_constraint()
		prob_constraints = self.problem.constraints
		if len(var_indices) == num_vars_per_constraint: #there will be just one constraint
			if len(constraints)>1:
				raise FCSSolutionException('Something is wrong. Look into find_best_joint_satisfaction function.')
			return prob_constraints[constraints[0]]

		#for binary, we eliminated 2 vars above. So, now we only have case for one variable
		best_num_values = {}
		for i in range(len(self.problem.variables)):
			if i not in var_indices:
				best_num_values[i] = 0


		for constraint in constraints:
			for val_ind in range(len(constraint)):
				var_val = constraint[val_ind]
				if (var_val != None) and (val_ind not in var_indices):
					constraint_sat_num = prob_constraints[constraint]
					if constraint_sat_num > best_num_values[val_ind]:
						best_num_values[val_ind] = constraint_sat_num

		#print "Best satisfaction values are", best_num_values

		if self.joint_constraint_type == 'product':
			#multiply each of them
			ret_val = 1.0
			for best_sat_key in best_num_values.keys():
				best_val = best_num_values[best_sat_key]
				ret_val *= best_val
			return ret_val
		elif self.joint_constraint_type == 'average':
			ret_val = 0
			for best_sat_key in best_num_values:
				best_val = best_num_values[best_sat_key]
				ret_val += best_val
			return ret_val/float(len(best_num_values))

		elif self.joint_constraint_type == 'min':
			return min(best_num_values.values())

		else:
			raise FCSSolutionException('Input the correct joint satisfaction type')


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