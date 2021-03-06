import numpy as np
import pandas as pd

import copy


"""
Helper methods of class particle
"""
def rand_arr_sum_one(length):
    arr = []
    rand = np.random.ranf(length - 1)
    rand = np.append(rand, [0, 1])
    rand.sort()
    for i in range(len(rand) - 1):
        arr.append(rand[i + 1] - rand[i])
    return arr


def update_velocity_micro_particle(w, c1, c2, velocity, position, post_best, global_best):
    r1 = np.random.random()
    r2 = np.random.random()

    vel_cognitive = c1 * r1 * (post_best - position)
    vel_social = c2 * r2 * (global_best - position)
    new_velocity = (w * velocity) + vel_cognitive + vel_social
    if new_velocity != 0:
        return new_velocity
    else:
        return np.random.random_sample()


def update_position_micro_particle(position, velocity, bounds):
    position = position + velocity

    # adjust maximum position if necessary
    if position > bounds[1]:
        position = bounds[1]

    # adjust maximum position if necessary
    if position < bounds[0]:
        position = bounds[0]

    return position


"""
Helper of class PSO
"""


def analyse_result(position, df):

    temp = pd.Series(
        index=['position', 'algorithm_period_return', 'alpha', 'benchmark_period_return', 'returns', 'sharpe','portfolio_value'])

    temp.position = position
    temp.algorithm_period_return = np.mean(df.algorithm_period_return)
    temp.alpha = np.mean(df.alpha)
    temp.benchmark_period_return = np.mean(df.benchmark_period_return)
    temp.returns = np.mean(df.returns)
    temp.sharpe = np.mean(df.sharpe)
    temp.portfolio_value = np.mean(df.portfolio_value[-1])

    return temp


def sum_correction(position):
    s = sum(position)
    return [a / s for a in position]


"""
Particle Class
"""
class Particle(object):
    # number of dimensions : number of indicators
    num_dimension = 9

    def __init__(self):
        self.position = []
        self.velocity = [[0.0] * Particle.num_dimension, [0.0] * Particle.num_dimension, 0.0, 0.0]
        self.post_best = [[0.0] * Particle.num_dimension, [0.0] * Particle.num_dimension, 0.0, 0.0]
        self.obj_best = -10000.0
        self.current_obj = -10000.0
        self.bounds = pd.Series([(0.0,1.0),(0.0,1.0),(-1.0,0.0)],index=['weights','DB','DS'])

        ##########test
        self.datafra_result = pd.DataFrame()

        # initialize position
        self.initialize_position()

    # this method initializes the weights of indicators
    def initialize_position(self):
        # initialize trend weights
        self.position.append(rand_arr_sum_one(Particle.num_dimension))
        # initialize non_trend weights
        self.position.append(rand_arr_sum_one(Particle.num_dimension))
        # initialize DB
        self.position.append(np.random.random_sample())
        # initialize DS
        self.position.append(np.random.random_sample()-1.0)

    # evaluate current fitness
    def evaluate(self, obj_func):

        back_tester = obj_func(self.position)

        ##############
        #TEST
        ##############
        self.current_obj, self.datafra_result = back_tester.run()


        # check to see if the current position is an individual best
        # type of optimization is maximize
        if self.current_obj > self.obj_best:
            self.post_best = copy.deepcopy(self.position)
            self.obj_best = self.current_obj

    # update the velocity of particle
    def update_velocity(self, global_best):
        if len(self.position) != len(global_best):
            raise ValueError('the dimension of global best did not correspond with dimension of particles')
        else:
            w = 0.5  # constant inertia weight (how much to weigh the previous velocity)
            c1 = 1  # cognitive constant
            c2 = 1  # social constant

            # update velocity of trend & non-trend weights
            for j in range(2):
                for i in range(0, Particle.num_dimension):
                    #print('(%s,%s)'%(i,j))
                    self.velocity[j][i] = update_velocity_micro_particle(w, c1, c2,
                                                                         self.velocity[j][i],
                                                                         self.position[j][i],
                                                                         self.post_best[j][i],
                                                                         global_best[j][i]
                                                                         )

            # update velocity of DB & DS
            for i in range(2, 4):
                self.velocity[i] = update_velocity_micro_particle(w, c1, c2,
                                                                  self.velocity[i],
                                                                  self.position[i],
                                                                  self.post_best[i],
                                                                  global_best[i]
                                                                  )

    def update_position(self):
        # update position of weights
        for i in range(2):
            for j in range(0, Particle.num_dimension):
                self.position[i][j] = update_position_micro_particle(
                                                                     self.position[i][j],
                                                                     self.velocity[i][j],
                                                                     self.bounds.weights
                                                                    )

        # update position of DB & DS
        for i in range(2, 4):
            self.position[i] = update_position_micro_particle(self.position[i],
                                                              self.velocity[i],
                                                              self.bounds.ix[i-1]
                                                              )

        # correct the weights so that the sum of them remains equal to 1
        for i in range(2):
            self.position[i] = sum_correction(self.position[i])


class PSO(object):
    def __init__(self, obj_func, swarm_size, max_iter):
        self.global_best_fit = -10000.0
        self.global_best_sol = []
        self.iter_num = 0
        self.obj_func = obj_func
        self.swarm_size = swarm_size
        self.max_iter = max_iter
        # test performance
        self.performance = pd.DataFrame(columns=['position', 'algorithm_period_return', 'alpha', 'benchmark_period_return', 'returns', 'sharpe','portfolio_value'])

    def run(self):
        # create swarm (population)
        swarm = []
        for i in range(0, self.swarm_size):
            swarm.append(Particle())

        # optimization loop
        while self.iter_num < self.max_iter:
            count = 0
            # iterate over particles in swarm and evaluate fitness
            for i in range(self.swarm_size):
                swarm[i].evaluate(self.obj_func)

                # determine the best global particle
                # type of optimization is maximize
                if swarm[i].current_obj > self.global_best_fit:
                    self.global_best_sol = copy.deepcopy(swarm[i].position)
                    self.global_best_fit = swarm[i].current_obj
                    #   store global best
                    self.performance.loc[str(self.iter_num)+'.'+str(count)] = analyse_result(copy.deepcopy(swarm[i].position),
                                                                                             swarm[i].datafra_result)

                    count += 1

            # update velocity and position
            for i in range(self.swarm_size):
                swarm[i].update_velocity(self.global_best_sol)
                swarm[i].update_position()

            #   store global best
            self.performance.to_pickle('global_best_solutions')
            print('performance stored in iteration :  '+str(self.iter_num))

            self.iter_num += 1
