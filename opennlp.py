#!/usr/bin/python3

from os.path import join
from wget import download

class OpenNLP(object):
  def __init__(self, task = 'part of speech'):
    tasks = {
      'language detector': 'https://www.apache.org/dyn/closer.cgi/opennlp/models/langdetect/1.8.3/langdetect-183.bin',
      'sentence detector': 'https://www.apache.org/dyn/closer.cgi/opennlp/models/ud-models-1.0/opennlp-en-ud-ewt-sentence-1.0-1.9.3.bin',
      'part of speech': 'https://www.apache.org/dyn/closer.cgi/opennlp/models/ud-models-1.0/opennlp-en-ud-ewt-pos-1.0-1.9.3.bin',
      'tokens': 'https://www.apache.org/dyn/closer.cgi/opennlp/models/ud-models-1.0/opennlp-en-ud-ewt-tokens-1.0-1.9.3.bin'
    }
    opennlp = join('bin','opennlp')

