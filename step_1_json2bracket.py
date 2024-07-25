
import json
import nltk
from nltk.tree import Tree

# Function to build the tree
def build_tree(data):
    id_to_tree = {0: ("root", [])}  # Root node
    for token in data:
        id_to_tree[token['id']] = ('z', [])  # Replace text with 'a'

    for token in data:
        head = token['head']
        if head in id_to_tree:
            id_to_tree[head][1].append(id_to_tree[token['id']])
    
    def create_nltk_tree(node):
        text, children = node
        if children:
            return Tree(text, [create_nltk_tree(child) for child in children])
        else:
            return text

    return create_nltk_tree(id_to_tree[0])

def print_custom_tree(tree):
    if isinstance(tree, Tree):
        return '{' + tree.label() + ''.join(print_custom_tree(child) for child in tree) + '}'
    else:
        return '{' + tree + '}'



def parse_json_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()  # Read all lines into a list
    
    n = len(lines)  # Total number of lines

    with open("bracket_notation_trees.txt", "w") as file:
        for x in range(n):
            try:
                data = json.loads(lines[x])
                syntax_tree = build_tree(data)
                tree_string=print_custom_tree(syntax_tree) + '\n'
                #print(tree_string)
                file.write(tree_string)

            except json.JSONDecodeError as e:
                print(f"Error decoding JSON on line {x+1}: {e}")

# Example usage
file_path = 'train.clean.en.json'
parse_json_file(file_path)
