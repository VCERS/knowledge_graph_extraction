#!/usr/bin/python3

from prompts import experimental_template

def experimental_chain(llm, tokenizer):
  exp_tmp = experimental_template(tokenizer)
  exp_chain = exp_tmp | llm
  return exp_chain

