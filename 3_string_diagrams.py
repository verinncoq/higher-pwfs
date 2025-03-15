from typing import List
import pwfs_framework


class StringAlgebra:

    def compose(self, f):
        return None

    def concat(self, f):
        return None


class StringComponent(pwfs_framework.Component, StringAlgebra):

    def compose(self, f):
        return super().compose(f)

    def concat(self, f):
        return super().concat(f)

    def evaluate(self, x):
        return super().evaluate(x)


class StringPiecewiseFunction(pwfs_framework.PiecewiseFunction, StringComponent, StringAlgebra):

    def __init__(self, components: List[StringComponent]):
        self.string_components = list(components)
        super().__init__(components)

    def compose(self, f):
        result_components = []
        for component in self.string_components:
            for f_component in f.string_components:
                new_component = component.compose(f_component)
                if new_component is None:
                    return None
                result_components.append(new_component)
        return StringPiecewiseFunction(result_components)

    def concat(self, f):
        result_components = []
        for component in self.string_components:
            for f_component in f.string_components:
                new_component = component.concat(f_component)
                if new_component is None:
                    return None
                result_components.append(new_component)
        return StringPiecewiseFunction(result_components)
