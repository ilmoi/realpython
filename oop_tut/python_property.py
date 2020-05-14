class Celsius(object):

    def __init__(self, temperature):
        self.temperature = temperature

    def to_fahrenheit(self):
        return (self.temperature * 1.8) + 32

    def set_temperature(self, value):
        print('going through Setter')
        self._temperature = value

    def get_temperature(self):
        print('going through Getter')
        return self._temperature

    temperature = property(get_temperature, set_temperature)
    # so even though we have self.temperature defined earlier - what this does is makes sure it always goes through GETTER/SETTER
    # property is a built-in function
    # property(fget=None, fset=None, fdel=None, doc=None)
    # it creates a property object aka <property object at 0x0000000003239B38>


print('1')
c = Celsius(10)
print('2')
f = c.to_fahrenheit()
print('3')
print(c.temperature, f)

print('==='*20)
print('another way of doing it')


class Celsius(object):

    def __init__(self, temperature):
        self.temperature = temperature

    def to_fahrenheit(self):
        return (self.temperature * 1.8) + 32

    @property  # getter
    def temperature(self):
        print('going through Getter')
        return self._temperature

    @temperature.setter  # setter
    def temperature(self, value):
        print('going through Setter')
        self._temperature = value


print('1')
c = Celsius(10)
print('2')
f = c.to_fahrenheit()
print('3')
print(c.temperature, f)
