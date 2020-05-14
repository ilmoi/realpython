"""https://realpython.com/python-data-classes/"""

# from __future__ import dataclasses
import timeit
from pympler import asizeof
from typing import List, Any
from dataclasses import dataclass, make_dataclass, field, fields


@dataclass
class DataClassCard:
    rank: str
    suit: str


queen_of_hearts = DataClassCard('Q', 'Hearts')
print(queen_of_hearts)
print(queen_of_hearts.rank)
print(queen_of_hearts == DataClassCard('Q', 'Hearts'))

# benefits
# 1 - less boilerplate code
# 2 - __repr__ already implemented (just like namedtuples!)
# 3 - __eq__ already implemented
# 4 - not immutable like namedtuple

# the new proposal - https://www.python.org/dev/peps/pep-0494/
# before you would attach types as comments, eg:
primes = []  # List[int]
# but now you can do:
primes: List[int] = []
# where everything between the : and = is a type hint
# NOTE 1: you need to import typing.List
# NOTE 2: it doesn't actually enforce anything - eg I can still append a non int to the list:
primes.append('a')
print(primes)


print("-------------------- BASICS --------------------")
# first way of making one
@dataclass
class Position:
    """Describes our position on planet Earth!"""
    name: str
    lon: float = 0.0  # default value
    lat: float = 0.0

    # defining datatypes is MANDATORY - otherwise the below won't appear in instances
    wontAppeal = 0.0

    # if you don't know what datatype it will be, use any
    dunno: Any = None

    # class methods work as expected
    def lon_distance(self, other):
        return self.lon - other.lon


p = Position('Oslo', 10.8, 59.9)
print(p)

# check defaults
NullIsland = Position('Null')
print(NullIsland)

# second way of making one
# Position = make_dataclass('Position', ['name', 'lon', 'lat'])
# Position = make_dataclass('Position', 'name, lat, lon') #does NOT work
q = Position('Riga', 1, 20)
print(q)

print(p.lon_distance(q))


print("-------------------- ADV --------------------")
RANKS = '2 3 4 5 6 7 8 9 10 J Q K A'.split()
SUITS = '♣ ♢ ♡ ♠'.split()


def make_french_deck():
    return [PlayingCard(r, s) for s in SUITS for r in RANKS]


@dataclass
class PlayingCard:
    rank: str
    suit: str
    # test: jibberish #note it wouldn't work if you just apped some gibberish into here

    def __str__(self):
        return f'{self.suit}, {self.rank}'


@dataclass
class Deck:
    # cards: List[PlayingCard] = make_french_deck() #DO NOT do this - mutable argument problem
    cards: List[PlayingCard] = field(default_factory=make_french_deck)  # the right way to do it

    def __str__(self):
        # NOTE the !s specifier - it means we specifically wnat to use the string version of the repr for class above
        # NOTE the alternative would be to use !r and call __repr__
        cards = ', '.join(f'{c!s}' for c in self.cards)
        return f'{self.__class__.__name__}({cards})'


queen_of_hearts = PlayingCard('Q', 'Hearts')
ace_of_spades = PlayingCard('A', 'Spades')
two_cards = Deck([queen_of_hearts, ace_of_spades])
print(queen_of_hearts)  # follows str
print(two_cards)  # NOTE: need a str method at BOTH of the classes


d = make_french_deck()
print(len(d))

dd = Deck()
print(dd)


print("-------------------- FIELD --------------------")
@dataclass
class Doggo:
    # field() supports the following arguments:

    # repr: Use field in repr of the object? (Default is True.)
    test_repr: str = field(repr=False)

    # compare: Include the field in comparisons? (Default is True.)
    test_compare: str = field(compare=False)

    # NOTE: default arguments need to go AFTER non-default (during function definition) arguments or python will throw an error
    # default: Default value of the field
    test_def: str = field(default='potato')

    # default_factory: Function that returns the initial value of the field
    # AS PER ABOVE
    # NOTE: YOU CAN'T SPECIFY BOTH DEFAULT AND DEFAULT FACTORY AT THE SAME TIME

    # init: Use field in .__init__() method? (Default is True.)
    test_init: str = field(init=False)

    # hash: Include the field when calculating hash()? (Default is to use the same as for compare.)
    # metadata: A mapping with information about the field
    # metadata is not used by dataclasses themselves but rather is avaialble to other devs / 3rd party packages
    test_metadata: str = field(default='12345', metadata={'unit': 'degrees'})


