import numpy as np


def test_func(input):
    w = [1,2,3,10,20,30,50,100]
    s = [a * b for a, b in zip(input, w)]
    return sum(s)


class Particle:
    # number of dimensions : number of indicators + BS + BD
    num_dimension = 8

    def __init__(self):
        self.position = []
        self.velocity = [0] * Particle.num_dimension
        self.post_best = []
        self.obj_best = 10000.0
        self.current_obj = 10000.0

        # initialize position
        self.initialize_position(num_dimension=Particle.num_dimension)

    # this method initializes the weights of indicators
    # to do: initialize the BS and BD
    def initialize_position(self, num_dimension):
        rand = np.random.ranf(num_dimension-1)
        rand = np.append(rand, [0, 1])
        rand.sort()
        # w = np.zeros(dtype=np.float64, shape=(num_dimension,))
        for i in range(len(rand)-1):
            self.position.append(rand[i + 1] - rand[i])

    # evaluate current fitness
    def evaluate(self, obj_func):

        self.current_obj = obj_func(self.position)

        # check to see if the current position is an individual best
        # type of optimization is MINIMIZE
        if self.current_obj < self.obj_best:
            self.post_best = list(self.position)
            self.obj_best = self.current_obj

    # update the velocity of particle
    def update_velocity(self, global_best):
        if len(self.position) != len(global_best):
            raise ValueError('the dimension of global best did not correspond with dimension of particles')
        else:
            w = 0.5  # constant inertia weight (how much to weigh the previous velocity)
            c1 = 2  # cognitive constant
            c2 = 2  # social constant

            for i in range(0, Particle.num_dimension):
                r1 = np.random.random()
                r2 = np.random.random()

                vel_cognitive = c1 * r1 * (self.post_best[i] - self.position[i])
                vel_social = c2 * r2 * (global_best[i] - self.position[i])
                self.velocity[i] = w * self.velocity[i] + vel_cognitive + vel_social

    def update_position(self, bounds):
        for i in range(Particle.num_dimension):
            self.position[i] = self.position[i] + self.velocity[i]

            # to do: the correction with bounds must be added
            # adjust maximum position if necessary
            if self.position[i] > bounds[i][1]:
                self.position[i] = bounds[i][1]

            # adjust maximum position if necessary
            if self.position[i] < bounds[i][0]:
                self.position[i] = bounds[i][0]

        # correct the weights so that the sum of them remains equal to 1
        s = sum(self.position)
        self.position = [a/s for a in self.position]
        print(self.position)


class PSO:
    def __init__(self, obj_func, bounds, swarm_size, max_iter):
        self.global_best_fit = 10000.0
        self.global_best_sol = []
        self.iter_num = 0

        # create swarm (population)
        swarm = []
        for i in range(0, swarm_size):
            swarm.append(Particle())

        # optimization loop
        while self.iter_num < max_iter:
            # iterate over particles in swarm and evaluate fittness
            for i in range(swarm_size):
                swarm[i].evaluate(obj_func)

                # determine the best global particle
                # type of optimization is MINIMIZE
                if swarm[i].current_obj < self.global_best_fit:
                    self.global_best_sol = list(swarm[i].position)
                    self.global_best_fit = swarm[i].current_obj
                    print(self.global_best_sol)

            for i in range(swarm_size):
                swarm[i].update_velocity(self.global_best_sol)
                swarm[i].update_position(bounds)

            self.iter_num += 1





if __name__ == '__main__':
    bound = [(0,1),(0,1),(0,1),(0,1),(0,1),(0,1),(0,1),(0,1)]
    pso = PSO(test_func, bound, 100, 100 )
    print(pso.global_best_sol)
    print(sum(pso.global_best_sol))