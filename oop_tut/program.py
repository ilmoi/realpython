"""This is where the main app runs."""
import backtrace
import hr
import employees
import productivity
import contacts

print(employees.TempSecretary.__mro__)

# vadim = employees.Employee(1, 'vadim')
aaron = employees.Manager(2, 'aaron', 1000)
aarona = employees.Secretary(3, 'aarona', 100)
cheng = employees.FactoryWorker(4, 'cheng', 10, 40)
luo = employees.SalesPerson(5, 'luo', 500, 300)
joanna = employees.TempSecretary(6, 'joanna', 10, 30)

# here we're adding an address object to aaron's object. so object inside of obj.
aaron.address = contacts.Address('dzirnavu', 'riga', 'soviet republic of latvia', '1010', '34a-15')

employees = [aaron, aarona, cheng, luo, joanna]

productivity_tracker = productivity.ProductivityTracker()
productivity_tracker.track(employees, 40)

payroll_system = hr.PayrollSystem()
payroll_system.calculate_payroll(employees)
