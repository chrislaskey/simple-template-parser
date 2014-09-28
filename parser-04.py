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

def parse(template):
    match = find(template)

    if not match:
        return template

    head = template[0:match['start']]
    tail = template[match['end']:]

    parser = get_keyword_parser(match)
    result = parser.parse(match, tail)

    return head + result.value + parse(result.remaining)

def get_keyword_parser(match):
    if match['keyword'] == 'each':
        pass
    else:
        return KeywordParserVariable()

class KeywordParserVariable:

    def parse(self, match, tail):
        self.value = 'tiger'
        self.remaining = tail
        return self

test = 'This <* myvar *> is a <* myvar *> test sentence'
expected = 'This tiger is a tiger test sentence'

assert parse(test) == expected
