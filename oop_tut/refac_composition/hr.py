"""We calc salaries here."""


class PayrollSystem(object):

    def __init__(self):
        self._policies = {
            1: SalaryPolicy(100),
            2: SalaryPolicy(30),
            3: CommissionPolicy(30, 30),
            4: HourlyPolicy(10),
            5: HourlyPolicy(5)
        }

    def get_policy(self, employee_id):
        # take in employee id, return salary policy
        policy = self._policies.get(employee_id)
        if not policy:
            raise ValueError(employee_id)
        return policy

    def calculate_payroll(self, employees):
        # take in employees list, return payroll for all
        for emp in employees:
            print(f'payroll for {emp.name} is {emp.calculate_payroll()}')
            print(f'sending to {emp.address}')


# layer 1
class PayrollPolicy(object):

    def __init__(self):
        self.hours = 0

    def track_work(self, hours):
        self.hours += hours


# layer 2
class SalaryPolicy(PayrollPolicy):

    def __init__(self, weekly_salary):
        super().__init__()  # make sure we have self.hours
        self.weekly_salary = weekly_salary

    def calculate_payroll(self):
        return self.weekly_salary/40*self.hours


class HourlyPolicy(PayrollPolicy):

    def __init__(self, rate):
        super().__init__()  # make sure we have self.hours
        self.rate = rate

    def calculate_payroll(self):
        return self.hours * self.rate


class CommissionPolicy(SalaryPolicy):

    def __init__(self, weekly_salary, commission):
        super().__init__(weekly_salary)
        self.commission = commission

    def calculate_payroll(self):
        return (self.weekly_salary + self.commission)/40*self.hours
