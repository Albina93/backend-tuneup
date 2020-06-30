#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tuneup assignment

Use the timeit and cProfile libraries to find bad code.
"""

__author__ = "Group session and Albina Tileubergen-Thomas"

import cProfile
import pstats
import functools
import timeit
from collections import Counter


def profile(func):
    """A cProfile decorator function that can be used to
    measure performance.
    """
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        profile = cProfile.Profile()
        profile.enable()   # starts timer
        value = func(*args, **kwargs)   # call the original function
        profile.disable()  # ends timer

        get_stats_obj = pstats.Stats(profile).strip_dirs(
        ).sort_stats('cumulative').print_stats(10)
        return value
    return wrapper_timer


def read_movies(src):
    """Returns a list of movie titles."""
    print(f'Reading file: {src}')
    with open(src, 'r') as f:
        return f.read().splitlines()


def is_duplicate(title, movies):
    """Returns True if title is within movies list."""
    for movie in movies:
        if movie == title:
            return True
    return False


@profile
def find_duplicate_movies(src):
    """Returns a list of duplicate movies from a src list."""
    movies = read_movies(src)

    c = Counter(movies)
    duplicates = []
    for k, v in c.items():
        if v > 1:
            duplicates.append(k)
    # while movies:
    #     movie = movies.pop()
    #     if is_duplicate(movie, movies):
    #         duplicates.append(movie)
    return duplicates


def timeit_helper():
    """Part A: Obtain some profiling measurements using timeit."""
    t = timeit.Timer(
        stmt="find_duplicate_movies('movies.txt')",
        setup="from __main__ import find_duplicate_movies"
    )
    runs_per_repeat = 3
    num_of_repeat = 5  # each repeat will run per repeat 3 times
    result = t.repeat(repeat=num_of_repeat, number=runs_per_repeat)
    # print(result)
    best_time = min(result) / runs_per_repeat
    print(f"The best run time per function was {best_time:.2f}")


def main():
    """Computes a list of duplicate movie entries."""

    # timeit_helper()
    result = find_duplicate_movies('movies.txt')
    print(f'Found {len(result)} duplicate movies:')
    print('\n'.join(result))


if __name__ == '__main__':
    main()
