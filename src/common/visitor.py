from abc import ABCMeta, abstractmethod

class Visitor(metaclass=ABCMeta):
    @abstractmethod
    def foo(self):
        pass
