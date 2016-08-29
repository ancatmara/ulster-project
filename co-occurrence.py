import json
import os
import re
from collections import Counter
from collections import defaultdict
from pprint import pprint as pp

with open('characterlist.txt', 'r', encoding='utf-8') as cl:
    characters = set([line.lower().strip() for line in cl])

charDict = {}
for char in characters:
    charDict[char] = re.sub(r'\s', r'_', char)

path = 'C:\\Users\\ahten_000\\Dropbox\\Библиотека\\Вышка\\OldIrish\\texts\\ulster\\processed\\lemmatized'
files = [name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name))]
terms = []
for file in files:
    with open(os.path.join(path, file), 'r', encoding='utf-8') as f:
        text = f.read()
        for char in characters:
            if char in text:
                text = re.sub(char, charDict[char], text)
        terms += text.split()


class Matcher():
    def __init__(self, phrases):
        phrase_pattern = "|".join("(?:{})".format(phrase) for phrase in phrases)
        gap_pattern = r"\W+(?:\w+\W+){0,10}?"
        full_pattern = "({0}){1}({0})".format(phrase_pattern, gap_pattern)

        self.regex = re.compile(full_pattern)

    def match(self, doc):
        return self.regex.findall(doc)


matcher = Matcher(charDict.values())
com = defaultdict(lambda: defaultdict(int))

matches = matcher.match(' '.join(terms))
filteredMatches = []
for el in matches:
    el = [name for name in el if len(name) != 0]
    el = [name for name in el if el[0] != el[1]]
    filteredMatches.append(tuple(set(el)))

counts = Counter(filteredMatches)

for k, v in counts.items():
    if len(k) != 0:
        com[k[0]][k[1]] += v

with open('pair_counts.json', 'w', encoding='utf-8') as p:
    json.dump(com, p, sort_keys=True, ensure_ascii=False)

with open('nodes.json', 'w', encoding='utf-8') as n, open('links.json', 'w', encoding='utf-8') as l:
    for k, v in com.items():
        for el in v:
            n.write('{"name":"%s","group":1},\n' % (k))
            l.write('{"source":%s,"target":%s,"value":%s},\n' % (k, el, v[el]))
