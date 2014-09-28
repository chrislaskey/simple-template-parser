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
        return KeywordParserEach()
    elif match['keyword'] == 'endeach':
        return KeywordParserEndeach()
    else:
        return KeywordParserVariable()

class KeywordParserVariable:

    def parse(self, match, tail):
        self.value = 'tiger'
        self.remaining = tail
        return self

class KeywordParserEndeach:

    def parse(self, match, tail):
        self.value = ''
        self.remaining = tail
        return self

class KeywordParserEach:

    def parse(self, match, tail):

        endeach = self.get_end_of_loop_index(tail)
        each_block = tail[:endeach]

        self.remaining = tail[endeach:]
        self.value = ''

        dummy_list = ['lion', 'bear', 'oh my']
        for item in dummy_list:
            self.value = self.value + parse(each_block)

        return self

    def get_end_of_loop_index(self, tail):
        count = 1
        index = 0
        match = find(tail)

        while match:
            if match['keyword'] == 'each':
                count = count + 1
            elif match['keyword'] == 'endeach':
                count = count - 1
                if count == 0:
                    index = index + match['end']
                    return index

            index = index + match['end']
            tail = tail[match['end']:]
            match = find(tail)

        raise error('No matching ENDEACH found')


with open('example/template.panoramatemplate', 'r') as file:
    template = file.read()

with open('example/data.json', 'r') as file:
    variables = file.read()

with open('example/output.html', 'r') as file:
    expected = file.read()

parse(template)
