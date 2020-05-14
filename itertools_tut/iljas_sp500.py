import time
import functools
from collections import namedtuple
import itertools
import csv
import os
import timeit
import copy
import datetime
from memory_profiler import profile, memory_usage

os.chdir('/Users/ilja/Dropbox/realpython/itertools_tut')

# count the length
# with open('sp500.csv', 'r') as f:
#     reader = csv.reader(f)
#     print(len(list(reader)))

# ==============================================================================
# PART 1
# Read data from the CSV file and transform it into a sequence gains of daily percent changes using the “Adj Close” column.


def open_sp500():
    with open('sp500.csv', 'r') as f:
        reader = csv.DictReader(f)

        # naive - 0.864s
        # days = []
        # for row in reader:
        #     days.append(float(row['Adj Close'].strip()))
        # return days

        # better - 0.053s
        for row in reader:
            yield float(row['Adj Close'].strip())


def pairwise(iter1, iter2=None):
    if iter2 == None:
        iter1, iter2 = itertools.tee(iter1)
    next(iter2, None)
    return zip(iter1, iter2)


def calc_daily_gains(days):

    # print('running')

    # ==========================================================================
    # EXPECTING AN ITERABLE

    # naive - 0.19s
    # gains = []
    # for i, day in enumerate(days):
    #     try:
    #         gain = (day - days[i-1]) / days[i-1]
    #         gains.append(gain)
    #     except ZeroDivisionError:
    #         gains.append(0)
    # return gains

    # better 0.13s
    # for i, day in enumerate(days):
    #     yield (day - days[i-1]) / days[i-1]

    # ==========================================================================
    # EXPECTING AN ITERATOR

    # naive = 0.14s
    # gains = []
    # pairs = pairwise(days)
    # for pair in pairs:
    #     gain = (pair[1] - pair[0]) / pair[0]
    #     gains.append(gain)
    # return gains

    # better = 0.05s
    pairs = pairwise(days)
    for pair in pairs:
        yield (pair[1] - pair[0]) / pair[0]


days = open_sp500()
gains = calc_daily_gains(days)


# ==============================================================================
# PART 2
# Find the maximum and minimum values of the gains sequence, and the date on which they occur. (Note that it is possible that these values are attained on more than on date; in that case, the most recent date will suffice.)


def get_dates():
    with open('sp500.csv', 'r') as f:
        reader = csv.DictReader(f)

        for row in reader:
            yield row['Date'].strip()


dates = get_dates()
gains_dates = pairwise(gains, dates)
dates_gains = ((dates, gains) for (gains, dates) in gains_dates)
# print(len(list(dates_gains))) #makes sense that it's 17190. We lost 1 line because it's a header and we lost 1 line because we were calcualting returns on 1+

# NOTE: this is not the most efficient way. Every time I exhaust an iterator, it's the same as looping over a list. So I effectively create and loop over 3 lists in my version of the code.
dates_gains_1, dates_gains_2, dates_gains_3 = itertools.tee(dates_gains, 3)

max_tuple = max(dates_gains_1, key=lambda x: x[1])
min_tuple = min(dates_gains_2, key=lambda x: x[1])

# ==============================================================================
# PART 3
# Transform gains into a sequence growth_streaks of tuples of consecutive positive values in gains. Then determine the length of the longest tuple in growth_streaks and the beginning and ending dates of the streak. (It is possible that the maximum length is attained by more than one tuple in growth_streaks; in that case, the tuple with the most recent beginning and ending dates will suffice.)


def positive_negative(tup):
    gain = tup[1]
    if gain >= 0:
        return 'positive'
    else:
        return 'negative'


pos_neg_groups = itertools.groupby(dates_gains_3, key=positive_negative)

L = []
for key, group in pos_neg_groups:
    # I wonder if this is inefficient?
    group = list(group)
    start_date = group[0][0]
    length = len(group)
    # end date
    start_date_dt = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    end_date_dt = start_date_dt + datetime.timedelta(days=int(length))
    end_date = end_date_dt.strftime('%Y-%m-%d')
    L.append((key, length, start_date, end_date))

# is this another O(N) operation?
L = sorted(L, key=lambda x: x[1], reverse=True)


print(max_tuple)
print(min_tuple)
print(L[0])


# ==============================================================================
"""
CONCLUSIONS:

1. List comprehension is shorter, sometimes harder to read, but has NO IMPACT on execution speed
2. Using generators increases speed massively - in my case 20x for a CSV with 17k rows
3. timeit.timeit(lambda: calc_daily_gains(days), number=10) = super fucking useful

QS:
1. Can I have a list of all operations in python and their complexity?

Yes - here - https://wiki.python.org/moin/TimeComplexity
They don't have tuples in there
In general tuples slightly faster than lists - But you should test on your own computer

# test tuple creation - 12 nsec
python -m timeit "x=(1,2,3,4,5)"
# test list creation - 62 nsec
python -m timeit "x=[1,2,3,4,5]"
# test tuple accesss - 32 nsec
python -m timeit "x=(1,2,3,4,5)" "y=x[3]"
# test list access - 82 nsec
python -m timeit "x=[1,2,3,4,5]" "y=x[3]"

"""


# ==============================================================================
# REAL PYTHON VERSION

