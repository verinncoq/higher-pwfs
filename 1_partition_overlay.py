from typing import Iterable

import pwfs_framework


class SetAlgebra:

    def intersection(self, s):
        return self

    def is_empty(self) -> bool:
        return True


class SetRegion(pwfs_framework.Region, SetAlgebra):
    pass


class SetSegment(pwfs_framework.Segment, SetAlgebra):

    def __init__(self, region: SetRegion, function):
        super().__init__(region, function)

    def intersection(self, s):
        return SetSegment(self.region.intersection(s), self.function)

    def is_empty(self):
        return self.region.is_empty()


class FastPartition:

    def __init__(self, regions: Iterable[SetRegion]):
        self.regions = list(regions)

    def get_index(self, x):
        # Fast implementation
        return 0

    def find_region(self, x):
        i = self.get_index(x)
        if i is None:
            return None
        return self.regions[i]


class OverlayPiecewiseFunction(pwfs_framework.PiecewiseFunction):

    def __init__(self, segments: Iterable[SetSegment], overlay_partition: FastPartition):
        self.partition = overlay_partition
        self.segments = []
        for partition_region in overlay_partition.regions:
            sub_pwf_segments = []
            for segment in segments:
                intersected_segment = segment.intersection(
                    partition_region)
                if not intersected_segment.is_empty():
                    sub_pwf_segments.append(intersected_segment)
            self.segments.append(
                pwfs_framework.PiecewiseFunction(sub_pwf_segments))

    def evaluate(self, x):
        i = self.partition.get_index(x)
        if i is None:
            return None
        return self.segments[i].evaluate(x)
