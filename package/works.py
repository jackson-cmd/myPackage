"""A works class for bibtex utilities."""
import base64
import bibtexparser
import requests
from bibtexparser.bwriter import BibTexWriter
from IPython.display import display, HTML


class Works:
    """A works class for bibtex utilities."""

    def __init__(self, oaid):
        """A works init for bibtex utilities."""
        self.oaid = oaid
        self.req = requests.get(f"https://api.openalex.org/works/{oaid}")
        self.data = self.req.json()

    @property
    def bibtex(self):
        """A works bibtex."""
        data = self.data
        db = bibtexparser.bibdatabase.BibDatabase
        db.entries = [
            {
                "journal": data["primary_location"]["source"]["host_organization_name"],
                "pages": data["biblio"]["first_page"]
                + "-"
                + data["biblio"]["last_page"],
                "url": data["primary_location"]["landing_page_url"],
                "title": data["title"],
                "year": str(data["publication_year"]),
                "volume": data["biblio"]["volume"],
                "author": data["authorships"][0]["author"]["display_name"],
                "number": data["biblio"]["issue"],
                "doi": data["doi"],
                "DATE_ADDED": data["updated_date"],
                "ID": "kitchin-2015",
                "ENTRYTYPE": "article",
            }
        ]
        db.comments = []
        db.strings = {}
        db.preambles = []
        writer = BibTexWriter()
        with open("bibtex.bib", "w", encoding="utf-8") as bibfile:
            bibfile.write(writer.write(db))
        ans = ""
        with open("bibtex.bib", "r", encoding="utf-8") as lines:
            for line in lines:
                ans += line
        # print(ans)
        return ans

    @property
    def ris(self):
        """A ris bibtex."""
        fields = []
        if self.data["type"] == "journal-article":
            fields += ["TY  - JOUR"]
        else:
            raise Exception("Unsupported type {self.data['type']}")

        for author in self.data["authorships"]:
            fields += [f'AU  - {author["author"]["display_name"]}']

        fields += [f'PY  - {self.data["publication_year"]}']
        fields += [f'TI  - {self.data["title"]}']
        fields += [f'JO  - {self.data["host_venue"]["display_name"]}']
        fields += [f'VL  - {self.data["biblio"]["volume"]}']

        if self.data["biblio"]["issue"]:
            fields += [f'IS  - {self.data["biblio"]["issue"]}']

        fields += [f'SP  - {self.data["biblio"]["first_page"]}']
        fields += [f'EP  - {self.data["biblio"]["last_page"]}']
        fields += [f'DO  - {self.data["doi"]}']
        fields += ["ER  -"]

        ris = "\n".join(fields)
        ris64 = base64.b64encode(ris.encode("utf-8")).decode("utf8")
        uri = f'<pre>{ris}</pre><br><a href="data:text/plain;base64,\
        {ris64}" download="ris">Download RIS</a>'

        display(HTML(uri))
        return ris


# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="Add some integers.")
#     parser.add_argument("-r", "--ris")
#     parser.add_argument("-b", "--bibtex")
#     # print(sys.argv)
#     args = parser.parse_args()
#     if args.ris:
#         works = Works(args.ris)
#         print(str(works.ris))
#     elif args.bibtex:
#         works = Works(args.bibtex)
#         print(works.bibtex)
# w = Works(args)
# print("Bibtex enty is below")
# w.bibtex
# print("Ris data is below")
# w.ris
