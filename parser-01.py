#!/usr/bin/env python


import re


pattern = re.compile('<\* *(.*?) *\*>')

def find(string):
    match = pattern.search(string)
    if not match:
        return None
    
    match_groups = match.groups()
    match_string = match_groups[0]
    return match_string

find_tests = [
    ('no matches', None),
    ('<* *>', ''),
    ('<* basic-match *>', 'basic-match'),
    ('<* matches multiple words *>', 'matches multiple words'),
    ('<*no-spaces*>', 'no-spaces'),
    ('<*  extra-spaces   *>', 'extra-spaces'),
    ('<* one *> two <* three *>', 'one'),
]

for input, expected in find_tests:
    assert find(input) == expected
