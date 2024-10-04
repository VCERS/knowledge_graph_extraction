#!/usr/bin/python3

from os.path import exists
import jpype
import jpype.imports
from jpype.types import *
from wget import download

class Oscar4(object):
  def __init__(self, ):
    if not exists('oscar4-all-5.2.0-with-dependencies.jar'): download('https://repo.maven.apache.org/maven2/uk/ac/cam/ch/wwmm/oscar/oscar4-all/5.2.0/oscar4-all-5.2.0-with-dependencies.jar', out = '.')
    jpype.startJVM(classpath = ['/usr/share/java/org.jpype-1.3.0.jar','./oscar4-all-5.2.0-with-dependencies.jar'])
    self.String = jpype.JClass('java.lang.String')
    self.List = jpype.JClass('java.util.List')
    self.Oscar = jpype.JClass('uk.ac.cam.ch.wwmm.oscar.Oscar')
    self.ResolvedNamedEntity = jpype.JClass('uk.ac.cam.ch.wwmm.oscar.chemnamedict.entities.ResolvedNamedEntity')
    self.ChemicalStructure = jpype.JClass('uk.ac.cam.ch.wwmm.oscar.chemnamedict.entities.ChemicalStructure')
    self.FormatType = jpype.JClass('uk.ac.cam.ch.wwmm.oscar.chemnamedict.entities.FormatType')
    self.types = {
      'CM': 'Compound',
      'CMS': 'Compounds',
      'GP': 'Group',
      'RN': 'Reaction',
      'CJ': 'Adjective',
      'CPR': 'Locant Prefix',
      'AHA': 'Potential Acronym',
      'ASE': 'Ase',
      'ASES': 'Ases',
      'PN': 'Proper Noun',
      'ONT': 'Ontology Term',
      'CUST': 'Custom',
      'STOP': 'Stop Word',
      'PM': 'Polymer',
      'DATA': 'Data'
    }
  def call(self, text):
    text = self.String(text)
    oscar = self.Oscar()
    entities = oscar.findAndResolveNamedEntities(text)
    results = list()
    for i in range(entities.size()):
      entity = entities[i]
      entity_text = entity.getSurface()
      start = entity.getStart()
      end = entity.getEnd()
      type_ = entity.getType().toString()
      results.append((entity_text,start,end,self.types[type_]))
      '''
      structure = entity.getFirstChemicalStructure(self.FormatType.STD_INCHI);
      if structure != None:
        print(structure)
      '''
    return results

if __name__ == "__main__":
  oscar = Oscar4()
  entities = oscar.call('Figure 5. Kinetic characteristic tests of chemical reaction between Li1–xCoO2(x= 0, 0.3, 0.5) and typical sulfide SEs. (a) DSC curves of the Li1–xCoO2+ Li6PS5Cl mixed powder at different heating rates (3, 5, 7, 15, 20 °C/min).')
  print(entities)
