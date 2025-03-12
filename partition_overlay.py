from typing import Iterable

import pwfs_framework


class SetAlgebra:

    def intersection(self, s):
        return self

    def is_empty(self) -> bool:
        return True


class SetRegion(pwfs_framework.Region, SetAlgebra):
    pass


class SetComponent(pwfs_framework.Component, SetAlgebra):

    def __init__(self, region: SetRegion, function):
        super().__init__(region, function)

    def intersection(self, s):
        return SetComponent(self.region.intersection(s), self.function)

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

    def __init__(self, components: Iterable[SetComponent], overlay_partition: FastPartition):
        self.partition = overlay_partition
        self.components = []
        for partition_region in overlay_partition.regions:
            sub_pwf_components = []
            for component in components:
                intersected_component = component.intersection(
                    partition_region)
                if not intersected_component.is_empty():
                    sub_pwf_components.append(intersected_component)
            self.components.append(
                pwfs_framework.PiecewiseFunction(sub_pwf_components))

    def evaluate(self, x):
        i = self.partition.get_index(x)
        if i is None:
            return None
        return self.components[i].evaluate(x)
