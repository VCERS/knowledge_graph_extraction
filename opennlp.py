#!/usr/bin/python3

from os.path import join, exists
import jpype
import jpype.imports
from jpype.types import *
from nltk.tree import Tree
from wget import download

class OpenNLP(object):
  def __init__(self,):
    if not exists('en-ner-date.bin'): download('https://opennlp.sourceforge.net/models-1.5/en-ner-date.bin', out = '.')
    if not exists('en-ner-location.bin'): download('https://opennlp.sourceforge.net/models-1.5/en-ner-location.bin', out = '.')
    if not exists('en-ner-money.bin'): download('https://opennlp.sourceforge.net/models-1.5/en-ner-money.bin', out = '.')
    if not exists('en-ner-organization.bin'): download('https://opennlp.sourceforge.net/models-1.5/en-ner-organization.bin', out = '.')
    if not exists('en-ner-percentage.bin'): download('https://opennlp.sourceforge.net/models-1.5/en-ner-percentage.bin', out = '.')
    if not exists('en-ner-person.bin'): download('https://opennlp.sourceforge.net/models-1.5/en-ner-person.bin', out = '.')
    if not exists('en-ner-time.bin'): download('https://opennlp.sourceforge.net/models-1.5/en-ner-time.bin', out = '.')
    if not exists('en-pos-maxent.bin'): download('https://opennlp.sourceforge.net/models-1.5/en-pos-maxent.bin', out = '.')
    if not exists('en-parser-chunking.bin'): download('https://opennlp.sourceforge.net/models-1.5/en-parser-chunking.bin', out = '.')
    '''
    if not exists('langdetect-183.bin'): download('https://dlcdn.apache.org/opennlp/models/langdetect/1.8.3/langdetect-183.bin', out = '.')
    if not exists('SentenceDetector'): download('https://dlcdn.apache.org/opennlp/models/ud-models-1.0/opennlp-en-ud-ewt-sentence-1.0-1.9.3.bin', out = '.')
    if not exists('POSTagger'): download('https://dlcdn.apache.org/opennlp/models/ud-models-1.0/opennlp-en-ud-ewt-pos-1.0-1.9.3.bin', out = '.')
    if not exists('TokenizerME'): download('https://dlcdn.apache.org/opennlp/models/ud-models-1.0/opennlp-en-ud-ewt-tokens-1.0-1.9.3.bin', out = '.')
    if not exists('Parser'): download('https://opennlp.sourceforge.net/models-1.5/en-parser-chunking.bin')
    '''
    jpype.startJVM(classpath = ['/usr/share/java/org.jpype-1.3.0.jar','/usr/share/java/opennlp-tools.jar'])
    self.FileInputStream = jpype.JClass('java.io.FileInputStream')
    self.TokenNameFinderModel = jpype.JClass('opennlp.tools.namefind.TokenNameFinderModel')
    self.NameFinderME = jpype.JClass('opennlp.tools.namefind.NameFinderME')
    self.POSModel = jpype.JClass('opennlp.tools.postag.POSModel')
    self.POSTaggerME = jpype.JClass('opennlp.tools.postag.POSTaggerME')
    self.ParserModel = jpype.JClass('opennlp.tools.parser.ParserModel')
    self.ParserFactory = jpype.JPackage('opennlp.tools.parser').ParserFactory
    self.Span = jpype.JClass('opennlp.tools.util.Span')
    self.tasks = {
      'LanguageDetector': 'langdetect-183.bin',
      'SentenceDetector': 'opennlp-en-ud-ewt-sentence-1.0-1.9.3.bin',
      'POSTagger': 'opennlp-en-ud-ewt-pos-1.0-1.9.3.bin',
      'TokenizerME': 'opennlp-en-ud-ewt-tokens-1.0-1.9.3.bin',
      'Parser': 'en-parser-chunking.bin',
    }
  def ner(self, text):
    models = {
      'date': self.NameFinderME(self.TokenNameFinderModel(self.FileInputStream('en-ner-date.bin'))),
      'location': self.NameFinderME(self.TokenNameFinderModel(self.FileInputStream('en-ner-location.bin'))),
      'money': self.NameFinderME(self.TokenNameFinderModel(self.FileInputStream('en-ner-money.bin'))),
      'organization': self.NameFinderME(self.TokenNameFinderModel(self.FileInputStream('en-ner-organization.bin'))),
      'percentage': self.NameFinderME(self.TokenNameFinderModel(self.FileInputStream('en-ner-percentage.bin'))),
      'person': self.NameFinderME(self.TokenNameFinderModel(self.FileInputStream('en-ner-person.bin'))),
      'time': self.NameFinderME(self.TokenNameFinderModel(self.FileInputStream('en-ner-time.bin'))),
    }
    sentence = JArray(JString,1)(text.split(' '))
    entities = list()
    for name_type, finder in models.items():
      names = finder.find(sentence)
      for name in names:
        entities.append({
          'entity': str(sentence[name.getStart()]),
          'type': str(name.getType()),
          'start': int(name.getStart()),
          'end': int(name.getEnd())
        })
    return entities
  def pos(self, text):
    tagger = self.POSTaggerME(self.POSModel(self.FileInputStream('en-pos-maxent.bin')))
    sentence = JArray(JString,1)(text.split(' '))
    tags = [str(tag) for tag in tagger.tag(sentence)]
    return tags
  def parse(self, text):
    parser = self.ParserFactory.create(self.ParserModel(self.FileInputStream('en-parser-chunking.bin')))
    sentence = JArray(JString,1)(text.split(' '))
    spans = JArray(self.Span,1)
    for i in range(sentence.length):
      spans[i] = self.Span(i, i + 1)
    results = Parser.parse(sentence, spans)
    tree = Tree.fromstring(str(results.toString()))
    return tree
  '''
  def call(self, text):
    try:
      self.process.read_nonblocking(2048, 0)
    except:
      pass
    self.process.sendline(text)
    self.process.waitnoecho()
    timeout = 5 + len(text) / 20.0
    self.process.expect('\r\n', timeout)
    results = self.process.before.decode()
    if self.task == 'POSTagger':
      parts = list()
      for token_with_part in results.split(' '):
        pos = token_with_part.rfind('_')
        content, part = token_with_part[:pos], token_with_part[pos+1:]
        parts.append((content, part))
      return parts
    elif self.task == 'TokenizerME':
      tokens = results.split(' ')
      return tokens
    elif self.task == 'Parser':
      tree = Tree.fromstring(results)
      return tree
    return results
  '''

