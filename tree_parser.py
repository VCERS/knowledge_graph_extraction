#!/usr/bin/python3

class TreeNode:
  def __init__(self, value=None):
    self.value = value
    self.children = []
  def add_child(self, child_node):
    self.children.append(child_node)
  def __repr__(self, level=0):
    ret = "\t" * level + repr(self.value) + "\n"
    for child in self.children:
      ret += child.__repr__(level + 1)
    return ret
