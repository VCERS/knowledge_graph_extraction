#!/usr/bin/python3

from os.path import join
from urllib.parse import urlparse
from wget import download

class OpenNLP(object):
  def __init__(self, task = 'part of speech'):
    self.tasks = {
      'language detector': 'https://www.apache.org/dyn/closer.cgi/opennlp/models/langdetect/1.8.3/langdetect-183.bin',
      'sentence detector': 'https://www.apache.org/dyn/closer.cgi/opennlp/models/ud-models-1.0/opennlp-en-ud-ewt-sentence-1.0-1.9.3.bin',
      'part of speech': 'https://www.apache.org/dyn/closer.cgi/opennlp/models/ud-models-1.0/opennlp-en-ud-ewt-pos-1.0-1.9.3.bin',
      'tokens': 'https://www.apache.org/dyn/closer.cgi/opennlp/models/ud-models-1.0/opennlp-en-ud-ewt-tokens-1.0-1.9.3.bin'
    }
    model_url = self.tasks[task]
    if not exists(urlparse(model_url).path.split('/')[-1]): download(model_url, out = '.')
    opennlp = join('bin','opennlp')