if __name__ == "__main__":
  opennlp = OpenNLP()
  res = opennlp.ner('Figure 5. Kinetic characteristic tests of chemical reaction between Li1–xCoO2(x= 0, 0.3, 0.5) and typical sulfide SEs. (a) DSC curves of the Li1–xCoO2+ Li6PS5Cl mixed powder at different heating rates (3, 5, 7, 15, 20 °C/min).')
  print(res)
  '''
  res = opennlp.call('Figure 5. Kinetic characteristic tests of chemical reaction between Li1–xCoO2(x= 0, 0.3, 0.5) and typical sulfide SEs. (a) DSC curves of the Li1–xCoO2+ Li6PS5Cl mixed powder at different heating rates (3, 5, 7, 15, 20 °C/min).')
  print(res)
  '''
  res = opennlp.pos('Figure 5. Kinetic characteristic tests of chemical reaction between Li1–xCoO2(x= 0, 0.3, 0.5) and typical sulfide SEs. (a) DSC curves of the Li1–xCoO2+ Li6PS5Cl mixed powder at different heating rates (3, 5, 7, 15, 20 °C/min).')
  print(res)
  res = opennlp.parse('Figure 5. Kinetic characteristic tests of chemical reaction between Li1–xCoO2(x= 0, 0.3, 0.5) and typical sulfide SEs. (a) DSC curves of the Li1–xCoO2+ Li6PS5Cl mixed powder at different heating rates (3, 5, 7, 15, 20 °C/min).')
  print(res)
