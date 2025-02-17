#!/usr/bin/python3

from os import remove
from os.path import exists
import jpype
import jpype.imports
from jpype.types import *
from wget import download
import tempfile
import xml.etree.ElementTree as ET
from nltk.tree import Tree

class Oscar4(object):
  def __init__(self, ):
    if not exists('oscar4-all-5.2.0-with-dependencies.jar'): download('https://repo.maven.apache.org/maven2/uk/ac/cam/ch/wwmm/oscar/oscar4-all/5.2.0/oscar4-all-5.2.0-with-dependencies.jar', out = '.')
    if not exists('chemicalTagger-1.6.2.jar'): download('https://repo.maven.apache.org/maven2/uk/ac/cam/ch/wwmm/chemicalTagger/1.6.2/chemicalTagger-1.6.2.jar', out = '.')
    if not exists('antlr4-runtime-4.7.4.jar'): download('https://repo1.maven.org/maven2/com/tunnelvisionlabs/antlr4-runtime/4.7.4/antlr4-runtime-4.7.4.jar', out = ".")
    jpype.startJVM(classpath = ['/usr/share/java/org.jpype-1.3.0.jar','/usr/share/java/log4j-1.2-1.2.17.jar','/usr/share/java/opennlp-tools.jar','./antlr4-runtime-4.7.4.jar','./oscar4-all-5.2.0-with-dependencies.jar','./chemicalTagger-1.6.2.jar'])
    self.String = jpype.JClass('java.lang.String')
    self.List = jpype.JClass('java.util.List')
    self.Oscar = jpype.JClass('uk.ac.cam.ch.wwmm.oscar.Oscar')
    self.ResolvedNamedEntity = jpype.JClass('uk.ac.cam.ch.wwmm.oscar.chemnamedict.entities.ResolvedNamedEntity')
    self.ChemicalStructure = jpype.JClass('uk.ac.cam.ch.wwmm.oscar.chemnamedict.entities.ChemicalStructure')
    self.FormatType = jpype.JClass('uk.ac.cam.ch.wwmm.oscar.chemnamedict.entities.FormatType')
    self.POSContainer = jpype.JClass('uk.ac.cam.ch.wwmm.chemicaltagger.POSContainer')
    self.ChemistryPOSTagger = jpype.JPackage('uk.ac.cam.ch.wwmm.chemicaltagger').ChemistryPOSTagger
    self.ChemistrySentenceParser = jpype.JClass('uk.ac.cam.ch.wwmm.chemicaltagger.ChemistrySentenceParser')
    self.Utils = jpype.JClass('uk.ac.cam.ch.wwmm.chemicaltagger.Utils')
    self.Document = jpype.JClass('nu.xom.Document')
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
  def ner(self, text):
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
      results.append((str(entity_text),int(start),int(end),self.types[type_]))
      '''
      structure = entity.getFirstChemicalStructure(self.FormatType.STD_INCHI);
      if structure != None:
        print(structure)
      '''
    return results
  def xml_to_nltk_tree(self, element):
    children = list(element)
    if not children:
        # No children, return a leaf node
        return Tree(element.tag, [element.text])
    # Return a Tree with the element's tag and its children
    return Tree(element.tag, [self.xml_to_nltk_tree(child) for child in children])
  def parse(self, text):
    text = self.String(text)
    posContainer = self.ChemistryPOSTagger.getDefaultInstance().runTaggers(text)
    chemistrySentenceParser = self.ChemistrySentenceParser(posContainer)
    chemistrySentenceParser.parseTags()
    doc = chemistrySentenceParser.makeXMLDocument()
    with tempfile.NamedTemporaryFile(delete = False, mode = 'w+', encoding = 'utf-8') as tmpfile:
      self.Utils.writeXMLToFile(doc, tmpfile.name)
      tmpfile_name = tmpfile.name
    root = ET.parse(tmpfile_name).getroot()
    tree = self.xml_to_nltk_tree(root)
    remove(tmpfile_name)
    return tree
  def extract_triplets_from_sentence(self, tree):
    triplets = list()
    subject = None
    predicate = None
    obj = None
    
    for subtree in tree:
        if type(subtree) is str:
            # skip terminal node
            continue
        # find object, predicate, subject in this subtree
        if subtree.label() == 'NounPhrase' and not subject:
            # generate object from noun phrase
            subject = ' '.join(subtree.leaves())
        elif subtree.label() == 'VerbPhrase':
            # generate predicate and subject from verb phrase
            for vp_subtree in subtree:
                if type(vp_subtree) is str: continue
                if vp_subtree.label().startswith('V'):
                    predicate = ' '.join(vp_subtree.leaves())
                elif vp_subtree.label() in ['NounPhrase', 'PrepPhrase']:
                    # both noun phrase and preposition phrase can be subject
                    obj = ' '.join(vp_subtree.leaves())
        # if this is a non-terminal node, recursively generate triplets among its children
        if len(subtree) > 0:
            triplets.extend(self.extract_triplets_from_sentence(subtree))
    if subject and predicate and obj:
        triplets.append((subject, predicate, obj))
    
    return triplets
  def triplets(self, tree):
    triplets_by_sentence = list()
    assert tree.label() == 'Document'
    for s in tree:
      assert s.label() == 'Sentence'
      triplets = self.extract_triplets_from_sentence(s)
      triplets_by_sentence.append({'triplets': triplets, 'sentence': ' '.join(s.leaves())})
    return triplets_by_sentence

