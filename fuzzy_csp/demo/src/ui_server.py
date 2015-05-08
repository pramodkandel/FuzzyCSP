from flask import Flask
from fuzzy_csp.src.fuzzy_cs_problem import FuzzyCSProblem
from fuzzy_csp.src.fuzzy_cs_solution import FuzzyCSSolution
#from fuzzy_example_problem import FuzzyExampleProblem
from habit_parser import HabitParser
from habit_to_fcsp import HabitToFCSP

from flask_restful import reqparse

app = Flask(__name__)
@app.route("/")
def hello():
	return '{"combined" : {"main":"M1","side":"S1","drink":"D1"}, "desirability" : {"main":"M2","side":"S2","drink":"D2"}, "availability" : {"main":"M3","side":"S3","drink":"D3"}}'

@app.route("/sendNextPreference")
def sendMainPreference():
	parser = reqparse.RequestParser()
	parser.add_argument('attempt', type=int)
	args = parser.parse_args()
	#print args = {'attempt': 1}
	return '{"combined" : {"main":"M11","side":"S11","drink":"D11"}, "desirability" : {"main":"M21","side":"S21","drink":"D21"}, "availability" : {"main":"M31","side":"S31","drink":"D31"}}'

	

if __name__ == "__main__":
	app.run()
