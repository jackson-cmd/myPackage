import bibtexparser
import time
import requests
from bibtexparser.bwriter import BibTexWriter
import sys
import base64
import matplotlib.pyplot as plt
from IPython.display import HTML
from IPython.core.pylabtools import print_figure
from IPython.display import display, HTML
import sys

class Works:
    def __init__(self, oaid):
        self.oaid = oaid
        self.req = requests.get(f'https://api.openalex.org/works/{oaid}')
        self.data = self.req.json()
        
    @property
    def bibtex(self):
        d = self.data
        db = bibtexparser.bibdatabase.BibDatabase
        db.entries = [
            {'journal': d["primary_location"]["source"]['host_organization_name'],
             'pages': d['biblio']['first_page'] + '-' + d['biblio']['last_page'],
             'url':d["primary_location"]['landing_page_url'],
             'title': d['title'],
             'year': str(d['publication_year']),
             'volume': d['biblio']['volume'],
             'author': d['authorships'][0]['author']['display_name'],
             'number':d['biblio']['issue'],
             'doi':d['doi'],
             'DATE_ADDED':d['updated_date'],
             'ID':"kitchin-2015",
             'ENTRYTYPE':'article',
            }]
        writer = BibTexWriter()
        writer.write(db)
        sys.stdout.write(writer.write(db))
     
    @property
    def ris(self):
        fields = []
        if self.data['type'] == 'journal-article':
            fields += ['TY  - JOUR']
        else:
            raise Exception("Unsupported type {self.data['type']}")
        
        for author in self.data['authorships']:
            fields += [f'AU  - {author["author"]["display_name"]}']
            
        fields += [f'PY  - {self.data["publication_year"]}']
        fields += [f'TI  - {self.data["title"]}']
        fields += [f'JO  - {self.data["host_venue"]["display_name"]}']
        fields += [f'VL  - {self.data["biblio"]["volume"]}']
        
        if self.data['biblio']['issue']:
            fields += [f'IS  - {self.data["biblio"]["issue"]}']
        
        
        fields += [f'SP  - {self.data["biblio"]["first_page"]}']
        fields += [f'EP  - {self.data["biblio"]["last_page"]}']
        fields += [f'DO  - {self.data["doi"]}']
        fields += ['ER  -']
                
        ris = '\n'.join(fields)
        ris64 = base64.b64encode(ris.encode('utf-8')).decode('utf8')
        uri = f'<pre>{ris}<pre><br><a href="data:text/plain;base64,{ris64}" download="ris">Download RIS</a>'
        display(HTML(uri))
        return HTML(uri)
    
if __name__ == "__main__":
    w = Works(sys.argv[1])
    print("Bibtex enty is below")
    w.bibtex
    print("Ris data is below")
    display(w.ris.data)