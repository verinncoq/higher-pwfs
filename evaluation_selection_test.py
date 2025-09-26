import time
import unittest
import evaluation_selection
import pwfs_framework

# Implementation of a simple mock segment with configurable evaluation delay


class DelayedSegment(pwfs_framework.Segment):

    def __init__(self, delay):
        self._delay = delay

    def evaluate(self, x):
        time.sleep(self._delay)
        return x

# Tests for evaluation selection


class TestEvaluationSelection(unittest.TestCase):

    def setUp(self):
        fast_segment = DelayedSegment(0)
        slow_segment = DelayedSegment(0.1)
        self.selector_pwf = evaluation_selection.SelectorPiecewiseFunction(
            [fast_segment, slow_segment])
        for _ in range(100):
            self.selector_pwf.evaluate(1.0)

    def test_fastest_identified(self):
        fastest_element_idx = self.selector_pwf.segments.index(
            min(self.selector_pwf.segments, key=lambda x: x[0]))
        self.assertEqual(
            self.selector_pwf.segments[fastest_element_idx][2]._delay, 0)

    def test_number_trials(self):
        full_num_trials = sum(segment[1]
                              for segment in self.selector_pwf.segments)
        self.assertGreaterEqual(full_num_trials, 100)