# 1 - import data
# they've created a custom subclass of namedtuple class
# so not just a instance of a namedtuple itself - but a subclass of a class
class DataPoint(namedtuple('ADataPoint', ['date', 'value'])):
    __slots__ = ()

    # knowing that they'll have to compare them later they've added these methods
    def __le__(self, other):
        return self.value <= other.value

    def __lt__(self, other):
        return self.value < other.value

    def __ge__(self, other):
        return self.value >= other.value

    def __gt__(self, other):
        return self.value > other.value


def read_prices(csvfile, _strptime=datetime.datetime.strptime):
    # then they read the prices and dates (2 pieces of info we need) into that custom datastructure
    with open(csvfile) as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield DataPoint(  # using yield like I did
                date=_strptime(row['Date'], '%Y-%m-%d').date(),
                value=float(row['Adj Close'])
            )


def consecutive_positives(sequence, zero=0):
    def _consecutives():
        # take the seq > turn into an iterator > keep repeating that iterator
        for i in itertools.repeat(iter(sequence)):
            # for each iterator produce a tuple
            yield tuple(
                # that contains all positives
                itertools.takewhile(
                    lambda p: p > zero,
                    # of another list that also contains only positives, made out of the original iterator
                    itertools.dropwhile(lambda p: p <= zero, i)
                )
            )
    # finally return the length of those tuples
    return itertools.takewhile(lambda t: len(t), _consecutives())


prices = tuple(read_prices('SP500.csv'))

# 2 - calc gains
# I really like how they're accessing elements with names - very readable
# zipping the list with one slightly off - seems an easier solution than defining a custom function, which is what I did


def calc_gains():
    """The choice of storing the data in a tuple is intentional.
    Although you could point gains to an iterator, you will need to iterate over the data twice to find the minimum and maximum values.
    If you use tee() to create two independent iterators, exhausting one iterator to find the maximum will create a copy of all of the data in memory for the second iterator.
    By creating a tuple up front, you do not lose anything in terms of space complexity compared to tee(), and you may even gain a little speed."""
    return tuple(DataPoint(price.date, (price.value/prev_price.value-1)) for prev_price, price in
                 zip(prices, prices[1:]))


gains = calc_gains()

# 3 - calc max and min
zdp = DataPoint(None, 0)
max_gain = functools.reduce(max, itertools.filterfalse(lambda p: p <= zdp, gains))
max_loss = functools.reduce(min, itertools.filterfalse(lambda p: p > zdp, gains))


# 4 - calc longest streak
growth_streaks = consecutive_positives(gains, zero=zdp)
longest_streak = functools.reduce(lambda x, y: x if len(x) > len(y) else y, growth_streaks)

print(f'max gain: {round(max_gain.value*100,2)} %')
print(f'max loss: {round(max_loss.value*100,2)} %')
print('longest growth streak: {num_days} days ({first} to {last})'.format(
    num_days=len(longest_streak),
    first=longest_streak[0].date,
    last=longest_streak[-1].date
))


# ==============================================================================
"""
LEARNINGS FROM RP:

1. using namedtuples to create custom data structures - very interesting!
- memory efficient (don't havee a __dict__ field, which is used to store all of the attributes of an object in python)
- immutable
- can be used as an alternative to classes, if immutability / efficiency is important

2. __slots__ - if defined the class will use this to store attributes instead of __dict__, thus saving memory
- classes with slots are halfway between namedtuples and full blown classes
- take a look below this comment to see what it looks like

http://maurodec.com/blog/classes-namedtuples-slots/


3. I like how they created a custom subclass with comparison methods baked in that look up the value attribute.
I didn't do that and so I had to constantly define how max/min works through indexing

4. I like the nice "named" access namedtuple gives them to their attributes - vs indexing which is less readable

5. reduce function new to me

6. really simple way to shift the list [1:]


Now let's talk efficiency
- they import the data using yield, which is exactly how I did it

"""


# class withSlots(object):
#     __slots__ = ('int1', 'int2', 'int3')
#
#     def __init__(self, int1, int2, int3):
#         self.int1 = int1
#         self.int2 = int2
#         self.int3 = int3
#
#
# c = withSlots(1, 2, 3)
# print(c.int1)

# NOTE: the below is kinda useful to measure time complexity, but not really space complexity
# print('-'*100)
# print('mine')
# print(timeit.timeit(open_sp500, number=100))
# print(timeit.timeit(get_dates, number=100))
# print(timeit.timeit(lambda: calc_daily_gains(days), number=100))
# print('RP')
# print(timeit.timeit(lambda: read_prices('SP500.csv'), number=100))
# print(timeit.timeit(lambda: tuple(read_prices('SP500.csv')), number=100))
# print(timeit.timeit(calc_gains, number=100))

# returns memory for each line of function
print('-'*100)

func = open_sp500
print(f'calcing for.....{func}')
m = memory_usage(func)
print(m)

func = calc_daily_gains
print(f'calcing for.....{func}')
m = memory_usage((func, (days,)))
print(m)

func = read_prices
print(f'calcing for.....{func}')
m = memory_usage((func, ('SP500.csv',)))
print(m)

func = calc_gains
print(f'calcing for.....{func}')
m = memory_usage(func)
print(m)
