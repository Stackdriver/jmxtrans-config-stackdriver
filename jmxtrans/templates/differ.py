#!/usr/bin/env python

from collections import OrderedDict
import json
import sys

def diff(obj1, obj2):
  """Prints a simple human-readable difference between two Python objects."""
  result = []
  diffAny(obj1, obj2, result)
  return '\n'.join(result)

def diffAny(obj1, obj2, result):
    """Recursively calculate the difference between 'obj1' and 'obj2' and
    append human-readable descriptions of those differences to the 'result'
    array.
"""
    if (type(obj1) is not type(obj2)):
        result.append("Types differ: {0} vs {1} ({2} vs {3})".format(
            str(type(obj1)), str(type(obj2)), obj1, obj2))
        return

    t = type(obj1)

    if (t is list):
        diffList(obj1, obj2, result)
        return

    if (t is dict or t is OrderedDict):
        diffDict(obj1, obj2, result)
        return

    if (obj1 != obj2):
        result.append("Values differ: {0} vs {1}".format(obj1, obj2))


def diffList(list1, list2, result):
    """Helper method that handles lists."""
    if (len(list1) != len(list2)):
        result.append("List lengths differ: {0} vs {1}".format(
          len(list1), len(list2)))

    # Compare the corresponding items in the lists (stop at the end of the
    # shorter list if one is shorter than the other)
    for pair in zip(list1, list2):
        diffAny(pair[0], pair[1], result)


def diffDict(dict1, dict2, result):
    """Helper method that handles dictionaries."""
    if (len(dict1) != len(dict2)):
        result.append("Dict lengths differ: {0} vs {1}".format(
          len(dict1), len(dict2)))
    for (key1, value1) in dict1.items():
        if key1 in dict2:
            value2 = dict2[key1]
            diffAny(value1, value2, result)

    diffDictHelper("only in dict1", dict1, dict2, result)
    diffDictHelper("only in dict2", dict2, dict1, result)

def diffDictHelper(text, dict1, dict2, result):
    """Another helper method that describes keys present in dict1 that are
    absent from dict2."""
    for key1 in dict1:
        if key1 not in dict2:
            result.append("{0}: {1}".format(text, key1))
