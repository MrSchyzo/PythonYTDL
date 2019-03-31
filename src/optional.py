class Optional:
    def __init__(self, value):
        self._value = value

    @staticmethod
    def none():
        return Optional.of_nullable(None)

    @staticmethod
    def of(value):
        if value is None:
            raise ReferenceError
        return Optional(value)

    @staticmethod
    def of_nullable(value):
        return Optional(value)

    def has_value(self):
        return self._value is not None

    def or_else(self, value):
        return value if not self.has_value() else self._value

    def or_else_exec(self, execution):
        if self._value is None:
            execution()

    def map(self, f):
        if self._value is None:
            return Optional.none()
        return Optional.of_nullable(f(self._value))

    def flat_map(self, f):
        result = f(self._value)
        if not isinstance(result, Optional):
            raise TypeError("flat_map expects a function that returns an Optional")
        if result.has_value():
            return Optional.of(result._value)
        return Optional.none()

    def filter(self, f):
        if not self.has_value():
            return Optional.none()
        result = f(self._value)
        if not result:
            return Optional.none()
        return Optional.of(self._value)

    def get_value(self):
        if self.has_value():
            return self._value
        raise RuntimeError("Optional doesn't contain any value")

    def equals(self, other):
        if not isinstance(other, Optional):
            return False
        if isinstance(self._value, Optional):
            return self._value.equals(other._value)
        return self._value == other._value
