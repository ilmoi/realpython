import csv
import os
from collections import namedtuple
import itertools
import functools

os.chdir('/Users/ilja/Dropbox/realpython/itertools_tut')


class Event(namedtuple('Event', ['stroke', 'name', 'time'])):
    __slots__ = ()

    def __lt__(self, other):
        return self.time < other.time


def median(L):
    L.sort()  # O(nlogn)
    return L[len(L)//2]  # length = O(1), getting item also O(1)


def open_swimmers():
    with open('swimmers.csv') as f:
        reader = csv.DictReader(f)

        for row in reader:
            yield Event(
                row['Stroke'],
                row['Name'],
                median([row['Time1'], row['Time2'], row['Time3']])
            )


def sort_and_group(iterable, key=None):
    iterable = sorted(iterable, key=key)  # O(nlogn)
    return itertools.groupby(iterable, key=key)


def grouper(inputs, n, fillvalue=None):
    iters = [iter(inputs)] * n
    return itertools.zip_longest(*iters, fillvalue=fillvalue)


swimmers = tuple(open_swimmers())  # O(n) - kills the point of the generator, but needed for sorted

# first we group by stroke. this needs to be the high level grouping because later we will be looking for best girls in each stroke
groups = sort_and_group(swimmers, key=lambda s: s.stroke)
for stroke, events in groups:

    # next we group by name. this is needed in oredr for us to find the best time for each girl
    events_by_name = sort_and_group(events, key=lambda e: e.name)
    best_times = (min(event) for _, event in events_by_name)  # __lt__

    # once we have the best time we can sort the girls by best times in each stroke
    sorted_by_time = sorted(best_times, key=lambda event: event.time)

    # finally we build the teams using the grouper method stolen from the recipes section here -> https://docs.python.org/3.6/library/itertools.html#itertools-recipes
    teams = zip(('A', 'B'), itertools.islice(grouper(sorted_by_time, 4), 2))
    for team in teams:
        print(team[0], [x.name for x in team[1]])