if __name__ == "__main__":
  oscar = Oscar4()
  '''
  entities = oscar.ner('Figure 5. Kinetic characteristic tests of chemical reaction between Li1–xCoO2(x= 0, 0.3, 0.5) and typical sulfide SEs. (a) DSC curves of the Li1–xCoO2+ Li6PS5Cl mixed powder at different heating rates (3, 5, 7, 15, 20 °C/min).')
  print(entities)
  tree = oscar.parse("A solution of 124C (7.0 g, 32.4 mmol) in concentrate H2SO4 " +
	            "(9.5 mL) was added to a solution of concentrate H2SO4 (9.5 mL) " +
	            "and fuming HNO3 (13 mL) and the mixture was heated at 60°C for " +
	            "30 min. After cooling to room temperature, the reaction mixture " +
	            "was added to iced 6M solution of NaOH (150 mL) and neutralized " +
	            "to pH 6 with 1N NaOH solution. The reaction mixture was extracted " +
	            "with dichloromethane (4x100 mL). The combined organic phases were " +
	            "dried over Na2SO4, filtered and concentrated to give 124D as a solid.")
  print(tree)
  '''
  s = """10.1002/adma.200903953
High-Performance Oxygen-Permeable Membranes with an Asymmetric Structure Using Ba0.95La0.05FeO3-δ Perovskite-Type Oxide
A porous BLF support was fabricated by an oxalate method 28. Ba (9.5 mmol) and La (0.5 mmol) acetates and Fe nitrate (10 mmol) were first dissolved in water (100 mL). The mixed metal salt solution was then added to ethanol (100 mL) containing oxalic acid (90 mmol). The mixing produced a yellow-colored suspension, which was allowed to stand for 1 h. The use of ethanol was critical to the precipitation of the metal oxalates. The suspension was filtrated to collect the precursor metal oxalate particles. The obtained precursor powder was dried at 120 degC for 2 h and then calcined at 700 degC for 2 h. The calcined powder was press-formed into a disk to form a green porous support disk. A BLF powder as the precursor of a dense layer was prepared by an AMP method 31. An aqueous malic acid solution (50 mL) was added to a solution (50 mL) containing the corresponding metal nitrates or acetates in a stoichiometric ratio under vigorous stirring. The molar ratio of malic acid to total metal ions was set to 1.5. The pH of the mixed aqueous solution was adjusted to 6 with aqueous ammonia (28%). The mixed solution was evaporated to dryness and the obtained powder was calcined in air at 800 degC. The calcined powder was ground and dispersed in ethanol to prepare a precursor slurry (10 wt %) for fabricating a dense layer on a porous support. A dense BLF layer was formed by dropping the slurry (0.6 mL) on the green porous support. The support disk was dried at room temperature and sintered at 1175 degC for 5 h to fabricate an asymmetric BLF membrane. For comparison, sintered-disk-type BLF membranes were also fabricated using the BLF powder prepared by the AMP method. The thickness of the sintered-disk membranes was controlled to about 1.0 and 0.5 mm by polishing the surfaces with emery paper (# 80). The morphology of the surface and cross-sections of the asymmetric membrane were observed with a SEM (JSM-6340F, JEOL Co., LTD.). The oxygen permeation flux through the fabricated asymmetric membrane was measured using the apparatus used in the previous study 18. The dense layer side of the asymmetric membrane was fixed on a quartz tube using a silver ring as an adhesive agent at 960-970 degC. Air (O2/N2 mixture gases) and He were supplied to the porous support side and dense layer side, respectively. The flow rates of air (O2/N2 mixture gases) and He were 200 and 150 mL min-1, respectively. The concentration of permeated oxygen from the air side to the He side was detected with a thermal conductivity detector (TCD) of a gas chromatograph directly connected to the effluent line of the dense layer side."""
  entities = oscar.ner(s)
  print(entities)
  tree = oscar.parse(s)
  print(tree)
