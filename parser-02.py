#!/usr/bin/env python


import re

pattern = re.compile('<\* *(.*?) *\*>')

def find(string):
    match = pattern.search(string)
    if not match:
        return None

    match_groups = match.groups()
    match_string = match_groups[0]
    match_keyword = keyword(match_string)

    return {
        'start': match.start(),
        'end': match.end(),
        'string': match_string,
        'keyword': match_keyword
    }

def keyword(match_string):
    stripped = match_string.strip()
    tokenized = stripped.split(' ')
    first_word = tokenized[0]
    keyword = first_word.lower()
    return keyword

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
    result = find(input)
    if expected == None:
        assert result == None
    else:
        assert result['string'] == expected
