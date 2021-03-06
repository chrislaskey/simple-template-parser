#!/usr/bin/env python


import re


class TemplateParser:

    def __init__(self):
        self.keyword_parsers = {}
    
    def parse(self, template):
        match = self.keyword_finder.find(template)

        if not match:
            return template

        head = template[0:match['start']]
        tail = template[match['end']:]

        keyword_parser = self.get_keyword_parser(match)
        result = keyword_parser.parse(match, tail)

        return head + result.value + self.parse(result.remaining)

    def set_keyword_finder(self, finder):
        self.keyword_finder = finder

    def add_keyword_parser(self, key, parser):
        self.keyword_parsers[key] = parser

    def get_keyword_parser(self, match):
        keyword = match['keyword']
        if keyword not in self.keyword_parsers:
            keyword = 'default'
        parser = self.keyword_parsers[keyword]()
        parser.set_keyword_finder(self.keyword_finder)
        parser.set_template_parser(self)
        return parser


class KeywordFinder:

    pattern = re.compile('<\* *(.*?) *\*>')

    def find(self, string):
        match = self.pattern.search(string)
        if not match:
            return None

        match_groups = match.groups()
        match_string = match_groups[0]
        match_keyword = self.keyword(match_string)

        return {
            'start': match.start(),
            'end': match.end(),
            'string': match_string,
            'keyword': match_keyword
        }

    def keyword(self, match_string):
        stripped = match_string.strip()
        tokenized = stripped.split(' ')
        first_word = tokenized[0]
        keyword = first_word.lower()
        return keyword


class KeywordParser:

    def set_keyword_finder(self, finder):
        self.keyword_finder = finder

    def set_template_parser(self, parser):
        self.template_parser = parser

    def parse(self, match, tail):
        self.value = ''
        self.remaining = tail
        return self


class KeywordParserVariable(KeywordParser):

    def parse(self, match, tail):
        self.value = 'tiger'
        self.remaining = tail
        return self


class KeywordParserEach(KeywordParser):

    def parse(self, match, tail):
        self.split_remaining_content(tail)
        self.value = ''

        dummy_list = ['lion', 'bear', 'oh my']
        for item in dummy_list:
            self.value = self.value + self.template_parser.parse(self.block)

        return self

    def split_remaining_content(self, tail):
        '''
        Split remaining content into two pieces:
            1. self.block     (entire each block)
            2. self.remaining (after each block)
        '''
        block_end = self.get_end_of_each_block(tail)

        self.block = tail[:block_end]
        self.remaining = tail[block_end:]

    def get_end_of_each_block(self, content):
        '''
        Find the matching ENDEACH location.
        Uses count to keep track of nested EACH blocks.
        Raises exception if template is malformed and no ENDEACH is found.
        '''
        count = 1
        index = 0
        match = self.keyword_finder.find(content)

        while match:
            if match['keyword'] == 'each':
                count = count + 1
            elif match['keyword'] == 'endeach':
                count = count - 1
                if count == 0:
                    index = index + match['end']
                    return index

            index = index + match['end']
            content = content[match['end']:]
            match = self.keyword_finder.find(content)

        raise error('No matching ENDEACH found')


class KeywordParserEndeach(KeywordParser):

    def parse(self, match, tail):
        self.value = ''
        self.remaining = tail
        return self


with open('example/template.panoramatemplate', 'r') as file:
    template = file.read()

with open('example/data.json', 'r') as file:
    variables = file.read()

with open('example/output.html', 'r') as file:
    expected = file.read()

parser = TemplateParser()

parser.set_keyword_finder(KeywordFinder())
parser.add_keyword_parser('each', KeywordParserEach)
parser.add_keyword_parser('endeach', KeywordParserEndeach)
parser.add_keyword_parser('default', KeywordParserVariable)

print(parser.parse(template))
