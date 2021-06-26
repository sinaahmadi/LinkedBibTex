"""
    This script retrieves bibliographic data from DBLP according to the citaiton keys used with a .tex file (bibtex or natbib).
    The references.bib is updated whenever a new entry is cited.

    Sina Ahmadi
    June 2021
"""
import sys
import re
import os
import argparse
import bibtex_dblp.dblp_api
import bibtex_dblp.database
from bibtex_dblp.dblp_api import BibFormat


def extract_cite_key(text):
    """
    Given a text, return all reference keys in citation commands.
    Citation keys in bibtex and natbib are the followings:
            ["cite", "citet", "citep", "citet", "citet*", "citep*", "citealt", "citealt*", "citealp", "citealp*", "citeauthor", "citeauthor*", "citeyear", "citeyearpar"]
    Each citation phrase can be accompanied by more details such as page number in brackets, i.e. [].
    """
    cite_regex = re.compile(r"\\cite(?:p|alp|t|author|alt|year|yearpar)?\*?(\[.*\])*{(.*?)}")
    for nested, cites in cite_regex.findall(text):
        for cite in extract_cite_key(nested):
            yield cite
        for cite in cites.split(","):
            yield cite

if __name__ == '__main__':
    
    # with open("references.bib", "r") as f:
    #     f.read()
    parser = argparse.ArgumentParser()
    parser.add_argument('tex_filename', help='Name of the .tex file')
    # parser.add_argument('ref_filename', nargs='?', help='Name of the bibliographic file (optional)')

    args = parser.parse_args()
    
    with open(args.tex_filename, "r") as f: 
        text = f.read()

    if len(re.findall(r"\\bibliography{(.*)}", text)[0].strip()) != "":
        reference_file_name = re.findall(r"\\bibliography{(.*)}", text)[0].strip() + ".bib"
    else:
        reference_file_name = "references.bib"

    citation_keys = list(set([i.strip() for i in extract_cite_key(text)]))

    # reading `bibkeys` file containing bibliographic entries which are previously imported
    if os.path.exists(".bibkeys"):
        with open(".bibkeys", "r") as f:
            bibkeys = f.read().split("\n")
    else:
        bibkeys = list()

    bibtex_file = dict()
    for cite_key in citation_keys:
        print(cite_key)
        # only run queries for new keys which do not exist in the `bibkeys` file
        if cite_key not in bibkeys and cite_key not in bibtex_file:
            try:
                bibtex_file[cite_key] = bibtex_dblp.dblp_api.get_bibtex(cite_key, bib_format=BibFormat.standard).replace("{DBLP:", "{")
            except:
                continue

    # save keys in a hidden file if bib file is to be updated.
    if len(bibtex_file):
        print("saving")
        with open(".bibkeys", "a") as f:
            f.write("\n".join(list(bibtex_file.keys())) + "\n")

        with open(reference_file_name, "a") as f:
            f.write("\n".join(list(bibtex_file.values())) + "\n")
