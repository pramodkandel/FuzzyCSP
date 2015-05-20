from flask import Flask
from fuzzy_csp.src.fuzzy_cs_problem import FuzzyCSProblem
from fuzzy_csp.src.fuzzy_cs_solution import FuzzyCSSolution
#from fuzzy_example_problem import FuzzyExampleProblem
from habit_parser import HabitParser
from habit_to_fcsp import HabitToFCSP
from demo_solution import DemoSolution
from flask_restful import reqparse
import json

####GLOBAL VARIABLES##########
data_path = '../data/'
brkfast_file = data_path + 'breakfast_log.txt'
ttl_file = data_path + 'time_to_last.txt'
pref_file = data_path + 'preferences.txt'
m = 10 #for m-best sols
done_startup = False

######END GLOBAL VARIABLES ########

####Instances required#####
habit_parser = None
habit_to_fcsp = None
demo_sol = None
###########################

def startup():
	print "RUNNING STARTUP.."
	global habit_parser
	global habit_to_fcsp
	global demo_sol
	if habit_parser == None: #we assume everything else is None
		print "Setting all variables.."
		habit_parser = HabitParser(brkfast_file, ttl_file, pref_file)
		habit_to_fcsp = HabitToFCSP(habit_parser)
		#print "Availability Problem.."
		avail_problem = habit_to_fcsp.get_availability_fcsp()
		#print "Desirability Problem.."
		desire_problem = habit_to_fcsp.get_desirability_fcsp()
		#print "Combined Problem.."
		combine_problem = habit_to_fcsp.get_combined_fcsp()
		demo_sol = DemoSolution(avail_problem, desire_problem, combine_problem)
		demo_sol.set_m(m)


startup()

app = Flask(__name__)
@app.route("/")
def initial():
	combined = demo_sol.get_nth_best_combined_solution(1)
	return send_response(combined)

@app.route("/sendNextPreference")
def sendMainPreference():
	parser = reqparse.RequestParser()
	parser.add_argument('attempt', type=int)
	parser.add_argument('sol_type', type=str)
	parser.add_argument('want', type=str)
	parser.add_argument('no_want', type=str)
	parser.add_argument('rejected_sols', type=str)
	args = parser.parse_args()
	#print "Parser is", parser
	print "Args are", args
	attempt_num = args['attempt']
	sol_type = args['sol_type']
	rejected_sols = parse_client_rejected_sols(args['rejected_sols'])
	#print "rejected sols are", rejected_sols


	want_items = []
	no_want_items = []
	if len(args['want'].strip()) >0:
		want_items = args['want'].strip().split(",")

	if len(args['no_want'].strip())>0:
		no_want_items = args['no_want'].strip().split(",")

	print "Want items: ", want_items
	print "No want items: ", no_want_items

	candidate_solns = demo_sol.get_mbest_fix_solutions(sol_type, want_items, no_want_items)
	print "candidate_solns are", candidate_solns
	sol = get_next_solution(candidate_solns, 1, rejected_sols)
	return send_response(sol)


def parse_client_rejected_sols(string_rej_sols):
	if string_rej_sols.strip() == "":
		return []
	sols = []
	rej_list = string_rej_sols.split(",")
	for i in range(len(rej_list)/3):
		sol = tuple(rej_list[3*i:3*i+3])
		sols.append(sol)
	return sols

def send_response(sol):
	if sol == None:
		return json.dumps({"sol":None})
	stock = get_stock_solution(sol)
	response_dict = {"sol":sol, "stock":stock}
	#response str should be: {"sol":["bread","jam","milk"], "stock":[0,2,1]}
	print "The response to be sent is: ", response_dict
	return json.dumps(response_dict)

def get_next_solution(candidate_solns, attempt_num, rejected_sols):
	if attempt_num > len(candidate_solns):
		return None
	next_sol = candidate_solns[len(candidate_solns)-attempt_num]
	if next_sol in rejected_sols:
		next_sol = get_next_solution(candidate_solns, attempt_num+1, rejected_sols)
	return next_sol


def get_stock_solution(sol):
	stock = []
	for item in sol:
		score = habit_to_fcsp.get_availability_score(item)
		if score == 0:
			stock.append(0)
		elif score <= 0.25:
			stock.append(1)
		else:
			stock.append(2)
	return stock



if __name__ == "__main__":
	app.run()
