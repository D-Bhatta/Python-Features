import abc


class FormalInterface(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, "load_data")
            and callable(subclass.load_data)
            and hasattr(subclass, "extract_data")
            and callable(subclass.extract_data)
            or NotImplemented
        )

    @abc.abstractmethod
    def load_data(self, path: str, file_name: str):
        """Load data"""
        raise NotImplementedError

    @abc.abstractmethod
    def extract_data(self, full_path: str):
        """Extract data"""
        raise NotImplementedError


class Example1(FormalInterface):
    """ Example 1 """

    def load_data(self, path: str, file_name: str) -> str:
        """Overrides Load data"""
        pass

    def extract_data(self, full_path: str):
        """Overrides extract data"""
        pass


class Example2(FormalInterface):
    """ Example 1 """

    def load_data(self, path: str, file_name: str) -> str:
        """Overrides Load data"""
        pass

    def extract_data_wrong_name(self, full_path: str):
        """Doesn't Overrides extract data"""
        pass


Example1()

Example2()
