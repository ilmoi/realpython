"""This is where all employee classes are defined."""

# this is an example of an abstract base class. It exists to be inherited but never instantiated
# we can therefore derive it from ABC and add an @abstractmethod to prevent ppl from instantiating it
# from abc import ABC, abstractmethod
# class Employee(ABC):  # ABC = telling other devs cant be instantiated
#
#     def __init__(self, id, name):
#         self.id = id
#         self.name = name
#
#     @abstractmethod  # telling other devs if they derive from this class, this must be overwritten
#     def calculate_payroll(self):
#         pass

# main class

# base class interface = methods, properties, attributes of base class
# base class implementation = code that implements the class interface
# most of the time you want to inherit all methods, but implement many interfaces
# you should use inheritance when there is a IS A type relationship
# basically i think what he's saying is: interface = what's exposed, implementation = the actual code. YOU WANT THE IMPLEMENTATION, NOT NECESSERILY THE INTERFACE


class Employee(object):

    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.address = None

# first line of subclasses


class SalaryEmployee(Employee):

    def __init__(self, id, name, weekly_salary):
        super().__init__(id, name)
        self.weekly_salary = weekly_salary

    def calculate_payroll(self):
        return self.weekly_salary


class HourlyEmployee(Employee):

    def __init__(self, id, name, hours, rate):
        super().__init__(id, name)
        self.hours = hours
        self.rate = rate

    def calculate_payroll(self):
        return self.hours * self.rate


class CommissionEmployee(SalaryEmployee):

    def __init__(self, id, name, salary, commission):
        super().__init__(id, name, salary)
        self.commission = commission

    def calculate_payroll(self):
        fixed = super().calculate_payroll()
        return fixed + self.commission

# 2nd line of subclasses


class Manager(SalaryEmployee):

    def __init__(self, id, name, salary):
        super().__init__(id, name, salary)

    def work(self, hours):
        print(f'{self.name} screms and yuells for {hours} hours')


class Secretary(SalaryEmployee):

    def __init__(self, id, name, salary):
        super().__init__(id, name, salary)

    def work(self, hours):
        print(f'{self.name} expends {hours} doing office paperwork')


class SalesPerson(CommissionEmployee):

    def __init__(self, id, name, salary, commission):
        super().__init__(id, name, salary, commission)

    def work(self, hours):
        print(f'{self.name} expends {hours} on the phone')


class FactoryWorker(HourlyEmployee):

    # interesting, turns out you DONT HAVE TO add the below lines if all you're doing is inhereting
    def __init__(self, id, name, hours, rate):
        super().__init__(id, name, hours, rate)

    def work(self, hours):
        print(f'{self.name} manufactures gadgets for {hours} hours')


# 3rd line of subclasses

# whichever we pass first, will be the one called first
# because we passed secretary first, we had to change __init__ and calculate_payroll to take them from hourly employee
# that said the work method is correctly taken from the secretary
class TempSecretary(Secretary, HourlyEmployee):

    def __init__(self, id, name, hours, rate):
        HourlyEmployee.__init__(self, id, name, hours, rate)

    def calculate_payroll(self):
        return HourlyEmployee.calculate_payroll(self)


# class TempSecretary(HourlyEmployee, Secretary):
#     # pass
#
#     def __init__(self, id, name, hours, rate):
#         HourlyEmployee.__init__(self, id, name, hours, rate)
#
#     def calculate_payroll(self):
#         return HourlyEmployee.calculate_payroll(self)
#
#     def work(self):
#         return Secretary.work()
