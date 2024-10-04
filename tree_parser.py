#!/usr/bin/python3

class TreeNode:
  def __init__(self, value=None):
    self.value = value
    self.children = []
  def add_child(self, child_node):
    self.children.append(child_node)
  def __repr__(self, level=0):
    ret = "\t" * level + repr((self.type, self.value)) + "\n"
    for child in self.children:
      ret += child.__repr__(level + 1)
    return ret

def parse_parentheses(s):
  stack = []  
  current_node = None  
      
  for char in s:  
    if char == '(':  
      # Create a new node (we can use None as a placeholder for empty nodes)  
      new_node = TreeNode()  
      if current_node:  
        current_node.add_child(new_node)  
      stack.append(current_node)  
      current_node = new_node  
    elif char == ')':  
      current_node = stack.pop() if stack else None  
    elif char.isalpha():  
      # Create a new node with the character as its value  
      new_node = TreeNode(char)  
      if current_node:  
        current_node.add_child(new_node)  
      # We don't change the current_node here because new_node is already added  
  
  return stack[0] if stack else None  # The root node will be the last item in the stack if not empty

if __name__ == "__main__":
  s = '(TOP (S (NP (NN Figure)) (VP (VBD 5.) (NP (NP (JJ Kinetic) (JJ characteristic) (NNS tests)) (PP (IN of) (NP (NP (JJ chemical) (NN reaction)) (PP (IN between) (NP (NP (NP (NNP Li1–xCoO2)) (PRN (-LRB- -LRB-) (NP (NN x=) (JJ 0,) (JJ 0.3,) (CD 0.5)) (-RRB- -RRB-))) (CC and) (NP (NP (JJ typical) (NN sulfide) (NNP SEs.)) (PRN (-LRB- -LRB-) (PP (NP (NP (NP (DT a) (-RRB- -RRB-) (NNP DSC) (NNS curves)) (PP (IN of) (NP (DT the) (JJ Li1–xCoO2+) (NNP Li6PS5Cl) (JJ mixed) (NN powder)))) (PP (IN at) (NP (NP (JJ different) (NN heating) (NNS rates)) (PRN (-LRB- -LRB-) (NP (QP (CD 3,) (CD 5,) (CD 7,)) (JJ 15,) (CD 20) (NN °C/min)) (-RRB- -RRB-)))))))))))))) (. .)))'
  tree = parse_parentheses(s)

