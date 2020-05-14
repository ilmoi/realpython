"""This is where the hr functionality sits."""


# this is what we would call an "interface" implemented by all other classes
# that's also why it's prefixed with the word "I"
class PayrollSystem(object):

    def calculate_payroll(self, employees):
        print('---------------------')
        print('calculating payroll')
        for emp in employees:
            print(f'{emp.name}\'s payroll is {emp.calculate_payroll()}')
            if emp.address:
                print(f'$$$ SENT TO {emp.address}')
        print('---------------------')
