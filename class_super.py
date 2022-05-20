#!/usr/bin/env python3


class A:
    def __init__(self, name):
        self.name = name
        self.foo = "foo"
        self.bar = "bar"
        self.guess = "iamnotsure"

    def upper(self):
        print(self.name.upper())


class B(A):
    def __init__(self, name, other):
        super().__init__(name)
        self.other = other
        self.bar = "BAR"
        print(self.guess)
        print(self.bar)

    def upper(self):
        print("I am using super() now")
        super().upper()

    def lower(self):
        print(self.other.lower())


a = A("xyz")
a.upper()

b = B("xyz", "ABC")
b.upper()
b.lower()
