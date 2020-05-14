"""We calcualte time worked here."""


class ProductivitySystem(object):  # inteface class

    def __init__(self):
        self._roles = {
            'manager': ManagerRole,
            'secretary': SecretaryRole,
            'sales': SalesRole,
            'factory': FactoryRole
        }

    def get_role(self, role_key):
        # takes role key, returns role object
        role_type = self._roles.get(role_key)
        if not role_type:
            raise ValueError('role_id')
        return role_type

    def track(self, employees, hours):
        # takes employees list, returns how each worked
        for emp in employees:
            emp.work(hours)


# actual implementation classes
class ManagerRole(object):
    # returns how manager works
    def perform_duties(self, hours):
        print(f'manager is managering for {hours} hours')


class SecretaryRole(object):
    # returns how the secretary works
    def perform_duties(self, hours):
        print(f'secretary is secreting for {hours} hours')


class SalesRole(object):
    # return how sales work
    def perform_duties(self, hours):
        print(f'sales are selling for {hours} hours')


class FactoryRole(object):
    # return how factory worker works
    def perform_duties(self, hours):
        print(f'factory workers are factoring for {hours} hours')
