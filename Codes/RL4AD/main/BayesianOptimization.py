import RL_AL
from bayes_opt import BayesianOptimization
from bayes_opt.observer import JSONLogger
from bayes_opt.event import Events
from bayes_opt.util import load_logs
import os

os.environ['CUDA_VISIBLE_DEVICES'] = "0,1"
logger = JSONLogger(path="./KPI_Bayesian_logs_f1_numLP(50-300)_numAL30.json")


# Bounded region of parameter space
# num_LP, num_AL, discount_factor
pbounds = {'num_LP': (50, 300), 'num_AL': (30, 31), 'discount_factor': (0.8, 1.0)}


def function_to_be_optimized(num_LP, num_AL, discount_factor):
    LP = int(num_LP)
    AL = int(num_AL)
    #return (LP+AL*LP ^ -3)/(AL*3*discount_factor)
    return RL_AL.train(LP, AL, discount_factor)


optimizer = BayesianOptimization(
    f=function_to_be_optimized,
    pbounds=pbounds,
    verbose=2,
    random_state=1,
)

optimizer.subscribe(Events.OPTMIZATION_STEP, logger)
optimizer.maximize(alpha=1e-3)