print(fields(Doggo))
h = Doggo('not_repr', 'not_compare')
h.test_init = 'not init'  # if we don't set this, next line throws an error.Thus it allows us not to set this during initation, but in order for the instance to work propertly it still needs to be set!
print(h)  # not printing repr as expected


print("-------------------- @DATACLASS DECORATOR --------------------")
# We can actually customize the decorator at the very top:
# init: Add .__init__() method? (Default is True.)
# repr: Add .__repr__() method? (Default is True.)
# eq: Add .__eq__() method? (Default is True.)
# order: Add ordering methods? (Default is False.)
# unsafe_hash: Force the addition of a .__hash__() method? (Default is False.)
# frozen: If True, assigning to fields raise an exception. (Default is False.) NOTE: this basically makes the class immutable, like namedtuple, NOTE: this fails if you have an immutagble class holding a list of immutable classes (like in the deck example above). The list is still modifiable.


@dataclass(order=True)
class PlayingCard:
    rank: str
    suit: str


# now we can compare them
# NOTE they are compared as if they were TUPLES - because Q comes after A it's considered "bigger"
a_spades = PlayingCard('A', 'spades')
q_hearts = PlayingCard('Q', 'hearts')
print(q_hearts > a_spades)


# but that's a shitty ranking system - a better one would be based on the order we lay cards in
# here's an imaginary way of doing it:
RANKS = '2 3 4 5 6 7 8 9 10 J Q K A'.split()
SUITS = '♣ ♢ ♡ ♠'.split()
card = PlayingCard('Q', '♡')
print(
    RANKS.index(card.rank) * len(SUITS) + SUITS.index(card.suit)
)


@dataclass(order=True)
class PlayingCard:
    sort_index: int = field(init=False, repr=False)
    rank: str
    suit: str

    # this method will make order work correctly - allows for special processing after the original init method
    def __post_init__(self):
        self.sort_index = RANKS.index(self.rank) * len(SUITS) + SUITS.index(self.suit)

    def __str__(self):
        return f'{self.suit}{self.rank}'


a_spades = PlayingCard('A', '♣')
q_hearts = PlayingCard('Q', '♡')
print(q_hearts > a_spades)

# we can now also create a sorted deck
@dataclass
class Deck:
    cards: List[PlayingCard] = field(default_factory=make_french_deck)  # the right way to do it

    def __repr__(self):
        cards = ', '.join(f'{c!s}' for c in self.cards)
        return f'{self.__class__.__name__}({cards})'


# NOTE how we call the sorted method inside of the deck method, not the other way around (it would break). In this way we're overriding default_factory with our own method, which happens to produce a sorted list
sd = Deck(sorted(make_french_deck()))
print(sd)


print("-------------------- SUBCLASSING --------------------")


@dataclass
class Country:
    country: str
    lat: float = 0.0
    lon: float = 0.0


@dataclass
class Capital(Country):
    capital_city: str = 'Unknown'  # need to add a default to prevent default argument error


l = Country('Latvia')
# one way to do it - feels more like composition
r = Capital(l, 'Riga')
# another way to do it - probably the right way to do it
r2 = Capital('Latvia', capital_city='Riga')
print(r)
print(r2)


print("-------------------- OPTIMIZATION --------------------")
# the same as in normal classes we can use slots to optimize memory efficiency


@dataclass
class SlotCountry:
    # used to list all class attributes
    # no default values allowed
    # variables NOT in slots not allowed
    __slots__ = ['country', 'lat', 'lon']
    country: str
    lat: float
    lon: float
    # another: str #NOTE produces an error since not in __slots__


l = Country('Latvia', 22, 11)
slot_l = SlotCountry('Latvia', 22, 11)
# print(l, slot_l)
print(f'normal country... {asizeof.asizeof(l)}')
print(f'slotted country... {asizeof.asizeof(slot_l)}')

timeit.timeit('l.country', setup="l=Country('Latvia', 22, 11)", number=999, globals=globals())
