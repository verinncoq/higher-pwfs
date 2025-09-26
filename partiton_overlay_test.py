import unittest
import partition_overlay
import pwfs_framework

# Implementation of partition overlay for piecewise-affine functions


class SetInterval(partition_overlay.SetRegion):

    def __init__(self, left, right):
        #Right and left interval boundaries, inclusive
        self._left = left
        self._right = right

    def contains(self, x):
        return (self._left <= x) and (x <= self._right)

    def intersection(self, s):
        new_left = s._left if self._left <= s._left else self._left 
        new_right = self._right if self._right <= s._right else s._right 
        return SetInterval(new_left, new_right)

    def is_empty(self):
        return self._right < self._left


class AffineFunction(pwfs_framework.PartialFunction):

    def __init__(self, c, b):
        self._c = c
        self._b = b

    def evaluate(self, x):
        return self._c * x + self._b


class IntervalFastPartition(partition_overlay.FastPartition):

    def __init__(self):
        negative_region = SetInterval(-1.0, 0.0)
        positive_region = SetInterval(0.0, 1.0)
        super().__init__([negative_region, positive_region])

    def get_index(self, x):
        if -1.0 <= x <= 1.0:
            return int(0.0 <= x)
        else:
            return None

# Tests


class TestPartitionOverlay(unittest.TestCase):

    def setUp(self):
        #Create an overlayed function to verify
        segment1 = partition_overlay.SetSegment(SetInterval(-1.0, -0.5), AffineFunction(1.0, 0.0))
        segment2 = partition_overlay.SetSegment(SetInterval(-0.5, 0.0), AffineFunction(1.0, 0.0))
        segment3 = partition_overlay.SetSegment(SetInterval(0.0, 0.5), AffineFunction(1.0, 0.0))
        segment4 = partition_overlay.SetSegment(SetInterval(0.0, 1.0), AffineFunction(1.0, 0.0))
        self.overlay_pwf = partition_overlay.OverlayPiecewiseFunction([segment1, segment2, segment3, segment4], IntervalFastPartition())

    def test_overlay_evaluation(self):
        self.assertEqual(self.overlay_pwf.evaluate(1.0),1.0)

    def test_overlay_size(self):
        self.assertEqual(len(self.overlay_pwf.segments),2)

    def test_overlay_none(self):
        self.assertIsNone(self.overlay_pwf.evaluate(1.1))
