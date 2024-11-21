import numpy as np
from numpy._typing import NDArray

class Particle:
    def __init__(self, position: NDArray, velocity: NDArray, bounds: NDArray):
        self.position = position
        self.velocity = velocity
        self.best_position = np.copy(position)
        self.best_value = float('inf')
        self.bounds = bounds

    def update_velocity(self, global_best_position: NDArray, w: float, c1: float, c2: float):
        r1 = np.random.rand(2)
        r2 = np.random.rand(2)
        self.velocity = (w * self.velocity +
                         c1 * r1 * (self.best_position - self.position) +
                         c2 * r2 * (global_best_position - self.position))

    def update_position(self):
        self.position += self.velocity
        self.position = np.clip(self.position, self.bounds[0], self.bounds[1])

    def evaluate(self, obj_function):
        value = obj_function(self.position)
        if value < self.best_value:
            self.best_value = value
            self.best_position = np.copy(self.position)
        return value

class PSOAlgorithm:
    def __init__(self, num_particles:int=30, max_iter:int=100, bounds:tuple[float,float]=(-5, 5), inertia_decrease:bool=False):
        self.num_particles = num_particles
        self.max_iter = max_iter
        self.bounds = np.array(bounds)
        self.swarm = []
        self.global_best_position = None
        self.global_best_value = float('inf')
        self.current_iter = 0
        self.inertia_decrease = inertia_decrease

    def initialize_swarm(self):
        for _ in range(self.num_particles):
            position = np.random.uniform(self.bounds[0], self.bounds[1], size=2)
            velocity = np.random.uniform(-1, 1, size=2)
            particle = Particle(position, velocity, self.bounds)
            self.swarm.append(particle)

    def step(self, w: float, c1: float, c2: float):
        if self.inertia_decrease:  
            w = self._calculate_inertia_weight(w)

        for particle in self.swarm:
            value = particle.evaluate(self.obj_function)
            if value < self.global_best_value:
                self.global_best_value = value
                self.global_best_position = np.copy(particle.position)

            particle.update_velocity(self.global_best_position, w, c1, c2)
            particle.update_position()

        self.current_iter += 1

    def _calculate_inertia_weight(self, w_max):
        w_min = w_max/10
        # Постепенное уменьшение инерции
        return w_max - (w_max - w_min) * (self.current_iter / self.max_iter)

    def is_finished(self) -> bool:
        return self.current_iter >= self.max_iter

    def get_swarm_data(self):
        positions = np.array([particle.position for particle in self.swarm])
        return positions, self.global_best_position, self.global_best_value, self.current_iter

    @staticmethod
    def obj_function(x: NDArray) -> float:
        return 8 * x[0] * x[0] + 4 * x[0] * x[1] + 5 * x[1] * x[1]
