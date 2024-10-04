#!/usr/bin/python3

from os.path import join
import pexpect
from urllib.parse import urlparse
from wget import download

class OpenNLP(object):
  def __init__(self, task = 'POSTagger'):
    self.tasks = {
      'LanguageDetector': 'https://dlcdn.apache.org/opennlp/models/langdetect/1.8.3/langdetect-183.bin',
      'SentenceDetector': 'https://dlcdn.apache.org/opennlp/models/ud-models-1.0/opennlp-en-ud-ewt-sentence-1.0-1.9.3.bin',
      'POSTagger': 'https://dlcdn.apache.org/opennlp/models/ud-models-1.0/opennlp-en-ud-ewt-pos-1.0-1.9.3.bin',
      'TokenNameFinder': 'https://dlcdn.apache.org/opennlp/models/ud-models-1.0/opennlp-en-ud-ewt-tokens-1.0-1.9.3.bin'
    }
    model_url = self.tasks[task]
    model_file = urlparse(model_url).path.split('/')[-1]
    if not exists(model_file): download(model_url, out = '.')
    self.process = pexpect.spawn(f"{join('bin','opennlp')} {task} {model_file}")
    self.process.setecho(False)
    self.process.expect('done')
    self.process.expect('\r\n')
  def call(self, text):
    
