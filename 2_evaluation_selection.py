from typing import Iterable
import random
import time

import pwfs_framework


class SelectorPiecewiseFunction(pwfs_framework.PiecewiseFunction):

    def __init__(self, implementations: Iterable[pwfs_framework.PiecewiseFunction]):
        self.components = []
        for implementation in implementations:
            # a triple: (average time, number of trials (time measurements), implementation)
            self.components.append((0, 0, implementation))

    def evaluate(self, x):
        # 1 in 5 chance to select a random implementation
        use_best_impl = random.randint(0, 4) != 0
        selected_idx = None
        if use_best_impl:
            selected_idx = self.components.index(
                min(self.components, key=lambda x: x[0]))
        else:
            selected_idx = random.randrange(len(self.components))
        avg_time, num_trials, selected_impl = self.components[selected_idx]
        start = time.time()
        result = selected_impl.evaluate(x)
        end = time.time()
        elapsed_secs = end - start
        new_num_trials = num_trials + 1
        new_avg_time = avg_time + (elapsed_secs - avg_time) / new_num_trials
        self.components.index[selected_idx] = (
            new_avg_time, new_num_trials, selected_impl)
        return result
