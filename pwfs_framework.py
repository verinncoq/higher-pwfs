from typing import TypeVar, Generic, Optional, Iterable

I = TypeVar('I')  # Input space
O = TypeVar('O')  # Output space


class Region(Generic[I]):
    def contains(self, x: I) -> bool:
        return True


class PartialFunction(Generic[I, O]):
    def evaluate(self, x: I) -> Optional[O]:
        return None


class Component(PartialFunction[I, O]):
    def __init__(self, region: Region[I], function: PartialFunction[I, O]):
        self.region = region
        self.function = function

    def evaluate(self, x: I) -> Optional[O]:
        if self.region.contains(x):
            return self.function.evaluate(x)
        else:
            return None


class PiecewiseFunction(Component[I, O]):
    def __init__(self, components: Iterable[Component[I, O]]):
        self.components = components

    def evaluate(self, x: I) -> Optional[O]:
        for component in self.components:
            result = component.evaluate(x)
            if result != None:
                return result
        return None
