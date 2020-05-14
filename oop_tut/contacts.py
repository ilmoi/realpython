# composite = class that contains an object of another class
# component = another class that is contained as an object inside the first


class Address(object):

    def __init__(self, street, city, state, zipcode, street2=''):
        self.street = street
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.street2 = street2

    def __str__(self):
        lines = [self.street]
        if self.street2:
            lines.append(self.street2)
        lines.append(f'{self.city}, {self.state}, {self.zipcode}')
        return '\n'.join(lines)


# riga = Address('dzirnavu', 'riga', 'soviet republic of latvia', '1010', '34a-15')
# print(riga)
