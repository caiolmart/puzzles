""" Module solves Kombucha Problem. """

from typing import List, Tuple
import numpy as np


class State:
    """ State of the problem. """

    def __init__(self, visited, cur_chair):
        self.visited = visited
        self.cur_chair = cur_chair


class KombuchaProblem:
    """ States, actions and costs of the problem. """

    def __init__(self, n_chairs):
        self.n_chairs = n_chairs

    def left_right_probabilities(self, cur_chair: int) -> Tuple[float, float]:
        """ Probabilities to go left or right, if not visited."""

        left_proba = (self.n_chairs - cur_chair) / (self.n_chairs + 1)
        right_proba = (cur_chair + 1) / (self.n_chairs + 1)

        return left_proba, right_proba

    def initial_state(self) -> State:
        """ State is the list of visited chair, the current_chair (initial 0)
        and the current direction (-1 for left 1 to right - starts at 0). """

        visited = [0] * self.n_chairs
        return State(visited, 0)

    def actions(self, state: State) -> List[Tuple[int, float]]:
        """ Returns tuples with actions and their probabilities."""

        left_p, right_p = self.left_right_probabilities(state.cur_chair)
        return [(-1, left_p), (1, right_p)]

    def get_new_pos(self, state, action):
        """ Gets new position given state and action. """
        new_pos = state.cur_chair - action
        if new_pos == -1:
            return self.n_chairs - 1
        if new_pos == self.n_chairs:
            return 0
        return new_pos

    def next_state(self, state: State, action: int):
        """ Returns new state with action. """

        new_state = State(state.visited.copy(),
                          state.cur_chair)
        new_state.visited[new_state.cur_chair] = 1
        cost = 1
        new_state.cur_chair = self.get_new_pos(new_state, action)
        return new_state, cost

    def is_final_state(self, state):
        """ Checks if state is final. """
        if (1 - state.visited[state.cur_chair]) + \
                sum(state.visited) >= self.n_chairs:
            return True
        return False


def get_expected_time(
        problem: KombuchaProblem,
        state: State,
        cache: dict,
        acc_prob: float,
        prob_threshold: float = 1e-40):
    """ Gets the expected time of the problem. """
    key = (tuple(state.visited), state.cur_chair)
    if key in cache:
        return cache[key]
    if problem.is_final_state(state):
        cache[key] = 0
        return cache[key]

    actions = problem.actions(state)
    total_expected = 0
    for action in actions:
        next_state, cost = problem.next_state(state, action[0])
        # If the accumulated probability is less than threshold stop expanding.
        if acc_prob < prob_threshold:
            total_expected += action[1] * cost
        else:
            total_expected += action[1] * (cost + get_expected_time(
                problem, next_state, cache, action[1] * acc_prob,
                prob_threshold=prob_threshold))
    cache[key] = total_expected
    return total_expected


if __name__ == '__main__':
    """ Solves the problem from its initial state. """

    cache = {}
    n_chairs = 3
    problem = KombuchaProblem(n_chairs)
    expected_time = get_expected_time(
        problem, problem.initial_state(), cache, 1)
    print(f'Expected time for {n_chairs} chairs: {expected_time}')

    cache = {}
    n_chairs = 4
    problem = KombuchaProblem(n_chairs)
    expected_time = get_expected_time(
        problem, problem.initial_state(), cache, 1)
    print(f'Expected time for {n_chairs} chairs: {expected_time}')

    cache = {}
    n_chairs = 5
    problem = KombuchaProblem(n_chairs)
    expected_time = get_expected_time(
        problem, problem.initial_state(), cache, 1)
    print(f'Expected time for {n_chairs} chairs: {expected_time}')

    cache = {}
    n_chairs = 10
    problem = KombuchaProblem(n_chairs)
    expected_time = get_expected_time(
        problem, problem.initial_state(), cache, 1)
    print(f'Expected time for {n_chairs} chairs: {expected_time}')

    cache = {}
    n_chairs = 30
    problem = KombuchaProblem(n_chairs)
    expected_time = get_expected_time(
        problem, problem.initial_state(), cache, 1)
    print(f'Expected time for {n_chairs} chairs: {expected_time}')

    for thresh in np.logspace(-1, -50, num=50):
        cache = {}
        n_chairs = 30
        problem = KombuchaProblem(n_chairs)
        expected_time = get_expected_time(
            problem, problem.initial_state(), cache, 1, prob_threshold=thresh)
        print(f'Expected time for {n_chairs} chairs with threshold {thresh}: '
              f'{expected_time}')
