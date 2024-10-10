#!/usr/bin/python3

from shutil import rmtree
from os import walk, mkdir
from os.path import splitext, join, exists
from absl import flags, app
from tqdm import tqdm
from nltk.tree import Tree
import json
from langchain.document_loaders import UnstructuredMarkdownLoader
import pickle
from models import Llama3, Qwen2
from chains import experimental_chain
from oscar import Oscar4
from corenlp import CoreNLP

FLAGS = flags.FLAGS

def add_options():
  flags.DEFINE_string('input_dir', default = None, help = 'path to input directory')
  flags.DEFINE_string('output_dir', default = 'processed', help = 'path to output directory')
  flags.DEFINE_enum('model', default = 'llama3', enum_values = {'llama3', 'qwen2'}, help = 'model to use')
  flags.DEFINE_enum('method', default = 'corenlp', enum_values = {'oscar', 'corenlp'}, help = 'which method to use for triplet extraction')
  flags.DEFINE_boolean('only_exp', default = False, help = 'whether to use only experimental part of the paper')

def tree2dict(tree):
  if isinstance(tree, str):
    return tree
  if isinstance(tree, Tree):
    return {
      'label': tree.label(),
      'children': [tree2dict(child) for child in tree]
    }
  else:
    return [tree2dict(child) for child in tree]

def main(unused_argv):
  if exists(FLAGS.output_dir): rmtree(FLAGS.output_dir)
  mkdir(FLAGS.output_dir)
  if FLAGS.only_exp:
    tokenizer, llm = {
      'llama3': Llama3,
      'qwen2': Qwen2}[FLAGS.model](True)
    exp_chain = experimental_chain(llm, tokenizer)
  if FLAGS.method == 'oscar':
    oscar = Oscar4()
  elif FLAGS.method == 'corenlp':
    corenlp = CoreNLP()
  else:
    raise Exception('unknown method!')
  for root, dirs, files in tqdm(walk(FLAGS.input_dir)):
    for f in files:
      print(f'processing {f}')
      stem, ext = splitext(f)
      if ext != '.md': continue
      loader = UnstructuredMarkdownLoader(join(root, f), model = 'single', strategy = 'fast')
      text = ' '.join([doc.page_content for doc in loader.load()])
      if FLAGS.only_exp:
        print('1) extracting experimental part')
        text = exp_chain.invoke({'text': text})
        with open(join(FLAGS.output_dir, stem + '_experimental.md'), 'w') as f:
          f.write(text)
      print('2) named entity recognition')
      if FLAGS.method == 'oscar':
        ne = oscar.ner(text)
      elif FLAGS.method == 'corenlp':
        ne = corenlp.ner(text)
      else:
        raise Exception('unknown method!')
      with open(join(FLAGS.output_dir, stem + '_ner.json'), 'w') as f:
        f.write(json.dumps(ne, indent = 2, ensure_ascii = False))
      print('3) parsing text')
      if FLAGS.method == 'oscar':
        tree = oscar.parse(text)
      elif FLAGS.method == 'corenlp':
        tree = corenlp.parse(text)
      else:
        raise Exception('unknown method!')
      with open(join(FLAGS.output_dir, stem + '_parsetree.json'), 'w') as f:
        f.write(json.dumps(tree2dict(tree), indent = 2, ensure_ascii = False))
      print('4) extracting triplets')
      if FLAGS.method == 'oscar':
        triplets = oscar.triplets(tree)
      elif FLAGS.method == 'corenlp':
        triplets = corenlp.triplets(text)
      else:
        raise Exception('unknown method!')
      with open(join(FLAGS.output_dir, stem + '_triplets.json'), 'w') as f:
        f.write(json.dumps(triplets, indent = 2, ensure_ascii = False))

if __name__ == "__main__":
  add_options()
  app.run(main)

