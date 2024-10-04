#!/usr/bin/python3

import jpype
import jpype.imports
from jpype.types import *

class Oscar4(object):
  def __init__(self, ):
    jpype.startJVM(classpath = ['/usr/share/java/org.jpype-1.3.0.jar','./oscar4-all-5.2.0-with-dependencies.jar'])
    self.String = jpype.JClass('java.lang.String')
    self.List = jpype.JClass('java.util.List')
    self.Oscar = jpype.JClass('uk.ac.cam.ch.wwmm.oscar.Oscar')
    self.ResolvedNamedEntity = jpype.JClass('uk.ac.cam.ch.wwmm.oscar.chemnamedict.entities.ResolvedNamedEntity')
    self.ChemicalStructure = jpype.JClass('uk.ac.cam.ch.wwmm.oscar.chemnamedict.entities.ChemicalStructure')
    self.FormatType = jpype.JClass('uk.ac.cam.ch.wwmm.oscar.chemnamedict.entities.FormatType')
  def call(self, s):
    s = 'Figure 5. Kinetic characteristic tests of chemical reaction between Li1–xCoO2(x= 0, 0.3, 0.5) and typical sulfide SEs. (a) DSC curves of the Li1–xCoO2+ Li6PS5Cl mixed powder at different heating rates (3, 5, 7, 15, 20 °C/min).'
    s = self.String(s)
    oscar = self.Oscar()
    entities = oscar.findAndResolveNamedEntities(s)
    for i in range(entities.size()):
      ne = entities[i]
      print(ne.getSurface())
      stdInchi = ne.getFirstChemicalStructure(self.FormatType.STD_INCHI);
      if stdInchi != None:
        print(stdInchi)

if __name__ == "__main__":
  oscar = Oscar4()
  oscar.call('')
