#!/usr/bin/python3

from langchain_core.prompts.prompt import PromptTemplate

def experimental_template(tokenizer):
  messages = [
    {'role': 'system', 'content': 'Given a full text of a paper. Please return the original text of the experimental part of the paper. If the experimental part is not present in the paper, just return "<no experimental>".'},
    {'role': 'user', 'content': 'the full text:\n\n{text}'}
  ]
  prompt = tokenizer.apply_chat_template(messages, tokenize = False, add_generating_prompt = True)
  template = PromptTemplate(template = prompt, input_variables = ['text'])
  return template
