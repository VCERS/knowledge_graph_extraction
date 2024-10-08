#!/usr/bin/python3

from os.path import join, exists
import jpype
import jpype.imports
from jpype.types import *
from nltk.tree import Tree
from wget import download

class CoreNLP(object):
  def __init__(self,):
    if not exists('ejml-core-0.39.jar'): download('https://repo1.maven.org/maven2/org/ejml/ejml-core/0.39/ejml-core-0.39.jar', out = '.')
    if not exists('ejml-simple-0.39.jar'): download('https://repo1.maven.org/maven2/org/ejml/ejml-simple/0.39/ejml-simple-0.39.jar', out = '.')
    if not exists('ejml-ddense-0.39.jar'): download('https://repo1.maven.org/maven2/org/ejml/ejml-ddense/0.39/ejml-ddense-0.39.jar', out = '.')
    if not exists('protobuf-java-3.19.6.jar'): download('https://repo1.maven.org/maven2/com/google/protobuf/protobuf-java/3.19.6/protobuf-java-3.19.6.jar', out = '.')
    if not exists('stanford-corenlp-4.5.7.jar'): download('https://repo1.maven.org/maven2/edu/stanford/nlp/stanford-corenlp/4.5.7/stanford-corenlp-4.5.7.jar', out = '.')
    if not exists('stanford-corenlp-4.5.7-models.jar'): download('https://repo1.maven.org/maven2/edu/stanford/nlp/stanford-corenlp/4.5.7/stanford-corenlp-4.5.7-models.jar', out = '.')
    if not exists('stanford-corenlp-4.5.7-models-english.jar'): download('https://repo1.maven.org/maven2/edu/stanford/nlp/stanford-corenlp/4.5.7/stanford-corenlp-4.5.7-models-english.jar', out = '.')
    jpype.startJVM(classpath = ['/usr/share/java/org.jpype-1.3.0.jar','./ejml-core-0.39.jar','./ejml-simple-0.39.jar','./ejml-ddense-0.39.jar','protobuf-java-3.19.6.jar','stanford-corenlp-4.5.7.jar','stanford-corenlp-4.5.7-models.jar','stanford-corenlp-4.5.7-models-english.jar'])
    Properties = jpype.JClass('java.util.Properties')
    StanfordCoreNLP = jpype.JClass('edu.stanford.nlp.pipeline.StanfordCoreNLP')
    self.CoreDocument = jpype.JClass('edu.stanford.nlp.pipeline.CoreDocument')
    self.String = jpype.JClass('java.lang.String')
    props = Properties()
    props.setProperty('annotators', "tokenize,pos,lemma,ner,parse,depparse,coref,kbp,quote,natlog,openie")
    props.setProperty('coref.algorithm','neural')
    self.pipeline = StanfordCoreNLP(props)
  def call(self, text):
    text = self.String(text)
    document = self.CoreDocument(text)
    self.pipeline.annotate(document)
    print(document.tokens())
    print(document.openie())

if __name__ == "__main__":
  corenlp = CoreNLP()
  corenlp.call("A solution of 124C (7.0 g, 32.4 mmol) in concentrate H2SO4 " +
                "(9.5 mL) was added to a solution of concentrate H2SO4 (9.5 mL) " +
                "and fuming HNO3 (13 mL) and the mixture was heated at 60°C for " +
                "30 min. After cooling to room temperature, the reaction mixture " +
                "was added to iced 6M solution of NaOH (150 mL) and neutralized " +
                "to pH 6 with 1N NaOH solution. The reaction mixture was extracted " +
                "with dichloromethane (4x100 mL). The combined organic phases were " +
                "dried over Na2SO4, filtered and concentrated to give 124D as a solid.")
