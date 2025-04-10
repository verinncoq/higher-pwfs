from typing import List
import pwfs_framework


class StringAlgebra:

    def compose(self, f):
        return None

    def concat(self, f):
        return None


class StringSegment(pwfs_framework.Segment, StringAlgebra):

    def compose(self, f):
        return super().compose(f)

    def concat(self, f):
        return super().concat(f)

    def evaluate(self, x):
        return super().evaluate(x)


class StringPiecewiseFunction(pwfs_framework.PiecewiseFunction, StringSegment, StringAlgebra):

    def __init__(self, segments: List[StringSegment]):
        self.string_segments = segments
        super().__init__(segments)

    def compose(self, f):
        result_segments = []
        for segment in self.string_segments:
            for f_segment in f.string_segments:
                new_segment = segment.compose(f_segment)
                if new_segment is None:
                    return None
                result_segments.append(new_segment)
        return StringPiecewiseFunction(result_segments)

    def concat(self, f):
        result_segments = []
        for segment in self.string_segments:
            for f_segment in f.string_segments:
                new_segment = segment.concat(f_segment)
                if new_segment is None:
                    return None
                result_segments.append(new_segment)
        return StringPiecewiseFunction(result_segments)
