#!/usr/bin/python3

from os.path import join, exists
import jpype
import jpype.imports
from jpype.types import *
from nltk.tree import Tree
from wget import download

class CoreNLP(object):
  def __init__(self,):
    if not exists('stanford-corenlp-4.5.7-models-english.jar'): download('https://search.maven.org/remotecontent?filepath=edu/stanford/nlp/stanford-corenlp/4.5.7/stanford-corenlp-4.5.7-models-english.jar', out = '.')
    jpype.startJVM(classpath = ['/usr/share/java/org.jpype-1.3.0.jar','stanford-corenlp-4.5.7-models-english.jar'])
    Properties = jpype.JClass('java.util.Properties')
    StanfordCoreNLP = jpype.JClass('edu.standford.nlp.pipeline.StanfordCoreNLP')
    self.CoreDocument = jpype.JClass('edu.stanford.nlp.pipeline.CoreDocument')
    self.String = jpype.JClass('java.lang.String')
    props = Properties()
    props.setProperty('annotators', "tokenize,pos,lemma,ner,parse,depparse,coref,kbp,quote,openie")
    props.setProperty('coref.algorithm','neural')
    self.pipeline = StanfordCoreNLP(props)
  def call(self, text):
    text = self.String(text)
    document = self.CoreDocument(text)
    self.pipeline.annotate(document)
    print(document.tokens())
    print(document.openie())
