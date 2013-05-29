""" A simple python script to analyse a python source file(s).
    The idea is to count the size of the file in terms of lines, then
    also parse the file using the standard-library's parser and estimate
    the size of the source tree in terms of the nodes in the parse tree.
"""

import argparse
import ast

# Known disadvantage that it is highly dependent on how the code is
# formatted
def get_number_of_lines(source):
  num_source_lines = 0
  for line in source.splitlines():
    num_source_lines += 1 
  return num_source_lines

# This has the distinct disadvantage that it does not count comments
def get_number_of_nodes(node):
  num_nodes = 1
  for child_node in ast.iter_child_nodes(node):
    num_nodes += get_number_of_nodes(child_node)
  return num_nodes

# In contrast to number of lines this doesn't depend so heavily on
# how the code is formatted. It does take into account comments, unlike
# the number of nodes in the source parse tree. It also, like the nodes
# in the parse tree method, won't be dependent on how long variable names
# are. This is a promising compromise.
def get_number_of_tokens(source):
  num_tokens = 0
  for token in source.split():
    num_tokens += 1
  return num_tokens

def analyse_source_file(filename):
  file = open(filename, "r")
  source = file.read()
  file.close()

  num_source_lines = get_number_of_lines(source)
  print ("Number of source lines is: " + str(num_source_lines))

  parse_tree = ast.parse(source)
  num_nodes = get_number_of_nodes(parse_tree)

  print ("The number of nodes in the parse tree is: " + str(num_nodes))

  num_tokens = get_number_of_tokens(source)
  print ("The number of tokens in the source is: " + str(num_tokens))


def run():
  """ The main method.  """ 
  description = "Analyse the size of the code in a python source file"
  argparser = argparse.ArgumentParser(add_help=True,
                                      description=description)
  argparser.add_argument('filenames', metavar='F', nargs='+',
                         help="A file to analyse")
  

  arguments = argparser.parse_args()
  for filename in arguments.filenames:
    analyse_source_file(filename)
  

if __name__ == "__main__":
  run()
