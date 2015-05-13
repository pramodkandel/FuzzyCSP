#6.834 PSET3 and PSET4
Group members: Manushaqe Muco, Pallavi Mishra, Pramod Kandel

# 6.834_PSET3
#Fuzzy Constraint Satisfaction Problem tutorial and implementation for Cognitive Robotics (6.834) MIT

Instructions to configure the project:

1. Download or clone this project. 
  
  git clone https://github.com/pramod2/FuzzyCSP

2. From the main project directory (where setup.py file is), run this in terminal: "sudo python setup.py install" . This makes sure the package installs correctly in your system.

3a. To see an example of all the public API use, see test/fuzzy_cs_api_test.py.

qIn the terminal,you can run it with this command: "python fuzzy_cs_api_test.py"

3b. To see an example of the public API use for the Genetic Algorithms (GA), see test/n_queen_ga.py and test/university_course_selection_ga.py.  

Before running those files,make sure you have PyEvolve installed, and active in the shell you are running the files in. Information on how to install PyEvolve can be found at: http://pyevolve.sourceforge.net/0_6rc1/intro.html# .

4. Unit tests for internal functions are placed in test/fuzzy_cs_unittest.py, which you can run as well.

5a. Benchmark tests are under benchmark/fuzzy_benchmark_test.py. If you run it, the results appear in a txt file in the same folder. The results compare various algorithms according to various problem metrics. For problem metrics, see the class variables of FuzzyExampleProblem in src/fuzzy_example_problem.py.

5b. For GA, the benchmark results appear in the FuzzyCSP-GA-Tutorial.pdf. The main metrics were runtime and the generation number at which the solution was achieved. The results compare the performance of GAs when changing various parameters (initial population, chromosome encoding, mutation/crossover probability, etc), and running the algorithms several times. Because of the nature of GA, we could not find an automatic way to plot and average the results (graphs can be found in the tutorial).

However, by running the individual files, test/n_queen_ga.py and test/university_course_selection_ga.py, we can see how the fitness is improved from one generation to the other. In this sense, every run of the algorithm prints on the screen the benchmarking results for the fitness of each generation. An example of how this looks like can be found at benchmark/n_queen_generation_benchmark.png and benchmark/university_course_selection_generation_benchmark.png

#6.834_PSET4 
Instructions on how to run the demo (located at FuzzyCSP/fuzzy_csp/demo/)

0. Install the python modules flask and flask-restful.

  flask:          http://flask.pocoo.org/ 
  
  flask-restful:  https://flask-restful.readthedocs.org/en/0.3.2/installation.html

1. Install CORS plugin for chrome browser.

  https://chrome.google.com/webstore/detail/allow-control-allow-origi/nlfbmbojpeacfghkpbjhddihlkkiljbi?hl=en

2. Pull/clone the latest github project.

  git clone https://github.com/pramod2/FuzzyCSP/tree/master/fuzzy_csp/demo

3. In the terminal, cd to the main folder where the setup.py file is. Then, run "python setup.py install". 

4. In the terminal, cd to demo/src, and run "python ui_server.py". Or, run the "ui_server.py" file in any other way.

5. Turn on the CORS plugin, i.e. toggle it "green" (top right corner in chrome browser).

6. Then, open UI_Basic_v2.html inside demo in the browser

