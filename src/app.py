from lxml import html
import requests
import itertools

page = requests.get('https://www.fs.blog/mental-models/')
tree = html.fromstring(page.content)

content = tree.xpath('//div[@class="rte"]')[0].getchildren()

def group_by_h2():
    h2 = {'current': None}
    def grouper(elem):
        if elem.tag == 'h2':
            h2['current'] = elem.xpath('./strong/text()')
        return h2['current']
    return grouper
            
groups = list(itertools.groupby(content, key=group_by_h2()))[3:]

models = []

for group in groups:
    group_name = group[0][0]
    print(group_name)
    elems = list(group[1])
    print(elems)
    model_name = None
    for elem in elems:
        print(elem.xpath('./strong'))
    

