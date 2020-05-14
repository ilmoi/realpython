"""https://dbader.org/blog/writing-clean-python-with-namedtuples"""

from collections import namedtuple

# note how we're able to just have one string with all attributes
Car = namedtuple('Car', 'mileage color')

# namedtuples come with a built in nice __repr__ method
c = Car(123, 'red')
print(c)

# because namedtuple is a class we can further extend it:


class OldCar(Car):

    def whenmade(self):
        return (f'this {self.color} sedan with {self.mileage} miles was made in 1994!')

    # this is exactly what the dudes in real python were doing during the itertools tutorial!


oc = OldCar(123, 'red')
print(oc.whenmade())

# we can easily convert to dictionary
print(oc._asdict())

# we can create a shallow copy of the tuple and replace some attrs:
oc2 = oc._replace(color='blue')
print(oc2)
