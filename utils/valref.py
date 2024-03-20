# TODO : more operator overloading ?

class ValRef:
    """
    The goal of this thing is to allow passing integer values by reference
    """
    def __init__(self, value: int | float):
        self.value = value

    def set(self, value: int | float):
        self.value = value

    def get(self) -> int | float:
        return self.value

    def __add__(self, other):
        """
        + operator overloading
        """
        r = ValRef(self.value)
        other_type = type(other)
        match other_type:
            case self.__class__:
                r.value += other.get()
            case type(r.value):
                r.value += other
            case _:
                assert "Unsupported type for IntRef operation"
        return r

    def __sub__(self, other):
        """
        - operator overloading
        """
        r = ValRef(self.value)
        other_type = type(other)
        match other_type:
            case self.__class__:
                r.value -= other.get()
            case type(r.value):
                r.value -= other
            case _:
                assert "Unsupported type for IntRef operation"
        return r

    def __iadd__(self, other):
        """
        += operator overloading
        """
        other_type = type(other)
        match other_type:
            case self.__class__:
                self.value += other.get()
            case type(self.value):
                self.value += other
            case _:
                assert "Unsupported type for IntRef operation"

    def __isub__(self, other):
        """
        -= operator overloading
        """
        other_type = type(other)
        match other_type:
            case self.__class__:
                self.value -= other.get()
            case type(self.value):
                self.value -= other
            case _:
                assert "Unsupported type for IntRef operation"
