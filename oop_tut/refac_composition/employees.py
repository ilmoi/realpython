"""We list all employees here."""

from productivity import ProductivitySystem
from hr import PayrollSystem
from contacts import AddressBook


class EmployeeDatabase(object):

    def __init__(self):
        self._employees = [
            {
                'id': 1,
                'name': 'm',
                'role': 'manager'
            },
            {
                'id': 2,
                'name': 's',
                'role': 'secretary'
            },
            {
                'id': 3,
                'name': 's',
                'role': 'sales'
            },
            {
                'id': 4,
                'name': 'f',
                'role': 'factory'
            },
            {
                'id': 5,
                'name': 'ts',
                'role': 'secretary'
            }
        ]

        # link components
        self.productivity = ProductivitySystem()  # should I be calling this somewhere?
        self.payroll = PayrollSystem()
        self.addresses = AddressBook()

    @property  # getter for employees list
    def employees(self):
        return [self._create_employee(i+1) for i in range(5)]

    def _create_employee(self, id):
        self.id = id
        self.name = self._employees[id-1].get('name')
        self.role = self.productivity.get_role(self._employees[id-2].get('role'))
        self.policy = self.payroll.get_policy(id)
        self.address = self.addresses.get_employee_address(id)

        return Employee(self.id, self.name, self.role, self.policy, self.address)


class Employee(object):
    def __init__(self, id, name, role, policy, address):
        self.id = id
        self.name = name
        self.role = role
        self.policy = policy
        self.address = address

    def work(self, hours):
        # performs duties
        print('more text if wanted to')
        self.role.perform_duties(self, hours)
        # tracks hours
        self.policy.track_work(hours)

    def calculate_payroll(self):
        return self.policy.calculate_payroll()
