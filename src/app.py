from collections import OrderedDict
from lxml import html
import requests
import genanki
import random
import re

# read main body of the site
page = requests.get('https://www.fs.blog/mental-models/')
tree = html.fromstring(page.content)
content = tree.xpath('//div[@class="rte"]')[0].getchildren()

def parse_groups(content):
    groups = OrderedDict()
    group = None
    for elem in content:
        if elem.tag == 'h2':
            group = elem.xpath('./strong/text()')[0]
            groups[group] = []
        else:
            if group:
                groups[group].append(elem)
    return groups

def parse_models(groups):
    models = OrderedDict()
    model = None
    for group in list(groups.keys())[2:]:
        models[group] = []
        elems = groups[group]
        for elem in elems:
            if elem.xpath('.//strong'):
                if re.search('^\s*\d+', elem.xpath('.//strong')[0].text_content()):
                    model = html.tostring(elem.xpath('.//strong')[0])
                    models[group].append([model])
            else:
                models[group][-1].append(html.tostring(elem))
    return models

grps = parse_groups(content)
mdls = parse_models(grps)
                
anki_model = genanki.Model(
    random.randrange(1 << 30, 1 << 31),
    'Simple Model',
    fields=[
        { 'name': 'Question' },
        { 'name': 'Answer' }
    ],
    templates=[
        {
            'name': 'Mental Model',
            'qfmt': '{{Question}}',
            'afmt': '{{Answer}}'
        }
    ]
)

notes = []

for group in mdls:
    for model in mdls[group]:
        question = "<h2>" + re.sub('\s*\d+\.\s*', '', model[0].decode()) + "</h2>"
        answer = "".join([m.decode() for m in model[1:]])
        notes.append(
            genanki.Note(
                model=anki_model,
                fields=[question, answer]
            )
        )

deck = genanki.Deck(
    random.randrange(1 << 30, 1 << 31),
    'Farnham Street Mental Models'
)

for note in notes:
    deck.add_note(note)
    
genanki.Package(deck).write_to_file('target/farnham_street_mental_models.apkg')

