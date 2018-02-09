# This script takes all our different bibliography IDs and tries to convert
# them.

import arxiv2bib
import doi2bib.crossref as doi2bib
import yaml

pubs = yaml.load(open("_data/publications.yml"))

# First do our DOIs

bibs = []

# What we want:
#
#   title: ''
#   authors: []
#   year: int
#   month:
#   doi:
#   url:
#   journal:

m = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul",
     "Aug", "Sep", "Oct", "Nov", "Dec"]

def convert_doientry(entry):
    title = entry['title']
    if isinstance(title, list):
        title = title[0]
    authors = ['{family}, {given}'.format(**_) for _ in entry['author']]
    if 'published-print' in entry:
        dp = entry['published-print']['date-parts'][0]
    elif 'published-online' in entry:
        dp = entry['published-online']['date-parts'][0]
    year, month, *a = dp
    doi = entry['DOI']
    url = entry['URL']
    journal = entry['container-title']
    if isinstance(journal, list):
        journal = journal[0]
    yearmonth = '%04i-%02i' % (year, month)
    return {'title': title, 'authors': authors, 'year': year, 'month': month,
            'doi': doi, 'url': url, 'journal': journal, 'yearmonth': yearmonth}

for ref in pubs['dois']:
    found, val = doi2bib.get_json(ref)
    if found:
        bibs.append(convert_doientry(val['message']))

arxivs = arxiv2bib.arxiv2bib(pubs['arxiv'])
for ref in arxivs:
    month = m.index(ref.month) + 1
    yearmonth = '%04i-%02i' % (int(ref.year), month)
    bibs.append( {'title': ref.title, 'authors': ref.authors,
                  'year': ref.year,
                  'month': month,
                  'yearmonth': yearmonth,
                  'url': ref.url,
                  'journal': "arXiv"} )

with open("_data/citations.yml", "w") as f:
    yaml.dump(bibs, f, default_flow_style=False)
