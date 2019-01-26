import csv
import StringIO
import spacy
import WikipediaExtractor
import write_to_file
import sys
import os

if(os.path.isfile('result.ttl')):
    os.unlink('result.ttl')

nlp = spacy.load('ner_model/')

if (sys.argv[1] == '-f'):
    with open(sys.argv[2]) as file:
        results = file.read()
        data = list(csv.DictReader(StringIO.StringIO(results), delimiter='\t'))

for entities in data:

    fact_id = entities['FactID']
    fact_statement = entities['Fact_Statement']

    text = unicode(fact_statement, 'latin-1')
    doc = nlp(text)
    ents = [e.text for e in doc.ents]
    print(ents)

    if e.label_ == "SUB" or e.label_ == "OBJ":
        dic = WikipediaExtractor.get_term_dict(e.text, ents)
        truth_value = WikipediaExtractor.check_existence(dic)
        write_to_file.write_to_file(fact_id, truth_value)
        print truth_value
