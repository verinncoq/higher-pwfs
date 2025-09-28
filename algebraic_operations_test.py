import unittest
import algebraic_operations
import pwfs_framework

# Implementation of a segment supporting string algebra


class StringAffineSegment(algebraic_operations.StringSegment):

    # Arguments:
    # dim - dimension of the element
    # lefts and rights - multiple interval boundaries (exclusive)
    # c and b - multiple scaling factors and shifts of affine functions (c * x + b)
    def __init__(self, dim, lefts, rights, c, b):
        self._dim = dim
        self._lefts = lefts
        self._rights = rights
        self._c = c
        self._b = b

    def contains(self, x):
        result = True
        for i in range(self._dim):
            result = result and (self._lefts[i] <= x[i]) and (
                x[i] <= self._rights[i])
        return result

    def evaluate(self, x):
        if self.contains(x):
            result = []
            for i in range(self._dim):
                result.append(self._c[i] * x[i] + self._b[i])
            return result
        else:
            return None

    def compose(self, s):
        new_lefts = []
        new_rights = []
        new_c = []
        new_b = []
        for i in range(self._dim):
            left_projection = (self._lefts[i] - s._b[i]) / s._c[i]
            new_lefts.append(
                s._lefts[i] if left_projection <= s._lefts[i] else left_projection)
            right_projection = (self._rights[i] - s._b[i]) / s._c[i]
            new_rights.append(
                right_projection if right_projection <= s._rights[i] else s._rights[i])
            if new_lefts[i] >= new_rights[i]:
                return None
            new_c.append(self._c[i] * s._c[i])
            new_b.append(self._c[i] * s._b[i] + self._b[i])
        return StringAffineSegment(self._dim, new_lefts, new_rights, new_c, new_b)

    def concat(self, s):
        new_dim = self._dim + s._dim
        new_lefts = self._lefts + s._lefts
        new_rights = self._rights + s._rights
        new_c = self._c + s._c
        new_b = self._b + s._b
        return StringAffineSegment(new_dim, new_lefts, new_rights, new_c, new_b)


# Tests

class TestStringAlgebras(unittest.TestCase):

    def setUp(self):
        # Segments for two piecewise function
        segment11 = StringAffineSegment(1, [0.0], [0.25], [2.0], [4.0])
        segment12 = StringAffineSegment(1, [0.25], [0.5], [2.0], [3.0])
        segment13 = StringAffineSegment(1, [0.5], [0.75], [2.0], [2.0])
        segment14 = StringAffineSegment(1, [0.75], [1.0], [2.0], [1.0])

        segment21 = StringAffineSegment(1, [0.0], [0.25], [3.0], [0.0])
        segment22 = StringAffineSegment(1, [0.25], [0.5], [3.0], [-0.75])
        segment23 = StringAffineSegment(1, [0.5], [0.75], [3.0], [-1.5])
        segment24 = StringAffineSegment(1, [0.75], [1.0], [3.0], [-2.25])

        # First-level piecewise functions
        pwaf11 = algebraic_operations.StringPiecewiseFunction(
            [segment11, segment12])
        pwaf12 = algebraic_operations.StringPiecewiseFunction(
            [segment13, segment14])

        pwaf21 = algebraic_operations.StringPiecewiseFunction(
            [segment21, segment22])
        pwaf22 = algebraic_operations.StringPiecewiseFunction(
            [segment23, segment24])

        # Nested piecewise functions
        self.npwaf1 = algebraic_operations.StringPiecewiseFunction([pwaf11, pwaf12])
        self.npwaf2 = algebraic_operations.StringPiecewiseFunction([pwaf21, pwaf22])

        # Prepare some sample inputs that not lie on interval boundaries
        self.sample_inputs = [0.1, 0.2, 0.3, 0.4, 0.6, 0.7, 0.8, 0.9, 1.1]

    def test_compose_values(self):
        composed = self.npwaf1.compose(self.npwaf2)
        self.assertAlmostEqual(composed.evaluate([0.1])[0], 3.6)
        self.assertAlmostEqual(composed.evaluate([0.3])[0], 4.3)
        self.assertAlmostEqual(composed.evaluate([0.7])[0], 3.2)
        self.assertAlmostEqual(composed.evaluate([0.9])[0], 3.9)
        self.assertIsNone(composed.evaluate([1.1]))

    def test_compose_invariant(self):
        composed = self.npwaf1.compose(self.npwaf2)
        for x in self.sample_inputs:
            npwaf2_result = self.npwaf2.evaluate([x])
            if npwaf2_result is not None:
                composed_result = self.npwaf1.evaluate(npwaf2_result)
                if composed_result is not None:
                    self.assertAlmostEqual(composed.evaluate([x])[
                                           0], composed_result[0])
                else:
                    self.assertIsNone(composed.evaluate([x]))
            else:
                self.assertIsNone(composed.evaluate([x]))

    def test_concat_values(self):
        concatted = self.npwaf1.concat(self.npwaf2)
        self.assertAlmostEqual(concatted.evaluate([0.1, 0.1])[0], 4.2)
        self.assertAlmostEqual(concatted.evaluate([0.1, 0.1])[1], 0.3)
        self.assertAlmostEqual(concatted.evaluate([0.3, 0.9])[0], 3.6)
        self.assertAlmostEqual(concatted.evaluate([0.3, 0.9])[1], 0.45)
        self.assertAlmostEqual(concatted.evaluate([0.6, 0.7])[0], 3.2)
        self.assertAlmostEqual(concatted.evaluate([0.6, 0.7])[1], 0.6)
        self.assertAlmostEqual(concatted.evaluate([0.9, 0.3])[0], 2.8)
        self.assertAlmostEqual(concatted.evaluate([0.9, 0.3])[1], 0.15)
        self.assertIsNone(concatted.evaluate([0.1, 1.1]))

    def test_concat_invariant(self):
        concatted = self.npwaf1.concat(self.npwaf2)
        for x1 in self.sample_inputs:
            for x2 in self.sample_inputs:
                npwaf1_result = self.npwaf1.evaluate([x1])
                npwaf2_result = self.npwaf2.evaluate([x2])
                if npwaf1_result is None or npwaf2_result is None:
                    self.assertIsNone(concatted.evaluate([x1, x2]))
                else:
                    self.assertAlmostEqual(
                        concatted.evaluate([x1, x2])[0], npwaf1_result[0])
                    self.assertAlmostEqual(
                        concatted.evaluate([x1, x2])[1], npwaf2_result[0])
                                      
