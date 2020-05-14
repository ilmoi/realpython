"""We define addresses here."""


class AddressBook(object):

    def __init__(self):
        self._addresses = {
            1: Address('dzirnavu', 'riga', '111'),
            2: Address('dzirnavu', 'riga', '222'),
            3: Address('dzirnavu', 'riga', '333'),
            4: Address('dzirnavu', 'riga', '444'),
            5: Address('dzirnavu', 'riga', '555')
        }

    def get_employee_address(self, employee_id):
        # take in emp id, return their address
        return self._addresses.get(employee_id)


class Address(object):

    def __init__(self, street, city, zip):
        # define what an adderss is
        self.street = street
        self.city = city
        self.zip = zip

    def __str__(self):
        # define how an address is displayed
        return f'GOING THROUGH STR METHOD: {self.street}, {self.city}, {self.zip}'
