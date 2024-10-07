#!/usr/bin/python3

from shutil import rmtree
from os import walk, mkdir
from os.path import splitext, join, exists
from absl import flags, app
from tqdm import tqdm
import json
from langchain.document_loaders import UnstructuredMarkdownLoader
import pickle
from models import Llama3, Qwen2
from chains import experimental_chain
from oscar import Oscar4
from triplet import extract_triplets

FLAGS = flags.FLAGS

def add_options():
  flags.DEFINE_string('input_dir', default = None, help = 'path to input directory')
  flags.DEFINE_string('output_dir', default = 'processed', help = 'path to output directory')
  flags.DEFINE_enum('model', default = 'llama3', enum_values = {'llama3', 'qwen2'}, help = 'model to use')

def extract_triplets_by_sentence(doc):
  triplets_by_sentence = list()
  assert doc.label() == 'Document'
  for s in doc:
    assert s.label() == 'Sentence'
    triplets = extract_triplets(s)
    triplets_by_sentence.append({'triplets': triplets, 'sentence': ' '.join(s.leaves())})
  return triplets_by_sentence

def main(unused_argv):
  if exists(FLAGS.output_dir): rmtree(FLAGS.output_dir)
  mkdir(FLAGS.output_dir)
  tokenizer, llm = {
    'llama3': Llama3,
    'qwen2': Qwen2}[FLAGS.model](True)
  exp_chain = experimental_chain(llm, tokenizer)
  oscar = Oscar4()
  for root, dirs, files in tqdm(walk(FLAGS.input_dir)):
    for f in files:
      print(f'processing {f}')
      stem, ext = splitext(f)
      if ext != '.md': continue
      loader = UnstructuredMarkdownLoader(join(root, f), model = 'single', strategy = 'fast')
      text = ' '.join([doc.page_content for doc in loader.load()])
      print('1) extracting experimental part')
      results = exp_chain.invoke({'text': text})
      with open(join(FLAGS.output_dir, stem + '_experimental.md'), 'w') as f:
        f.write(results)
      print('2) parsing text')
      tree = oscar.parse(results)
      with open(join(FLAGS.output_dir, stem + '_parsetree.pkl'), 'wb') as f:
        f.write(pickle.dumps(tree))
      print('3) extracting triplets')
      triplets = extract_triplets_by_sentence(tree)
      with open(join(FLAGS.output_dir, stem + '_triplets.pkl'), 'wb') as f:
        f.write(pickle.dumps(triplets))

if __name__ == "__main__":
  add_options()
  app.run(main)

