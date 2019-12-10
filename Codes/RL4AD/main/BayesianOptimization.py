import RL_AL
from bayes_opt import BayesianOptimization
from bayes_opt.observer import JSONLogger
from bayes_opt.event import Events

logger = JSONLogger(path="./Bayesian_logs.json")


# Bounded region of parameter space
# num_LP, num_AL, discount_factor
pbounds = {'num_LP': (1, 50), 'num_AL': (1, 20), 'discount_factor': (0.8, 1.0)}


def function_to_be_optimized(num_LP, num_AL, discount_factor):
    LP = int(num_LP)
    AL = int(num_AL)
    return RL_AL.train(LP, AL, discount_factor)


optimizer = BayesianOptimization(
    f=function_to_be_optimized,
    pbounds=pbounds,
    verbose=2,
    random_state=1,
)

optimizer.subscribe(Events.OPTMIZATION_STEP, logger)
optimizer.maximize(alpha=1e-3)

