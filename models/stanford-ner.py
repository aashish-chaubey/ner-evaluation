import spacy
from models.nltk import word_tokenize
from nltk.tag.stanford import StanfordNERTagger

jar = '../assets/stanford-ner/stanford-ner.jar'
model = '../assets/stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz'

sp_sm = spacy.load('en_core_web_sm')

example_document = '''Deepak Jasani, Head of retail research, HDFC Securities, said: “Investors will look to the European Central Bank later Thursday for reassurance that surging prices are just transitory, and not about to spiral out of control. In addition to the ECB policy meeting, investors are awaiting a report later Thursday on US economic growth, which is likely to show a cooling recovery, as well as weekly jobs data.”. 9189189822. New Delhi, India'''

ner_tagger = StanfordNERTagger(model, jar)

words = word_tokenize(example_document)

words = ner_tagger.tag(words)

def func(items):
    entities = ['PERSON', 'LOCATION', 'ORGANIZATION']
    if items[1] in entities:
        return True
    else:
        return False

new_list = filter(func, words)
print(list(new_list))

